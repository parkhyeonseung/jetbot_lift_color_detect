import Jetson.GPIO as GPIO

class IO():

    GPIO.setmode(GPIO.TEGRA_SOC)

    ### switch
    GPIO.setup('UART2_RTS', GPIO.IN)  #down
    GPIO.setup('DAP4_SCLK', GPIO.IN)  # up

    ### sensor ## turnoff : 1
    GPIO.setup('UART2_CTS', GPIO.IN)   #right 
    GPIO.setup('DAP4_DIN', GPIO.IN)   #left  
    
    def __init__(self):
        

        self.sensor_val = 0

        self.lift_val = 0

    def sensor(self,dir):
        if dir == 'right':
            self.sensor_val = GPIO.input('UART2_CTS')
        if dir == 'left':
            self.sensor_val = GPIO.input('DAP4_DIN')
        return self.sensor_val

    def lift(self,dir):
        if dir == 'down':
            self.lift_val = GPIO.input('DAP4_SCLK')
        if dir =='up':
            self.lift_val = GPIO.input('UART2_RTS')
        return self.lift_val

    def clean():
        GPIO.cleanup()
