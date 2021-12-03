from detec_tag import Tag
import cv2
from camera import gstreamer_pipeline

tag = Tag(lower_=[65, 130, 90],upper_=[90, 255, 180])

find = False
arrive = False
att = False
b_att = False
back_stop=False

prev_sensor_left = 0
prev_sensor_right = 0

up_camera = cv2.VideoCapture(gstreamer_pipeline(sensor_id = 1, flip_method=2), cv2.CAP_GSTREAMER)

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
            error2 = tag.find_area(stats)
        except:
            find=False

        ## when find true, 
        if find == True:

            ## go to center
            try :
                go_val = tag.go_speed(error2)
                tag.area_center(error,go_val)
            except:
                ## stop
                tag.robot.stop()
                pass

        ## can't find       
        else:
            ## stop
            tag.robot.stop()
        
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

tag.robot.allstop()
tag.robot.init()
up_camera.release()