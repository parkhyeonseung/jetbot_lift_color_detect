# TensorFlow and tf.keras
import tensorflow as tf
import numpy as np
import cv2
from camera import gstreamer_pipeline
from gpio import IO
from detec_tag import Tag
import time
# Load TFLite model and allocate tensors.
#interpreter = tf.lite.Interpreter(model_path="./saved_model/my_model.quant.tflite")
interpreter = tf.lite.Interpreter(model_path="./new_new_12_05_10_0.tflite")
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
# Test model on random input data.
input_shape = input_details[0]['shape']
# robot = Robot()
tag = Tag()
io = IO()
cap_down = cv2.VideoCapture(gstreamer_pipeline(sensor_id = 0, flip_method = 0), cv2.CAP_GSTREAMER)
#input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
# input_data = np.array(np.random.randint(0,1000, size=input_shape), dtype=np.float32)
while True:
    left_val = 0.33
    right_val = 0.4
    # left_val = 0.4
    # right_val = 0.4
    ret, frame = cap_down.read()
    if ret:
        try:
            #input_data = np.array([[1]], dtype=np.float32)
            # print("input : %s" % input_data)
            input_data = frame.copy()
            input_data = input_data.astype(np.float32)
            input_data = cv2.resize(input_data, (224,224))
            input_data = np.expand_dims(input_data, axis=0)
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            # The function `get_tensor()` returns a copy of the tensor data.
            # Use `tensor()` in order to get a pointer to the tensor.
            output_data = interpreter.get_tensor(output_details[0]['index'])
            # print(output_data)
            res = np.argmax(output_data)
            rate = output_data[0][res]
            
            print('res', res)
            print(rate)

            sensor_left = io.sensor('left')
            sensor_right = io.sensor('right')

            if sensor_right == 1:
                tag.robot.motors2(-0.3,0.43)
                time.sleep(0.27)
            if sensor_left == 1:
                tag.robot.motors2(0.43,-0.3)
                time.sleep(0.3)
            if (sensor_right ==0)and (sensor_left==0):
                if res == 0:
                    tag.robot.motors2(left_val, right_val)
                elif res == 1:
                    tag.robot.motors2(left_val*0.33, right_val*0.98)
                    # time.sleep(0.05)
                elif res == 2:
                    tag.robot.motors2(left_val*0.84, right_val*0.33)
                    # time.sleep(0.05)
            frame = cv2.flip(frame,0)
            frame = cv2.flip(frame,1)

            # cv2.imshow('frame',frame)
            if cv2.waitKey(1) == 27:
                break
        except KeyboardInterrupt as ke:
            break
        except Exception as e:
            print(e)
            break

cap_down.release()
tag.robot.stop()
tag.robot.init()
# cv2.destroyAllWindows()
print("프로그램 종료")
