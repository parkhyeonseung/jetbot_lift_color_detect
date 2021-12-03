import socket

local_ip = '192.168.16.12'
local_port = 5555

bot_ip = '192.168.16.21'
bot1_port = 1777
bot2_port = 2777

receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.bind((local_ip,local_port))
sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
stop_raga = False
stop_rawa = False
while True:

    bytepair = receiver.recvfrom(1024)

    message = bytepair[0].decode('utf-8')
    
    if message =='test rawa':
        stop_rawa = True
    if message == 'test raga':
        stop_raga = True
    if (stop_rawa ==True) and (stop_raga == True):
        sender.sendto(str.encode('good'),(bot_ip,bot1_port))
        sender.sendto(str.encode('good'),(bot_ip,bot2_port))
        print('step')
        stop_raga = False
        stop_rawa = False