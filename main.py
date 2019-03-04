'''
This is main function, used to start instances of the full system
'''
from arlo import Arlo
from subprocess import call
from shared_variables import Shared_Variables
from camera_handler import *
from vizualise import Vizualise
from vizualise_detections import Vizualise_Detections
from obj_detection import Obj_Detection
from threading import Thread


USERNAME = '' # for arlo login
PASSWORD = ''

show_on_other_monitor = False
use_arlo = False
MONITOR_WIDTH = 1920;
MONITOR_HEIGHT = 700;
MONITOR_OFFSET = 100;

def create_instances( source_list ):
    '''
    Create instances of system
    @param get list of sources, int for webcams and str for rtsp
    '''
    amount = len(source_list)
    shared_variables = Shared_Variables(amount = amount)

    # start show all detection crop images thread
    Vizualise_Detections(shared_variables=shared_variables).start()

    image_new_line = 0
    image_new_column = 0

    for i in range(0, amount):
        if (type(source_list[i]) == type(int())):

            cam = Web_Camera(id = i, cam_id=source_list[i], shared_variables=shared_variables).start()
        else:
            cam = Ip_Camera(id = i, address = source_list[i], shared_variables=shared_variables).start()

        Obj_Detection( id = i, shared_variables=shared_variables).start()

        if show_on_other_monitor:
            if image_new_column*(cam.IMAGE_WIDTH*2) - MONITOR_WIDTH > 0: # new line out of screensize

                image_new_line+=1
                image_new_column= 0

            Vizualise(id = i, shared_variables=shared_variables, pos = [image_new_column*cam.IMAGE_WIDTH-MONITOR_WIDTH, MONITOR_OFFSET + image_new_line*MONITOR_HEIGHT/2 ]).start()
        else:
            Vizualise(id = i, shared_variables=shared_variables).start()

        print("Created instance ", i," with camera, detection and vizualisation.")

        image_new_column += 1


# Main start here
if __name__ == "__main__":
    print("Starting Program: Number of Persons in Room")
    print("Please hold on while we recieve cameras and start detection threads...")

    print("Setting up source_list...")

    print("Adding local cameras...")
    source_list = [ 0]
    if use_arlo:
        print("Waiting for Arlo cameras...")
        try:

            # Instantiating the Arlo object automatically calls Login(),
            # which returns an oAuth token that gets cached.
            # Subsequent successful calls to login will update the oAuth token.
            arlo = Arlo(USERNAME, PASSWORD)
            # At this point you're logged into Arlo.

            # Get the list of devices and filter on device type to only get the cameras.
            # This will return an array which includes all of the canera's associated metadata.
            cameras = arlo.GetDevices('camera')

            # Get the list of devices and filter on device type to only get the basestation.
            # This will return an array which includes all of the basestation's associated metadata.
            basestations = arlo.GetDevices('basestation')

            # Open the event stream to act as a keep-alive for our stream.
            arlo.Subscribe(basestations[0])

            # Send the command to start the stream and return the stream url.
            #url = arlo.StartStream(basestations[0], cameras[0])

            i = 0

            for cam in cameras:
                url = arlo.StartStream(basestations[0], cameras[i])
                source_list.append(url)

                i+=1

        except Exception as e:
            print(e)

    print("Done with collecting cameras...")
    print("----- Print source list -----")
    for address in source_list:
        print(address)
    print("----- Source list end -----")

    print("Creating all instances... this might take a while!")
    create_instances( source_list)
