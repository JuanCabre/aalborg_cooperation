# Send UDP broadcast packets

import sys, time, array, os
from socket import *

rates = ['1', '2', '5.5', '6', '9', '11', '12', '18', '24', '36', '48', '54']
rates_i = 0
MYPORT = 53524
# dest_ip = '<broadcast>'
# My pc
# dest_ip = '192.168.1.124'
# Measurements PC
dest_ip = '192.168.1.130'
data = "0"*2500 # n/2 * 8 [bits] in total

def change_ap_rate ():
    global rates_i
    global rates
    rate = rates[rates_i]
    command = 'ssh root@192.168.1.1 \'wl rate ' + rate + '\''
    os.popen(command)
    print ('Changing rate to {}Mbps'.format(rate) + ' using the following command '  + command)
    # Increase the index for the next function call
    rates_i += 1
    if rates_i >= len(rates):
        rates_i = 0

# Check if n minute passed
def has_minutes_passed(oldepoch,n):
    return time.time() - oldepoch >= n*60

def main():
    # Initialize the rate to 1 Mbps
    change_ap_rate()
    pkts_sent = 0
    oldepoch = time.time()
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    global data
    data= data.decode('hex')

    while 1:
        s.sendto(data, (dest_ip, MYPORT))
        pkts_sent += 1
        #print data
        # 5 minutes passed
        if (has_minutes_passed(oldepoch,5)):
            oldepoch = time.time()
            print (pkts_sent)
            pkts_sent = 0
            change_ap_rate()

        time.sleep(0.05)
        #break

if __name__ == "__main__":
    main()
