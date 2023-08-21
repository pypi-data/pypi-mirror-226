import struct
import socket

from .serializer import Encoding, Serializer

import socket

class SocketSerializer(Serializer):
    def __init__(self, connection):
        self._conn = connection

    """
    Set a timeout on blocking socket operations. 
    
    The value argument can be a nonnegative floating point number expressing seconds, or None. 
    If a non-zero value is given, subsequent socket operations will raise a timeout exception if the timeout period value has elapsed before the operation has completed. 
    If zero is given, the socket is put in non-blocking mode. 
    If None is given, the socket is put in blocking mode.
    """
    def setReceiveTimeout(self, timeout):
        self._conn.settimeout(timeout)

    def _receive(self, size, timeout=None):
        try:
            data = self._conn.recv(size)
            return data
        except TimeoutError:
            return b""
    
    def _transmit(self, data, size):
        self._conn.sendall(data)
