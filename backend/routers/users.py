import datetime
from io import StringIO
from fastapi import Depends
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, HTTPException
from sqlalchemy import delete, insert, select, update
from routers.oauth2_scheme import oauth2_scheme
from sms import BAIDUSMS
from utils import check_verify_code, generate_numeric_code_randint, get_token, get_userInfo_from_token, password_hash
import schemas
from database import TurUsers, TurVerifyCodes, get_db
from sqlalchemy.ext.asyncio import AsyncSession

# 创建一个 APIRouter 实例
router = APIRouter()

# 登录
@router.post("/api/login", response_model=schemas.UserLoginRequestOut)
async def login(request: schemas.UserLoginRequestIn, db: AsyncSession = Depends(get_db)):
    """
    用户登录
    """
    query_stmt = select(TurUsers).where(TurUsers.phone_number == request.phone_number)
    result = await db.execute(query_stmt)
    userinfo = result.scalar_one_or_none()

    if userinfo is None:
        raise HTTPException(status_code=401, detail="手机号未注册")

    checkPassword = password_hash(request.password)
    if (checkPassword == userinfo.password_hash):
        token = get_token(userinfo)
        
        return schemas.UserLoginRequestOut(
            code=200,
            message="success",
            data=schemas.UserLoginToken(token=token)
        )
    else:
        raise HTTPException(status_code=401, detail="用户密码错误")

# 注册
@router.post("/api/register", response_model=schemas.UserRegisterRequestOut, summary="用户注册")
async def register(request: schemas.UserRegisterRequestIn, db: AsyncSession = Depends(get_db)):
    """
    用户注册
    """
    # 检测用户是否注册
    query_stmt = select(TurUsers).where(
        TurUsers.phone_number == request.phone_number
    )
    result = await db.scalar(query_stmt)
    if result is not None:
        raise HTTPException(status_code=409, detail="手机号已被注册")

    # 检测验证码
    await check_verify_code(db, request.phone_number, request.verify_code, schemas.UserGetVerifyCodePurposeEnum.REGISTER)

    # 注册用户
    passwordh = password_hash(request.password)
    insert_stmt = insert(TurUsers).values(
        phone_number=request.phone_number,
        password_hash=passwordh
    )

    result = await db.execute(insert_stmt)
    # result.inserted_primary_key[0]
    await db.commit()

    return schemas.UserRegisterRequestOut(
        code=200,
        message="注册成功"
    )

# 重置密码
@router.post("/api/reset_password", response_model=schemas.UserResetPasswordRequestOut, summary="重置密码")
async def reset_password(request: schemas.UserResetPasswordRequestIn, db: AsyncSession = Depends(get_db)):
    """
    重置密码
    """
    # 检测用户是否注册
    user_exists_stmt = select(TurUsers).where(TurUsers.phone_number == request.phone_number)
    result = await db.execute(user_exists_stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="手机号未注册")

    # 检测验证码
    await check_verify_code(db, request.phone_number, request.verify_code, schemas.UserGetVerifyCodePurposeEnum.FORGOT_PASSWORD)

    # 重置密码
    update_stmt = update(TurUsers).where(
        TurUsers.phone_number == request.phone_number
    ).values(
        password_hash=password_hash(request.new_password)
    )

    result = await db.execute(update_stmt)
    await db.commit()

    return schemas.UserResetPasswordRequestOut(
        code=200,
        message="重置密码成功"
    )

# 获取手机验证码
@router.post("/api/get_verify_code", response_model=schemas.UserGetVerifyCodeRequestOut, summary="获取验证码")
async def get_verify_code(request: schemas.UserGetVerifyCodeRequestIn, db: AsyncSession = Depends(get_db)):
    # ------------------------------------------------------------------------
    # 60秒内同一手机号不能重复获取验证码
    select_stmt = select(
        TurVerifyCodes
    ).where(
        TurVerifyCodes.phone_number == request.phone_number
    ).order_by(
        TurVerifyCodes.id.desc()
    ).limit(1)
    lastVerifyCode = (await db.execute(select_stmt)).scalar()

    if lastVerifyCode is not None:
        if lastVerifyCode.created_at > datetime.datetime.now() - datetime.timedelta(seconds=60):
            raise HTTPException(status_code=429, detail="60秒内不允许重复获取验证码")
    # ------------------------------------------------------------------------

    # 查看是否注册
    if request.purpose == schemas.UserGetVerifyCodePurposeEnum.REGISTER:
        query_stmt = select(TurUsers).where(TurUsers.phone_number == request.phone_number)
        userinfo = await db.scalar(query_stmt)
        if userinfo is not None:
            raise HTTPException(status_code=409, detail="手机号已被注册")

    # 验证码
    code = str(generate_numeric_code_randint())

    # 调用接口发送验证码
    if request.purpose == schemas.UserGetVerifyCodePurposeEnum.REGISTER:
        BAIDUSMS.send_register_verify_code(request.phone_number, code)
    elif request.purpose == schemas.UserGetVerifyCodePurposeEnum.FORGOT_PASSWORD:
        BAIDUSMS.send_reset_password_verify_code(request.phone_number, code)

    # 保存验证码
    insert_stmt = insert(TurVerifyCodes).values(
        phone_number=request.phone_number,
        code=code,
        purpose=request.purpose,
        is_used=False
    )
    result = await db.execute(insert_stmt)
    await db.commit()

    return schemas.UserGetVerifyCodeRequestOut(
        code=200,
        message="获取验证码成功"
    )

# 获取手机验证码列表(测试用)
@router.get("/api/get_verify_code_list", response_class=HTMLResponse, summary="获取验证码列表")
async def get_verify_code_list(db: AsyncSession = Depends(get_db)):
    select_stmt = select(TurVerifyCodes).order_by(TurVerifyCodes.id.desc())
    data = (await db.scalars(select_stmt)).all()

    s = StringIO()

    script = """
<script>
function clearVerifyCodeList() {
    fetch("/api/clear_verify_code_list", {
        method: "POST"
    }).then(res => {
        if (res.status == 200) {
            location.reload();
        }
    })
}
</script>
"""

    s.write(script)

    s.write('<table style="border-collapse: collapse; width: 1000px;">')
    s.write('<thead><tr>')

    s.write('<th style="border: 1px solid black; padding: 4px; text-align: left;">电话</th>')
    s.write('<th style="border: 1px solid black; padding: 4px; text-align: left;">验证码</th>')
    s.write('<th style="border: 1px solid black; padding: 4px; text-align: left;">用途</th>')
    s.write('<th style="border: 1px solid black; padding: 4px; text-align: left;">是否已使用</th>')
    s.write('<th style="border: 1px solid black; padding: 4px; text-align: left;">使用时间</th>')
    s.write('<th style="border: 1px solid black; padding: 4px; text-align: left;">创建日期</th>')
    s.write('</tr></thead>')
    s.write('<tbody>')

    if len(data) > 0:
        for item in data:
            s.write('<tr>')
            s.write(f'<td style="border: 1px solid black; padding: 4px;">{item.phone_number}</td>')
            s.write(f'<td style="border: 1px solid black; padding: 4px;">{item.code}</td>')
            s.write(f'<td style="border: 1px solid black; padding: 4px;">{item.purpose}</td>')
            if item.is_used:
                s.write(f'<td style="border: 1px solid black; padding: 4px;">是</td>')
            else:
                s.write(f'<td style="border: 1px solid black; padding: 4px;">否</td>')
            s.write(f'<td style="border: 1px solid black; padding: 4px;">{item.used_at}</td>')
            s.write(f'<td style="border: 1px solid black; padding: 4px;">{item.created_at}</td>')
            s.write('</tr>')
    else:
        s.write("<tr><td style=\"border: 1px solid black; padding: 4px; text-align: center;\" colspan=\"6\">无数据</td></tr>")

    s.write("</tbody>")
    s.write("</table>")
    s.write("<br />")
    s.write(f"<button onclick=\"clearVerifyCodeList()\">清空</button>")
    content = s.getvalue()
    s.close()

    return content


# 清空手机验证码列表(测试用)
@router.post("/api/clear_verify_code_list", response_model=schemas.BaseResponse, summary="清空验证码列表")
async def clear_verify_code_list(db: AsyncSession = Depends(get_db)):
    delete_stmt = delete(TurVerifyCodes)
    data = await db.execute(delete_stmt)

    await db.commit()

    return schemas.BaseResponse(code=200, message="清空成功")

# 获取用户信息
@router.post("/api/userinfo", response_model=schemas.UserInfoRequestOut)
async def userinfo(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        userinfo = get_userInfo_from_token(token)
    except:
        raise HTTPException(status_code=401, detail="token解析错误")

    return schemas.UserInfoRequestOut(
        code=200,
        message="success",
        data=schemas.UserInfo(
            phone_number=userinfo['phone_number']
        )
    )

# test
@router.post("/api/test", response_class=HTMLResponse)
async def test():
    return "hello world"
