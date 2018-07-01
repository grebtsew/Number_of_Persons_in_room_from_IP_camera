import cv2
from threading import Thread
from shared_variables import OutputFrame

class Web_Camera(Thread):

    IMAGE_WIDTH = 640
    IMAGE_HEIGHT = 480

    def __init__(self, name=None, shared_variables = None):
        Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables

        # Create first outputFrame
        self.shared_variables.OutputFrame_list.append(OutputFrame(self.IMAGE_HEIGHT, self.IMAGE_WIDTH))

    def run(self):
        cap = cv2.VideoCapture(0)

        while True:

            if(cap.isOpened()):
                ret, frame = cap.read()
                self.shared_variables.OutputFrame_list[0].frame = frame


class Ip_Camera(Thread):

    IMAGE_WIDTH = 640
    IMAGE_HEIGHT = 480

    def __init__(self, name=None, shared_variables = None):
        Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables

        # Create first outputFrame
        self.shared_variables.OutputFrame_list.append(OutputFrame(self.IMAGE_HEIGHT, self.IMAGE_WIDTH))

    def run(self):
        cap = cv2.VideoCapture("rtsp://admin:modusproject@192.168.0.202:554/h264_vga.sdp")

        while True:

            if(cap.isOpened()):
                ret, frame = cap.read()

                self.shared_variables.OutputFrame_list[0].frame = frame
