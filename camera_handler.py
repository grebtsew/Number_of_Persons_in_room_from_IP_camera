import cv2
from threading import Thread
from shared_variables import OutputFrame

class Camera(Thread):

    IMAGE_WIDTH = 420
    IMAGE_HEIGHT = 310

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
        cap = cv2.VideoCapture(self.cam_id)
        try:
            while True:

                if(cap.isOpened()):
                    ret, frame = cap.read()
                    self.shared_variables.OutputFrame_list[self.id].frame = cv2.resize(frame,(self.IMAGE_WIDTH, self.IMAGE_HEIGHT))

        except Exception as e:
            # arlo might have failed here so close capture and restart!
            cap.close()
            self.run()
