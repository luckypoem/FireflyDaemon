# coding: utf8
from firefly.netconnect.datapack import DataPackError
from twisted.python import log
import struct


class DataPackProtoc:
    """数据包协议
    """
    def __init__(self):
        self.header = 8

    def getHeadlength(self):
        """获取数据包的长度
        """
        return self.header

    def unpack(self, dpack):
        '''解包
        '''
        try:
            length, command = struct.unpack('!2I', dpack)
        except DataPackError, de:
            log.err(de)
            return {'result': False, 'command': 0, 'length': 0}
        return {'result': True, 'command': command, 'length': length}

    def pack(self, response, command):
        '''打包数据包
        '''
        length = response.__len__()
        data = struct.pack('!2I', length, command)
        print len(data + response)
        return data + response


