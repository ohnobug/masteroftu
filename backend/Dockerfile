FROM python:3.10-slim-bullseye

# 2. 设置工作目录
WORKDIR /app

# 3. 设置环境变量，防止 Python 写入 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. 安装系统依赖 (如果需要的话，例如构建某些库需要 gcc)
# RUN apt-get update && apt-get install -y build-essential

# 5. 复制依赖文件并安装
#    先复制 requirements.txt 是为了利用 Docker 的层缓存
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. 复制所有应用代码到工作目录
COPY . .

# 7. 暴露应用运行的端口
EXPOSE 8000

# 8. 定义容器启动时运行的命令
#    --host 0.0.0.0 让容器外的请求可以访问到应用
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8001"]