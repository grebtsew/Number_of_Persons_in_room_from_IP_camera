
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

    category_index = None
    OutputFrame_list = list()
    number_of_persons = 0

    image_of_detections = list() # [[img id1....],[img id2...] ]

    def __init__(self, name=None, amount= 1):
        Thread.__init__(self)
        self.name = name
        self._initialized = 1
