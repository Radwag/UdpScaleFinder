import socket
import re

class RDevice:
    ip_address = ''
    port_tcp = ''
    device_type = ''
    device_name = ''
    serial_number = ''  

print('Start')
radwag_devices = [];
msg = "REQREPLY_ALL\r\n"
bytesToSend = str.encode(msg)
bufferSize = 1024
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.settimeout(5)
client.sendto(bytesToSend, ('<broadcast>', 6000))
while True:
    try:
        bytes_data, addr = client.recvfrom(1024)
        data = str(bytes_data, 'utf-8')
        device = RDevice()
        device.ip_address = re.search('(?s)(?<=<IP_ADDRESS=).*?(?=>)', data).group()
        device.port_tcp = re.search('(?s)(?<=<PORT_TCP=).*?(?=>)', data).group()
        device.device_type = re.search('(?s)(?<=<DEVICE_TYPE=).*?(?=>)', data).group()
        device.device_name = re.search('(?s)(?<=<DEVICE_NAME=).*?(?=>)', data).group()
        device.serial_number = re.search('(?s)(?<=<SERIAL_NUMBER=).*?(?=>)', data).group()
        radwag_devices.append(device)             
       
    except socket.timeout:
        break

if len(radwag_devices) != 0:
    print('Devices found: ' + str(len(radwag_devices)))    
    for device in radwag_devices:
        print("Type: {}, Name: {}, Serial Number: {}, Ip Address: {}, Port: {}".format
              (device.device_type,
               device.device_name,
               device.serial_number,
               device.ip_address,
               device.port_tcp)) 
print('Done')
       
    
    
