from motor import Robot
from gpio import IO

io = IO()
robot = Robot()
robot.lift_down()

while True:
    try:
        lift_val = io.lift('down')

        if lift_val == 0:
            break
        
    except KeyboardInterrupt:
        break
    except:
        pass
    
IO.clean() 
robot.lift_stop()
robot.init()
