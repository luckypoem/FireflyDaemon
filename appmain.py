# coding: utf8
import os
import sys
from firefly.server.server import FFServer

reload(sys)
sys.setdefaultencoding("utf-8")


if os.name != 'nt' and os.name != 'posix':
    from twisted.internet import epollreactor
    epollreactor.install()


if __name__=="__main__":
    args = sys.argv
    name = None
    if len(args) > 1:
        name = args[1]
    else:
        raise ValueError
    import initialize
    server = FFServer()
    server.set_name(name)
    server.set_config()
    server.start()
