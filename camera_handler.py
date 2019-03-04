import cv2
from threading import Thread
from shared_variables import OutputFrame

class Web_Camera(Thread):

    IMAGE_WIDTH = 420
    IMAGE_HEIGHT = 310

    def __init__(self, name=None, id = 0, cam_id = 0, shared_variables = None):
        Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        self.cam_id = cam_id;
        self.id = id;
        # Create first outputFrame
        self.shared_variables.OutputFrame_list.append(OutputFrame(self.IMAGE_HEIGHT, self.IMAGE_WIDTH))


    def run(self):
        cap = cv2.VideoCapture(self.cam_id)
        while True:

            if(cap.isOpened()):

                ret, frame = cap.read()
                self.shared_variables.OutputFrame_list[self.id].frame = cv2.resize(frame,(self.IMAGE_WIDTH, self.IMAGE_HEIGHT))




class Ip_Camera(Thread):

    IMAGE_WIDTH = 420
    IMAGE_HEIGHT = 310

    def __init__(self, name=None, id = 0, address = "rtsp://admin:modusproject@192.168.0.202:554/h264_vga.sdp", shared_variables = None):
        Thread.__init__(self)
        self.name = name
        self.id = id
        self.address = address
        self.shared_variables = shared_variables


        # Create first outputFrame
        self.shared_variables.OutputFrame_list.append(OutputFrame(self.IMAGE_HEIGHT, self.IMAGE_WIDTH))

    def run(self):
        cap = cv2.VideoCapture(self.address)

        try:
            while True:

                if(cap.isOpened()):
                    ret, frame = cap.read()
                    self.shared_variables.OutputFrame_list[self.id].frame = cv2.resize(frame,(self.IMAGE_WIDTH, self.IMAGE_HEIGHT))

        except:
            # arlo might have failed here so close capture and restart!
            cap.close()
            self.run()
