import cv2
from threading import Thread
from utils import visualization_utils as vis_util
import numpy as np
import time

class Vizualise_Detections(Thread):

    def __init__(self, name=None, shared_variables = None):
        Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables

    def run(self):
        while True:
            if self.shared_variables.image_of_detections is not None:
                image = None
                k = 0
                for list in self.shared_variables.image_of_detections:
                    for img in list:
                        if img is not None:
                            cv2.imshow("detect"+str(k), img)
                            k+=1
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                return
                time.sleep(1)

        cv2.destroyAllWindows()
