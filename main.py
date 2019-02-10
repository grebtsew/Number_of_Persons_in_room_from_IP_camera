'''
This is main function, used to start instances of the full system
'''

from shared_variables import Shared_Variables
from camera_handler import *
from vizualise import Vizualise
from vizualise_detections import Vizualise_Detections

from obj_detection import Obj_Detection
from threading import Thread

def create_instances( source_list ):
    '''
    Create instances of system
    @param get list of sources, int for webcams and str for rtsp
    '''
    amount = len(source_list)
    shared_variables = Shared_Variables(amount = amount)

    # start show all detection crop images thread
    Vizualise_Detections(shared_variables=shared_variables).start()

    for i in range(0, amount):
        if (type(source_list[i]) == type(int())):
            Web_Camera(id = i, cam_id=source_list[i], shared_variables=shared_variables).start()
        else:
            Ip_Camera(id = i, address = source_list[i], shared_variables=shared_variables).start()

        Obj_Detection( id = i, shared_variables=shared_variables).start()

        Vizualise(id = i, shared_variables=shared_variables).start()

        print("Created instance ", i," with camera, detection and vizualisation.")


# Main start here
if __name__ == "__main__":
    source_list = [0] # must be of size amount atleast!

    create_instances( source_list)
