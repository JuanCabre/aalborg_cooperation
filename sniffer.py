# Receive UDP broadcast packets

MYPORT = 50000

from socket import *
import pyshark

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', MYPORT))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while 1:
    data = s.recv(1024)
    print (data)
