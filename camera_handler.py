import cv2
from threading import Thread
from shared_variables import OutputFrame
import time
import numpy as np

class Camera(Thread):

    IMAGE_WIDTH = 420
    IMAGE_HEIGHT = 310
    MAX_FAILED_CAPTURES = 10

    STREAM_FAIL_COUNTER = 0

    def __init__(self,cam_id, DETECTION_OPTIMIZE_SIZE, name=None, id = 0, shared_variables = None, ):
        Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        self.cam_id = cam_id;
        self.id = id;
        if DETECTION_OPTIMIZE_SIZE:
            self.IMAGE_WIDTH = DETECTION_OPTIMIZE_SIZE[0]
            self.IMAGE_HEIGHT = DETECTION_OPTIMIZE_SIZE[1]

        # Create first outputFrame
        self.shared_variables.OutputFrame_list.append(OutputFrame(self.IMAGE_HEIGHT, self.IMAGE_WIDTH))
        start_frame = np.zeros(shape=[self.IMAGE_WIDTH, self.IMAGE_HEIGHT, 3], dtype=np.uint8) # this will create a start frame
        cv2.putText(start_frame, "Camera "+str(self.id) +" is loading..." , (10,300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2, cv2.LINE_AA)
        self.shared_variables.OutputFrame_list[self.id].frame =start_frame

    def run(self):
        test_counter = 0
        try:
            cap = cv2.VideoCapture(self.cam_id)
        except Exception as e:

            print("Failed to capture camera " + str(self.cam_id) + " will retry in 2 seconds")
            time.sleep(2)
            test_counter+=1
            if test_counter > self.MAX_FAILED_CAPTURES:
                print("Failed captures has exceided the MAX FAILED CAPTURES treshhold, will now stop trying to connect to: "+ str(self.cam_id))
            else:
                self.run()
        try:
            while self.shared_variables.running_status_list[self.id]:

                if(cap.isOpened()):
                    ret, frame = cap.read()
                    self.shared_variables.OutputFrame_list[self.id].frame = frame

        except Exception as e:
            # arlo might have failed here so close capture and restart!
            time.sleep(10)
            STREAM_FAIL_COUNTER+=1
            if STREAM_FAIL_COUNTER > MAX_FAILED_CAPTURES:
                self.shared_variables.running_status_list[self.id] = False # stop instance
                print("Shuting down camera stream of instance " + str(self.id))
            else:
                self.run()
