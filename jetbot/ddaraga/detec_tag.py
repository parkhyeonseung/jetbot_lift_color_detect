import cv2
import numpy as np
from motor import Robot
import time
import socket


class Tag(Robot):

    def __init__(self,lower_= [100, 160, 100],upper_= [120, 255, 150],forward_vel = 0.3,tuning_val = 0.3):
        self.lower_ = np.array(lower_)
        self.upper_= np.array(upper_)
        self.low = 50
        self.high = 150
        self.kernel = np.ones((2, 2), np.uint8)
        self.frame_w = 224

        self.tuning_factor = 0.0035
        self.forward_vel = forward_vel 
        self.tuning_val = tuning_val
        self.robot = Robot()
        self.robot.motor1.throttle = 0
        self.robot.motor2.throttle = 0

        self.i_val = 0
        self.error_prev = 0
        self.time_prev = 0
        
        self.areas = []

    def attitude(self,sensor_left,sensor_right):
        
        if (sensor_right==0) and (sensor_left==0) :
            self.robot.motors2(0.3,0.3)
            att =False
        if (sensor_left==1) or (sensor_right==1) :
            self.robot.stop()
            if (sensor_left ==1) and (sensor_right==0):
                self.robot.stay_left(0.45)
                att =False
            elif (sensor_right ==1) and (sensor_left ==0):
                self.robot.stay_right(0.45)
                att =False

        if (sensor_left ==1) and (sensor_right ==1):
            self.robot.stop()
            att =True
        return att

    def attitude_back(self,sensor_left,sensor_right):
        if (sensor_right==0) and (sensor_left==0) :
            self.robot.motors2(-0.3,-0.3)
            b_att =False
        if (sensor_left==1) or (sensor_right==1) :
            self.robot.stop()
            if (sensor_left ==1) and (sensor_right==0):
                self.robot.motors2(0,-0.5)
                b_att =False
            elif (sensor_right ==1) and (sensor_left ==0):
                self.robot.motors2(-0.5,0)
                b_att =False

        if (sensor_left ==1) and (sensor_right ==1):
            self.robot.stop()
            b_att =True
        return b_att

    def attitude_turn(self,sensor_left,sensor_right):
        if (sensor_right==0) and (sensor_left==0) :
            self.robot.stay_right(0.4)
            t_att =False
        if (sensor_left==1) or (sensor_right==1) :
            self.robot.stop()
            if (sensor_left ==1) and (sensor_right==0):
                self.robot.stay_right(0.4)
                t_att =False
            elif (sensor_right ==1) and (sensor_left ==0):
                self.robot.stay_left(0.4)
                t_att =False

        if (sensor_left ==1) and (sensor_right ==1):
            self.robot.stop()
            t_att =True
        return t_att

    def find_color(self,frame):
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        img_mask = cv2.inRange(img_hsv, self.lower_, self.upper_)
        img_mask = cv2.dilate(img_mask, np.ones((3, 3), np.uint8), iterations=3)
        img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, self.kernel)
        img_result = cv2.bitwise_and(frame, frame, mask=img_mask)
        gray = cv2.cvtColor(img_result, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (0, 0), 1)
        img_canny = cv2.Canny(blurred, self.low, self.high)
        edge = cv2.bitwise_not(img_canny)
        return edge

    def find_contour(self,edge):
        contours, _ = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            cv2.drawContours(edge, [cnt], 0, (0, 255, 255), 1)
        _, _, stats, centroids = cv2.connectedComponentsWithStats(edge)
        return stats,centroids

    def find_tag(self,frame,stats,centroids):
        max_area = np.max(stats[2:][:,4])
        max_index = np.argmax(max_area)+2
        if max_area >300: 
            self.areas.append(max_area)
            center_x = int(centroids[max_index][0])
            center_y = int(centroids[max_index][1])
            cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)
            center = center_x
            error = self.frame_w/2 - center
            find = True
            if max_area > 10000:
                arrive = True
            else :
                arrive = False
        else :
            find = False
        return error, find, arrive , self.areas

    def find_area(self,stats):
        max_area = np.max(stats[2:][:,4])
        if max_area >100: 
            self.areas.append(max_area)
            error = 3500 - max_area

        return error

    def pid(self,error,kp=0.005,ki=0.0001,kd=0.0002):
        self.de = error-self.error_prev
        self.dt = time.time()-self.time_prev
        out = kp*error + ki*error*self.dt + kd*(self.de/self.dt)
        out = abs(out)
        self.error_prev = error
        self.time_prev = time.time()
        if out >=1:
            out =0
        return out

    def pid2(self,error,kp=0.000015,ki=0.0000008,kd=0.0000005):
        self.de = error-self.error_prev
        self.dt = time.time()-self.time_prev
        out = kp*error + ki*error*self.dt + kd*(self.de/self.dt)
        out = abs(out)
        self.error_prev = error
        self.time_prev = time.time()
        if 1<=out or -1>=out :
            out =1
        return out

    def go_center(self,error):
        out = self.pid(error)
        if error > 5: # If center point is located left to center -10
            # print("Turn left")
            turn_value = out
            if turn_value >1.0:
                turn_value = 1
            turn_value = round(turn_value,4)

            self.robot.motors2(self.forward_vel,self.forward_vel+turn_value)

        elif error <-5: # If center point is located right to center +10
            # print("Turn right")
            turn_value = out
            if turn_value >1.0:
                turn_value = 1
            turn_value = round(turn_value,4)

            self.robot.motors2(self.forward_vel+turn_value,self.forward_vel)

        elif -5<=error<=5:
            self.robot.forward(self.forward_vel)
            
        else :
            self.robot.stay_left(self.tuning_val)
            
        return 

    def area_center(self,error,go_val):
        out = self.pid(error,kp=0.00000001,ki=0.0000000002,kd=0.000000002)
        if error > 5: # If center point is located left to center -10
            # print("Turn left")
            turn_value = out
            if turn_value >1.0:
                turn_value = 1
            turn_value = round(turn_value,4)
            if go_val<-0.2:
                go_val = -0.2
            # print('left',turn_value)
            # print('go',go_val)
            self.robot.motors2(0.3+go_val,0.3+go_val+turn_value)

        elif error <-5: # If center point is located right to center +10
            # print("Turn right")
            turn_value = out
            if turn_value >1.0:
                turn_value = 1
            turn_value = round(turn_value,4)
            if go_val<-0.2:
                go_val = -0.2
            # print('right',turn_value)
            # print('go',go_val)
            self.robot.motors2(0.3+go_val+turn_value,0.3+go_val)

        elif -5<=error<=5:
            if go_val<-0.2:
                go_val = -0.2
            self.robot.motors2(0.3+go_val,0.3+go_val)
            
        else :
            self.robot.stop()
            sender = socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)
            sender.sendto(str.encode('stop'),('10.1.1.7',7778))
            
        return 

    def go_speed(self,error):
        go_value = self.pid2(abs(error))
        # print(go_value)
        if 0<error:
            pass
        if error<0:
            go_value = -go_value
        go_value = round(go_value,4) 
            
        return go_value
