import pyshark
import pandas as pd
import numpy as np

# Some constants

# In[3]:

# TOTAL_BITS = 400
TOTAL_BITS = 10000
AP_MAC = '58:6d:8f:d3:5e:70'

# ## Loading the captured packets

# In[4]:
# file = '2015-12-09_17_12_60mw_all_nightmbps.pcapng' # Big automated
file = '2015-12-09_18_33_60mw_all_night2mbps.pcapng' # ALL NIGHT!

cap = pyshark.FileCapture(file)


p_data = pd.DataFrame(columns=['Data','Data_rate','RSSI','Tx_mac','Time'])

i = 0
for pkt in cap:
    if pkt.wlan.fcs_bad == '1':
        try:
            data = pkt.data.data.replace(':','')
            data_rate = np.float16(pkt.radiotap.datarate)
            rssi = int(pkt.radiotap.dbm_antsignal)
            tx_mac = pkt.wlan.ta
            time_rel = pkt.frame_info.time_relative
            
            p_data.loc[i] = [data,data_rate,rssi,tx_mac,time_rel]
            i +=1
        except:
            continue


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
p_data.to_msgpack('output.msg')
# ==========

