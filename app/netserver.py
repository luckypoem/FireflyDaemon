# coding: utf8
from firefly.server.globalobject import GlobalObject
from twisted.python import log
from test import write_log


def doWhenStop():
    """
    服务器关闭前的处理
    :return:
    """
    log.msg("****    The [net] server is shut down ...    ****")
    write_log("net")


GlobalObject().stophandler = doWhenStop