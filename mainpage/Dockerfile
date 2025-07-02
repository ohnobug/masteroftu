FROM nginx:latest

# 删除默认的 Nginx 配置
RUN rm /etc/nginx/conf.d/default.conf

# 将我们自定义的配置文件复制到容器的配置目录中
COPY nginx.conf /etc/nginx/conf.d/nginx.conf

COPY certs/turcar.net.cn.key /etc/ssl/certs/turcar.net.cn.key
COPY certs/fullchain.cer /etc/ssl/certs/fullchain.cer

# 暴露 80 端口
EXPOSE 80
