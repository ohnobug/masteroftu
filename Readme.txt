项目组件清单
nginx: Web服务器。托管前端静态页面，并作为后端 API 和 WebSocket 的反向代理。
frontend: 前端项目。通过 dockerbuild.sh 脚本构建，并将产物部署到 Nginx。
backend: 后端服务，分为两个 Docker 镜像：
Dockerfile_api: FastAPI 接口服务，处理核心业务逻辑。
Dockerfile_ws: Socket.IO 服务，负责实时通信，并与大语言模型对接。
moodle: 集成的 Moodle 开源教育平台。
dbbackup: 数据库备份模块。内含 backup.sh 脚本，用于执行数据备份。
