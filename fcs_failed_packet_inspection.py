import pyshark
import pandas as pd
import numpy as np
import timeit
import os




# Some constants

# In[3]:

# TOTAL_BITS = 400
TOTAL_BITS = 10000
AP_MAC = '58:6d:8f:d3:5e:70'


# ## Loading the captured packets

# In[4]:

# file = 'test_capture.pcapng'
# file = 'gvsp.pcapng'
# file = 'bigger test.pcapng'
# file = 'test_for_weekend.pcapng'
# file = '30-11-15_54mbps_1mw.pcapng'
# file = '2015-12-04_17_25.pcapng' # Testing automated measurements
# file = '2015-12-07_11_51.pcapng' # Test across the rooms
# file = '2015-12-09_14_36_60mw_manymbps.pcapng' # First automated test
file = '2015-12-09_17_12_60mw_all_nightmbps.pcapng' # Big automated
# file = '2015-12-09_18_33_60mw_all_night2mbps.pcapng' # ALL NIGHT!

cap = pyshark.FileCapture(file)


# ## Extracting information

# ### Filter the CRC broken packets

# We use pandas to build the data frame with some usefull columns:

# In[ ]:

# Broken data as a string
data = []
data_rate = []
rssi = []
tx_mac = []
is_broken = []
# for pkt in broken_pkts:
for pkt in cap:
    if pkt.wlan.fcs_bad == '1':
# for pkt in pkts:
        # Data
        try:
            data.append(pkt.data.data.replace(':',''))
        except(AttributeError):
            continue
        # Data rate
        try:
            data_rate.append(float(pkt.radiotap.datarate))
        except:
            data.pop()
            continue
        # RSSI
        try:
            rssi.append(int(pkt.radiotap.dbm_antsignal))
        except:
            data.pop()
            data_rate.pop()
            continue
        # Transmitter MAC Address
        try:
            tx_mac.append(pkt.wlan.ta)
        except:
            data.pop()
            data_rate.pop()
            rssi.pop()
            continue
        # CRC failed
        try:
            is_broken.append(bool(pkt.wlan.fcs_bad))
        except:
            data.pop()
            data_rate.pop()
            rssi.pop()
            tx_mac.pop()
            continue

fields={'Data':data,'Data_rate':data_rate,'RSSI':rssi,'Tx_mac':tx_mac,'Broken':is_broken}
p_data = pd.DataFrame(fields)
# ==========

# Add a column stating if the AP sent the packet
p_data['AP_pkt'] = p_data['Tx_mac'].apply(lambda x: x == '58:6d:8f:d3:5e:70')
# ==========


# Add a column with Binary Data
def str2bin(number):
    decimal_number = int(number,16)
    # Do not return the '0b' at the beginning and fill with zeroes
    return bin(decimal_number)[2:].zfill(8)

def data_to_bin(data):
    return [str2bin(data[byte : byte+2]) for byte in range(0, len(data),2)]

def bytes_to_binarray(list_of_bytes):
    temp_str = ''
    for byte in list_of_bytes:
        temp_str = temp_str + byte
    return temp_str

p_data['Data_bin'] = p_data['Data'].apply(data_to_bin)
p_data['Data_bin'] = p_data['Data_bin'].apply(bytes_to_binarray)
# ==========

# Add a column stating if the data has the right length
# p_data['Right_Length'] = p_data['Data'].apply(lambda x: len(x) == 100)
p_data['Right_Length'] = p_data['Data_bin'].apply(lambda x: len(x) == TOTAL_BITS)
# ==========

# Add column with number of bits flipped
p_data['Flipped_bits'] = p_data['Data_bin'].apply(lambda x: x.count('1'))
# ==========

# Save DF
p_data.to_msgpack('test.msg')
# ==========

