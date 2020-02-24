# Shared variables between threads
from threading import Thread

class OutputFrame:
    def __init__(self, height, width):
        self.frame = None
        self.boxes = ()

# Global shared variables
# an instace of this class share variables between system threads
class Shared_Variables():

    _initialized = 0

    running_status_list = list()
    category_index = None
    OutputFrame_list = list() #see class above
    number_of_persons = 0
    image_of_detections = list()

    def __init__(self, name=None, amount= 1):
        Thread.__init__(self)
        self.name = name
        for i in range(amount):
            self.running_status_list.append(True)
        self._initialized = 1
