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
    
    if message =='stop rawa':
        stop_rawa = True
    if message == 'stop raga':
        stop_raga = True
    if (stop_rawa ==True) and (stop_raga == True):
        sender.sendto(str.encode('misson ready'),(bot_ip,bot1_port))
        sender.sendto(str.encode('misson ready'),(bot_ip,bot2_port))
        print('step')
        stop_raga = False
        stop_rawa = False
    
    if message =='lift rawa':
        stop_rawa = True
    if message == 'lift raga':
        stop_raga = True
    if (stop_rawa ==True) and (stop_raga == True):
        sender.sendto(str.encode('lift ready'),(bot_ip,bot1_port))
        sender.sendto(str.encode('lift ready'),(bot_ip,bot2_port))
        print('step')
        stop_raga = False
        stop_rawa = False

    if message =='back rawa':
        stop_rawa = True
    if message == 'back raga':
        stop_raga = True
    if (stop_rawa ==True) and (stop_raga == True):
        sender.sendto(str.encode('back ready'),(bot_ip,bot1_port))
        sender.sendto(str.encode('back ready'),(bot_ip,bot2_port))
        print('step')
        stop_raga = False
        stop_rawa = False

    if message =='turn rawa':
        stop_rawa = True
    if message == 'turn raga':
        stop_raga = True
    if (stop_rawa ==True) and (stop_raga == True):
        sender.sendto(str.encode('turn ready'),(bot_ip,bot1_port))
        sender.sendto(str.encode('turn ready'),(bot_ip,bot2_port))
        print('step')
        stop_raga = False
        stop_rawa = False

    if message =='go rawa':
        stop_rawa = True
    if message == 'go raga':
        stop_raga = True
    if (stop_rawa ==True) and (stop_raga == True):
        sender.sendto(str.encode('go ready'),(bot_ip,bot1_port))
        sender.sendto(str.encode('go ready'),(bot_ip,bot2_port))
        print('step')
        stop_raga = False
        stop_rawa = False

