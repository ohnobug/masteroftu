#!/bin/bash

# 前端
export buildfrontend="cd frontend/ && ./dockerbuild05.sh && cd .."

# 数据库
export rebuild_mariadb="docker compose -f docker-compose05.yml build mariadb && docker compose -f docker-compose05.yml down mariadb && docker compose -f docker-compose05.yml up mariadb -d"

# Moodle
export rebuild_moodle="docker compose -f docker-compose05.yml build moodle && docker compose -f docker-compose05.yml down moodle && docker compose -f docker-compose05.yml up moodle -d"

# API
export rebuild_newmoodle_api="docker compose -f docker-compose05.yml build newmoodle_api && docker compose -f docker-compose05.yml down newmoodle_api && docker compose -f docker-compose05.yml up newmoodle_api -d"

# rabbitmq
export rebuild_rabbitmq="docker compose -f docker-compose05.yml build rabbitmq && docker compose -f docker-compose05.yml down rabbitmq && docker compose -f docker-compose05.yml up rabbitmq -d"

# Socket.io
export rebuild_newmoodle_ws="docker compose -f docker-compose05.yml build newmoodle_ws && docker compose -f docker-compose05.yml down newmoodle_ws && docker compose -f docker-compose05.yml up newmoodle_ws -d"

# Nginx
export rebuild_nginx="docker compose -f docker-compose05.yml build nginx && docker compose -f docker-compose05.yml down nginx && docker compose -f docker-compose05.yml up nginx -d"


echo -e "\n=======================================\n🚀正在构建Mariadb\n=======================================\n"            && eval $rebuild_mariadb
echo -e "\n=======================================\n🚀正在构建moodle\n=======================================\n"             && eval $rebuild_moodle
echo -e "\n=======================================\n🚀正在构建前端项目\n=======================================\n"            && eval $buildfrontend
echo -e "\n=======================================\n🚀正在构建rabbitmq\n=======================================\n"           && eval $rebuild_rabbitmq
echo -e "\n=======================================\n🚀正在构建新官网Socket.io服务\n=======================================\n" && eval $rebuild_newmoodle_ws
echo -e "\n=======================================\n🚀正在构建新官网接口\n=======================================\n"          && eval $rebuild_newmoodle_api
echo -e "\n=======================================\n🚀正在构建新官网Nginx服务\n=======================================\n"     && eval $rebuild_nginx


# # 查看日志
# docker logs -f masteroftu-newmoodle_api-1
