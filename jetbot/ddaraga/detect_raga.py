########### find tag and detect then go there, and stop use attitude########################################
import cv2
from camera import gstreamer_pipeline
from detec_tag import Tag
import time
from gpio import IO
import socket
#############################################################################################################
# lower_blue1 = [100, 160, 100]
# upper_blue1 = [120, 255, 150]
#light
# lower_blue1 = [100, 160, 100]
# upper_blue1 = [120, 255, 255]
#magok
lower_blue1 = [100, 140, 140]
upper_blue1 = [120, 180, 160]

io = IO()

find = False
arrive = False
att = False
b_att = False
back_stop=False

prev_sensor_left = 0
prev_sensor_right = 0

tag = Tag(lower_blue1,upper_blue1)

up_camera = cv2.VideoCapture(gstreamer_pipeline(sensor_id = 1, flip_method=2), cv2.CAP_GSTREAMER)

local_ip = '10.1.1.16'
raga_ip = '10.1.1.7'

## start ##############################################################3
receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.bind((raga_ip,7778))
print('on')
while True:
    try:
        bytepair = receiver.recvfrom(1024)
        message = bytepair[0].decode('utf-8')
        if message == 'start':
            break
    except KeyboardInterrupt:
        break
    except :
        pass
#######################################################

### sensor attitude #################################################
tag.robot.motors2(0.4,0.4)
while True:
    try:
        sensor_left = io.sensor('left')
        sensor_right = io.sensor('right')
        att = tag.attitude(sensor_left,sensor_right)
        
        if att==True:
            tag.robot.stop()
            break

    except KeyboardInterrupt:
        break
    except :
        pass
#######################################################################
print('misson ready')
sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
sender.sendto(str.encode('stop raga'),(local_ip,7778))

receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.bind((raga_ip,7778))

while True:
    try:
        bytepair = receiver.recvfrom(1024)
        message = bytepair[0].decode('utf-8')
        if message == 'misson ready':
            break
    except KeyboardInterrupt:
        break
    except :
        pass



###############################################################################################################
tag.robot.motors2(-0.45,0.45)
time.sleep(1)
while True:
    try:
        ret, frame = up_camera.read()
        frame = cv2.flip(frame,0)
        frame = cv2.flip(frame,1)
        if not ret :
            print('notopencamera')
            break

    # find color
        edge = tag.find_color(frame)

    # find contour
        stats,centroids = tag.find_contour(edge)
    
    # find property of contour that is tag we want
        try:
            error, find, arrive,areas = tag.find_tag(frame,stats,centroids)
        except:
            find=False
        
    # the robot arrive ?
        if arrive == True:
            tag.robot.stop()
            break
        else:
            pass

        ## when find true, 
        if find == True:

            ## go to center
            try :
                tag.go_center(error)
            except:
                ## stop
                tag.robot.stay_left(0.35)
                pass

        ## can't find       
        else:
            ## stop
            tag.robot.stay_left(0.35)
        
    except KeyboardInterrupt:
        break
    except :
        pass
#####################################################################

### sensor attitude #################################################
while True:
    try:
        sensor_left = io.sensor('left')
        sensor_right = io.sensor('right')
        att = tag.attitude(sensor_left,sensor_right)
        if att==True:
            tag.robot.stop()
            break

    except KeyboardInterrupt:
        break
    except :
        pass
#######################################################################

#### lift ready key input#################################################
print('lift ready')
sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
sender.sendto(str.encode('lift raga'),(local_ip,7778))

receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.bind((raga_ip,7778))

while True:
    try:
        bytepair = receiver.recvfrom(1024)
        message = bytepair[0].decode('utf-8')
        if message == 'lift ready':
            break
    except KeyboardInterrupt:
        break
    except :
        pass
# sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
# sender.sendto(str.encode('lift ready'),('192.168.16.21',2777))
# print('author')
############################################################################
    
##### lift #############################################################
tag.robot.lift_up()
while True:
    try:
        tag.robot.lift_up()
        lift_val = io.lift('up')

        if lift_val == 0:
            break
        
    except KeyboardInterrupt:
        break
    except:
        pass
#################################################################################
time.sleep(2)
#### back ready key input########################################################
print('back ready')
sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
sender.sendto(str.encode('back raga'),(local_ip,7778))

receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.bind((raga_ip,7778))

while True:
    try:
        bytepair = receiver.recvfrom(1024)
        message = bytepair[0].decode('utf-8')
        if message == 'back ready':
            break
    except KeyboardInterrupt:
        break
    except :
        pass
# sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
# sender.sendto(str.encode('back ready'),('192.168.16.21',2777))
# print('author')
##################################################################################

#### back attitude ###############################################################
tag.robot.backward(0.3)
time.sleep(2)
while True:
    try:
        sensor_left = io.sensor('left')
        sensor_right = io.sensor('right')
        b_att = tag.attitude_back(sensor_left,sensor_right)
        if b_att==True:
            tag.robot.stop()
            break

    except KeyboardInterrupt:
        break
    except :
        pass
#############################################################################

#### turn ready key input########################################################
print('turn ready')
sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
sender.sendto(str.encode('turn raga'),(local_ip,7778))

receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.bind((raga_ip,7778))
while True:
    try:
        bytepair = receiver.recvfrom(1024)
        message = bytepair[0].decode('utf-8')
        if message == 'turn ready':
            break
    except KeyboardInterrupt:
        break
    except :
        pass
# sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
# sender.sendto(str.encode('back ready'),('192.168.16.21',2777))
# print('author')
##################################################################################

#### turn 90########################################################
tag.robot.stay_right(0.45)
time.sleep(1)
tag.robot.stop()
tag.robot.motors2(0.3,0.3)
while True:
    try:
        sensor_left = io.sensor('left')
        sensor_right = io.sensor('right')
        att = tag.attitude(sensor_left,sensor_right)
        if att==True:
            tag.robot.stop()
            break

    except KeyboardInterrupt:
        break
    except :
        pass
##################################################################################

#### go ready key input########################################################
print('go ready')
sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
sender.sendto(str.encode('go raga'),(local_ip,7778))

receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.bind((raga_ip,7778))

while True:
    try:
        bytepair = receiver.recvfrom(1024)
        message = bytepair[0].decode('utf-8')
        if message == 'go ready':
            break
    except KeyboardInterrupt:
        break
    except :
        pass
# sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
# sender.sendto(str.encode('go ready'),('192.168.16.21',2777))
# print('author')
##################################################################################

##############################################################################
tag.robot.lift_down()
while True:
    try:
        tag.robot.lift_down()
        lift_val = io.lift('down')

        if lift_val == 0:
            break
        
    except KeyboardInterrupt:
        break
    except:
        pass
###################################################################################
print('liftdown')



# When everything is done, release the capture

tag.robot.allstop()
tag.robot.init()
io.clean()
up_camera.release()
