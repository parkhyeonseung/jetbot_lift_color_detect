import socket

local_ip = '192.168.16.12'
rawa_ip = '10.1.1.3'

sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
sender.sendto(str.encode('test rawa'),(local_ip,5555))

receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.bind((rawa_ip,7778))

while True:
    try:
        bytepair = receiver.recvfrom(1024)
        message = bytepair[0].decode('utf-8')
        if message == 'good':
            print('good')
            break
    except KeyboardInterrupt:
        break
    except :
        pass