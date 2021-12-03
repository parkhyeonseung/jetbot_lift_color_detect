import time
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor



# motor4 = motor.DCMotor(pca.channels[12], pca.channels[13])
class Robot():
    def __init__(self):
        
        self.i2c = busio.I2C(SCL, SDA)

        self.pca = PCA9685(self.i2c, address=0x40)
        self.pca.frequency = 2000

        self.motor1 =  motor.DCMotor(self.pca.channels[8], self.pca.channels[9]) # right
        self.motor2 = motor.DCMotor(self.pca.channels[11], self.pca.channels[10]) # left
        self.motor_lift = motor.DCMotor(self.pca.channels[13],self.pca.channels[12] ) # 
        ##6,7

        self.motor1.decay_mode = motor.SLOW_DECAY
        self.motor2.decay_mode = motor.SLOW_DECAY
        # self.motor_lift.decay_mode = motor.SLOW_DECAY

    def motors2(self,left_val,right_val):
        if left_val >1:
            left_val = 1
        if right_val >1:
            right_val = 1
        if left_val >0:
            self.motor2.throttle = left_val#*1.082
            self.motor1.throttle = right_val
        else:
            self.motor2.throttle = left_val
            self.motor1.throttle = right_val

    def forward(self,val):
        self.motor1.throttle = val
        self.motor2.throttle = val

    def backward(self,val):
        self.motor1.throttle = -val
        self.motor2.throttle = -val

    def stay_left(self,val):         ## 제자리 회전
        self.motor1.throttle = val
        self.motor2.throttle = -val

    def stay_right(self,val):         ## 제자리 회전
        self.motor1.throttle = -val
        self.motor2.throttle = val
        
    def lift_up(self):                  ####### val > 0 : lift up
        self.motor_lift.throttle = 1

    def lift_down(self):                  ####### val > 0 : lift up
        self.motor_lift.throttle = -1

    def lift_stop(self):
        self.motor_lift.throttle = 0

    def stop(self):
        self.motor1.throttle = 0
        self.motor2.throttle = 0

    def allstop(self):
        self.motor1.throttle = 0
        self.motor2.throttle = 0
        self.motor_lift.throttle = 0

    def init(self):
        self.pca.deinit()
    
if __name__=='__main__':
    robot = Robot()
    # robot.forward(1)
    # time.sleep(5)
    
    robot.allstop()
    robot.init()
