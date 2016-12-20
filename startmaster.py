# coding: utf8
"""
启动服务器
@name: startmaster.py
@author: cbwfree
@create: 15/12/29 20:02
"""
import sys
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from firefly.master.master import Master, MULTI_SERVER_MODE
from twisted.application import service
import initialize


APP_NAME = "firefly"
APP_SCRIPT = "appmain.py"


# 创建Application容器
application = service.Application(APP_NAME)

# 创建守护进程
master = Master()
master.set_script(APP_SCRIPT)                   # 设置启动脚本
master.set_mode(MULTI_SERVER_MODE)              # 设置启动模式
master.start(application)                       # 启动守护进程
