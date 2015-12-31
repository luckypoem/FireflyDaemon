#FireflyDaemon
本项目将firefly服务端改写为twisted的守护进程程序. 可以直接在后台运行, 不需要像以前一样使用`python startmaster.py &`的方式让程序在后台运行, 且不会像原来一样出现大量的日志写入异常. 另外还修改了master主进程创建各子进程的方式, 同样是使用的twisted的service, 在子进程异常退出后, ProcessMonitor 会自动重启退出的子进程

## FireFlayDaemon 的依赖:
FireFlayDaemon的依赖和firefly基本相同，只是多了psutil包
```
pip install psutil
pip install twisted
pip install zope.interface
pip install DBUtils
pip install affinity
pip install python-memcached
pip install MySQL-python
```

## 如何启动服务器
在安装好依赖后，在startmaster.py所在的根目录下执行如下命令(服务端将自动在后台运行, 并按天生成运行日志到`logs/master.log`文件中):
```
twistd -y startmaster.py
```
使用下面的命令将不会在后台运行，也不会创建`logs/master.log`日志(直接使用`Ctrl + C`退出程序即可自动保存数据):
```
twisted -ny startmaster.py
```

## 停止服务
停止服务的方法和firefly相同, 都是访问本地URL:
```
curl http://127.0.0.1:9998/stop
```
但本程序的Master主进程会在所有子进程安全退出后才会退出, 而在master主进程未退出时再次启动服务, 会提示程序已在运行中, 避免出现一不小心运行多个实例的情况

## 查看服务器状态
在服务器启动后可以通过如下命令查看服务器进程的状态:
```
curl http://127.0.0.1:9998/status
```

显示结果如图:

![status](https://git.oschina.net/cbwfree/FireflyDaemon/raw/master/demo/status.png)