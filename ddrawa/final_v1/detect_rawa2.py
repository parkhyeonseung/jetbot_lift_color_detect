########### find tag and detect then go there, and stop use attitude########################################
import cv2
from camera import gstreamer_pipeline
from detec_tag import Tag
import time
from gpio import IO
import socket
#############################################################################################################
lower_blue1 = [100, 190, 140]
upper_blue1 = [120, 255, 200]
# lower_blue1 = [100, 160, 140]
# upper_blue1 = [120, 255, 255]

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

local_ip = '192.168.16.12'
rawa_ip = '10.1.1.3'

### passing #################################################
tag.robot.motors2(0.4,0.4)
while True:
    try:
        sensor_left = io.sensor('left')
        sensor_right = io.sensor('right')
        if (prev_sensor_left!=sensor_left) or (prev_sensor_right!=sensor_right):
            if (prev_sensor_right==1) and (prev_sensor_left==1):
                break

        if sensor_left ==1:
            if prev_sensor_left!=1:
                prev_sensor_left =sensor_left
                
        if sensor_right ==1:
            if prev_sensor_right!=1:
                prev_sensor_right = sensor_right
                
        time.sleep(0.05)
    except KeyboardInterrupt:
        break

    except :
        pass
#######################################################################

######## 1st line passing send to ddaraga #########################################################
sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
sender.sendto(str.encode('pass'),('192.168.16.21',1777))
####################################################################################3

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
print('misson ready')
sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
sender.sendto(str.encode('stop rawa'),(local_ip,5555))

receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.bind((rawa_ip,7778))

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
tag.robot.motors2(-0.4,0.4)
time.sleep(0.5)
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
        # cv2.waitKey(1)
        # cv2.imshow('a',frame)
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
print('lift ready')
#### lift ready key input#################################################
sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
sender.sendto(str.encode('lift rawa'),(local_ip,5555))

receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.bind((rawa_ip,7778))

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
# sender.sendto(str.encode('lift ready'),('192.168.16.21',1777))
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
sender.sendto(str.encode('back rawa'),(local_ip,5555))

receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.bind((rawa_ip,7778))

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
# sender.sendto(str.encode('back ready'),('192.168.16.21',1777))
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
sender.sendto(str.encode('turn rawa'),(local_ip,5555))

receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.bind((rawa_ip,7778))

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
# sender.sendto(str.encode('turn ready'),('192.168.16.21',1777))
##################################################################################

#### turn 90########################################################
tag.robot.stay_right(0.4)
time.sleep(0.85)
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
sender.sendto(str.encode('go rawa'),(local_ip,5555))

receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.bind((rawa_ip,7778))

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
# sender.sendto(str.encode('go ready'),('192.168.16.21',1777))
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
