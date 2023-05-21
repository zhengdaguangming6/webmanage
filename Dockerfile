# 启动运行基本系统
FROM ubuntu
FROM docker.io/python:3.9.7
# 导入项目文件
ADD ./ /home/webmanage
WORKDIR /home/webmanage
# 安装软件环境
RUN apt-get update && apt-get install python3-pip -y && pip3 install -r requirements.txt
# 指定对外开放端口
EXPOSE 8001
# 运行项目
ENTRYPOINT uwsgi --ini uwsgi.ini
