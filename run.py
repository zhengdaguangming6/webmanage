import os
print("开始执行启动uwsgi")

print("执行命令：cd /home/webmanage")
os.popen(r"/home/webmanage")

start = os.popen('uwsgi --ini uswgi.ini').read()
print("执行命令： uwsgi --ini uwsgi.ini")
print(start)

print("脚本执行完毕")