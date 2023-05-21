import os
print("开始执行停止uwsgi")

print("执行命令：cd /home/webmanage")
os.chdir(r"/home/webmanage")

print("执行命令：uwsgi --stop uwsgi.pid")
stop = os.popen("uwsgi --stop uwsgi.pid").read()
print(stop)

print("执行脚本完毕")