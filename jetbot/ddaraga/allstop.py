from gpio import IO
from detec_tag import Tag
from camera import gstreamer_pipeline
import cv2

cap_down = cv2.VideoCapture(gstreamer_pipeline(flip_method=0,sensor_id=0), cv2.CAP_GSTREAMER)
cap_up = cv2.VideoCapture(gstreamer_pipeline(sensor_id = 1, flip_method=0), cv2.CAP_GSTREAMER)

tag =Tag()
io = IO()

cap_down.release()
cap_up.release()

tag.robot.allstop()
tag.robot.init()
io.clean()