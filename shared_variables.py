
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

    def __init__(self, name=None):
        Thread.__init__(self)
        self.name = name
        self._initialized = 1
