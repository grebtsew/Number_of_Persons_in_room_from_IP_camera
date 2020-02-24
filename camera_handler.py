import cv2
from threading import Thread
from shared_variables import OutputFrame
import time

class Camera(Thread):

    IMAGE_WIDTH = 420
    IMAGE_HEIGHT = 310
    MAX_FAILED_CAPTURES = 10
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
            while True:

                if(cap.isOpened()):
                    ret, frame = cap.read()
                    self.shared_variables.OutputFrame_list[self.id].frame = cv2.resize(frame,(self.IMAGE_WIDTH, self.IMAGE_HEIGHT))

        except Exception as e:
            # arlo might have failed here so close capture and restart!
            cap.close()
            self.run()
