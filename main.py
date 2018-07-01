from shared_variables import Shared_Variables
from camera_handler import *
from vizualise import Vizualise
from obj_detection import Obj_Detection
from threading import Thread

if __name__ == "__main__":

    shared_variables = Shared_Variables()

    print("Started Detection")
    object_detection_thread = Obj_Detection(shared_variables=shared_variables)
    object_detection_thread.start()

    print("Started cameras")
    camera_thread_1 = Web_Camera(shared_variables=shared_variables)
    camera_thread_1.start()

    print("Started vizualise")
    vis_thread = Vizualise(shared_variables=shared_variables)
    vis_thread.start()
