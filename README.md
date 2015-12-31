#FireflyDaemon

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
在安装好依赖后，在startmaster.py所在的根目录下执行:
```
twistd -y startmaster.py
```
服务端将自动在后台运行, 并按天生成运行日志到 `logs/master.log` 文件中
使用下面的命令将不会在后台运行，也不会创建`logs/master.log`日志:
```
twisted -ny startmaster.py
```
使用上面的命令运行时，直接`Ctrl + C`退出程序即可自动保存数据

## 停止服务
停止服务的方法和firefly相同, 都是访问本地URL:
```
curl http://127.0.0.1:9998/stop
```
但本程序的Master主进程会在所有子进程安全退出后才会退出, 而在master主进程未退出时再次启动服务, 会提示程序已在运行中, 避免一不小心运行多个实例
