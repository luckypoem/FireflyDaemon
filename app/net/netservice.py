# coding:utf8
from firefly.server.globalobject import GlobalObject
from firefly.utils.services import CommandService
from twisted.internet import defer
from twisted.python import log


class CurrentService(CommandService):

    def callTargetSingle(self, targetKey, *args, **kw):
        self._lock.acquire()
        try:
            target = self.getTarget(0)
            if not target:
                log.err('the command '+str(targetKey)+' not Found on net service')
                return None
            if targetKey not in self.unDisplay:
                log.msg("call method %s on service[single]"%target.__name__)
            defer_data = target(targetKey, *args, **kw)
            if not defer_data:
                return None
            if isinstance(defer_data, defer.Deferred):
                return defer_data
            d = defer.Deferred()
            d.callback(defer_data)
        finally:
            self._lock.release()
        return d


wsservice = CurrentService("wsservice")
GlobalObject().server.ws.addServiceChannel(wsservice)


def wsserviceHandle(target):
    """
    net节点服务
    :param target:
    :return:
    """
    wsservice.mapTarget(target)


@wsserviceHandle
def NetForwarding_0(cmd, conn, data):
    """
    消息转发
    :param cmd:
    :param conn:
    :param data:
    :return:
    """
    clientId = conn.transport.sessionno
    # 将收到的消息返回客户端
    log.msg("clientId: %s, command: %s, msg: %s" % (clientId, cmd, data))
    GlobalObject().server.ws.pushObject(10001, str(data), [clientId])
    return None
