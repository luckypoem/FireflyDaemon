# coding: utf8
from firefly.server.globalobject import GlobalObject, webserviceHandle
from twisted.web import resource
from twisted.python import log
from firefly.utils.common import ToUtf8
from app.net.datapack import DataPackProtoc
from test import write_log


def doWhenStop():
    """
    服务器关闭前的处理
    :return:
    """
    log.msg("****    The [net] server is shut down ...    ****")
    write_log("net")


def callWhenConnLost(conn):
    """
    客户端连接断开时处理
    :param conn:
    :return:
    """
    log.msg("client %s login out" % conn.transport.sessionno)


GlobalObject().stophandler = doWhenStop

# WebSocket设置
GlobalObject().server.ws.setDataProtocl(DataPackProtoc())
GlobalObject().server.ws.doConnectionLost = callWhenConnLost


@webserviceHandle('/websocket')
class websocket(resource.Resource):

    def render(self, request):
        with open("demo/websocket.html", "r") as f:
            content = f.read()
            f.close()
        return ToUtf8(content)


import net.netservice