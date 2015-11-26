# Send UDP broadcast packets

MYPORT = 50000

import sys, time
from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while 1:
    #data = repr(time.time()) + '\n'
    data = "0"*100
    data= data.decode('hex')
    s.sendto(data, ('<broadcast>', MYPORT))
    print data
    time.sleep(1)
