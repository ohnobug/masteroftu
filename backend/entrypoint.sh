#!/bin/sh

# 遇到任何错误则立即退出
set -e

# 动态计算 worker 数量
# NPROC=$(nproc) # 获取 CPU 核心数
# WORKER_COUNT=$((1 * NPROC + 1))
# echo "CPU cores: $NPROC, Starting with $WORKER_COUNT workers."

# 或者，如果您想用环境变量来控制，可以这样写：
# 如果 WORKERS 环境变量未设置，则默认使用 nproc 计算，否则使用环境变量的值
# : "${WORKERS:=$(($(nproc) + 1))}"
# echo "Starting with $WORKERS workers."

# 最终的主命令。
# 使用 exec 将 uvicorn 进程替换当前 shell 进程，使其成为 PID 1
# 这样 uvicorn 就能直接接收来自 Docker 的信号了
# exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers "$WORKERS"

# 简化版：直接在启动命令中计算worker数量
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers "$WORKERS"