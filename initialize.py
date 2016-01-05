# coding:utf8
"""
初始化配置文件
"""
import sys
from multiprocessing import cpu_count
from firefly.server.config import Config, ServerConfig

# 创建Game节点数量
TOTAL_GAME_NODE = 4
# 是否绑定CPU核心
IS_BIND_CPU = False


# =============   配置服务器信息   ================
# 设置master信息
Config().setMaster(
    roothost="127.0.0.1",
    rootport=9999,
    webport=9998
)
# 设置memcached缓存
Config().setCache({
    'urls': ["127.0.0.1:11211"],
    'hostname': "firefly"
})
# 设置数据库连接
Config().setDb(
    db="db_name",
    host="127.0.0.1",
    port=3306,
    user="root",
    passwd="123456",
    charset="utf8",
    conv={10: str, 246: float}
)

# =============   设置服务器节点   ================
# Net节点
node = ServerConfig("net")
node.set_log()
node.set_net(20000)
node.set_web(22000)
node.set_ws(21000)
node.set_remote("gate")
Config().addServer(node)

# Gate节点
node = ServerConfig("gate")
node.set_log()
# node.set_db()
# node.set_reload()
node.set_root(20001)
node.set_remote("share", "middle", "logs")
Config().addServer(node)

# Sync节点
node = ServerConfig("sync")
node.set_log()
# node.set_db()
# node.set_mem()
Config().addServer(node)

# 创建Game节点
total = cpu_count()             # 获取CPU核心数
if total > TOTAL_GAME_NODE > 0:
    total = TOTAL_GAME_NODE
else:
    total -= 1                  # 保留一个核心
for cpu_id in xrange(total):
    node = ServerConfig("game", "game_%s" % (cpu_id + 1))
    node.set_log()
    # node.set_db()
    # node.set_mem()
    # node.set_reload()
    node.set_remote("gate", "share", "middle", "logs", "battle")
    if IS_BIND_CPU and sys.platform in ('win32', 'linux2'):
        node.set_cpu(cpu_id + 1)
    Config().addServer(node)


