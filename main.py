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
from pyfiglet import Figlet
import os, re


"""
Change These Variables, some functions won't work while running in docker!
"""
source_list = [ 0] # these most be openable by cv2.VideoCapture!

# Set both these to False in order to use default image sizes
UTILIZE_ALL_MONITOR_SPACE = False # Set this to maximize visual size of all images
VISUALIZATION_OFFSET_AND_SIZE = False # If UTILIZE_ALL_MONITOR_SPACE is false, use this size instead, set to False if you want all screen to load on eachother with camera default size.
MONITOR_INDEX_LIST = False # fill this list with the index numbers of monitors to use [1 2 3]

SHOW_ALL_PERSONS = False # Decide if you want to show all cropped images of detected persons

use_arlo = False # Set to True if you want to scan for and use arlo cameras!
USERNAME = '' # for arlo login
PASSWORD = ''

DETECTION_OPTIMIZE_SIZE = [640,480] # Set size of images before prediction, Set to None if you want to use full size images


"""
----- PROGRAM CODE -----
"""
path = "/proc/" + str(os.getpid()) + "/cgroup"

def is_docker():
  if not os.path.isfile(path): return False
  with open(path) as f:
    for line in f:
      if re.match("\d+:[\w=]+:/docker(-[ce]e)?/\w+", line):
        return True
    return False

class Monitor():
    x: 0
    y: 0
    width: 0
    height: 0
    name: ""

def getParenthesis(texte):
    content = None
    p1 = texte.find('(')
    if p1 >= 0:
        p2 = texte.find(')')
        if p2 > p1:
            content = texte[p1:p2+1]
    return content

def monitorsInfo():
    import subprocess
    commande = ['xrandr','--listmonitors']
    res = subprocess.check_output(commande, shell=True).decode().split('\n')

    monitors = {}

    for l in res:
        if len(l) > 1:
            if l[0] != ' ':
                if l.split()[0] == l.split()[0].upper():

                    options = getParenthesis(l)
                    if options:
                        l = l.replace(options, '')
                    z = l.split()

                    # this is a connector
                    name = z[0]
                    conn = None
                    primary = None
                    geo = None
                    size = None
                    width = height = offsetx = offsety = None
                    if z[1].lower() == 'connected':
                        conn = True
                        # monitor in use :-)
                    else:
                        # screeen connection exists, no screen used
                        conn = False
                    # for connected screens : get extra data
                    if conn:
                        if z[2].lower() == 'primary':
                            primary = True
                            z.pop(2)
                        # other data for connected screeens
                        geo = z[2]   # get rid of extra 'primary'
                        size = ''.join(z[3:])
                        # get width and height
                        z = geo.split('+')
                        offsetx = int(z[1])
                        offsety = int(z[2])
                        z = z[0].split('x')
                        width = int(z[0])
                        height = int(z[1])


                    # create a dict per monitor
                    d = {}
                    d['name'] = name
                    d['connected'] = conn
                    d['primary'] = primary
                    d['geometry'] = geo
                    d['options'] = options
                    d['size'] = size
                    d['width'] = width
                    d['height'] = height
                    d['offsetx'] = offsetx
                    d['offsety'] = offsety

                    monitors[name] = d

    return monitors
def detect_monitors():
    if os.name == 'nt':
        from screeninfo import get_monitors
        return get_monitors()
    else:
        # Linux command
        monitor_list = []
        monitors = monitorsInfo()
        for monitor in monitors:
            if monitor["connected"]:
                #monitor exist
                monitor_list.append(Monitor(x = monitor["offsetx"], y=monitor["offsety"], width=monitor["width"], height=monitor["height"]))

def get_monitors_to_use(monitor_list, MONITOR_INDEX_LIST):
    if MONITOR_INDEX_LIST:
        res_list = []
        for i in range(0,len(monitor_list)):
            res_list.append(monitor_list[MONITOR_INDEX_LIST[i]])
    else:
        return monitor_list

def split_monitors(monitor_list, source_list):

    # This function is an algoritm for splitting up any amount of screens into even boxes.
    monitor_box_list = []
    camera_amount = len(source_list)
    monitor_list = get_monitors_to_use(monitor_list, MONITOR_INDEX_LIST)
    monitor_amount = len(monitor_list)

    cameras_per_monitor_split = list(splitlist(source_list, monitor_amount))

    for i in range(0,len(cameras_per_monitor_split)):
        if len(cameras_per_monitor_split[i]) == 1:
            cameras_on_monitor_divide = [1]
        else:
            cameras_on_monitor_divide = list(splitnum(len(cameras_per_monitor_split[i]),int(len(cameras_per_monitor_split[i])/2)))

        # Divide monitor into N boxes
        for j in range(0,len(cameras_on_monitor_divide)): # rows
            for k in range(0,cameras_on_monitor_divide[j]): # columns
                camera_width = int(monitor_list[i].width/cameras_on_monitor_divide[j])
                camera_height = int(monitor_list[i].height/len(cameras_on_monitor_divide))
                x= monitor_list[i].x + k*camera_width
                y= monitor_list[i].y + j*camera_height

                if (j == 0):
                    h= y+(1+j)*camera_height
                else:
                    h= y+j*camera_height
                if (k == 0):
                    w= x+(1+k)*camera_width
                else:
                    w= x+k*camera_width

                monitor_box_list.append([x,y,w,h])

    return monitor_box_list

def splitnum(a, n):
    """
    Split numbers into even divided numbers
    """
    num, div = a, n
    return (num // div + (1 if x < num % div else 0)  for x in range (div))

def splitlist(a, n):
    """
    Simple split array into even sizes
    """
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def create_instances( source_list , monitor_list):
    '''
    Create instances of system
    @param get list of sources, int for webcams and str for rtsp
    '''
    camera_amount = len(source_list)
    shared_variables = Shared_Variables(amount = camera_amount)
    if not is_docker():
        monitor_box_list = split_monitors(monitor_list, source_list)

    # start show all detection crop images thread
    if SHOW_ALL_PERSONS:
        Vizualise_Detections(shared_variables=shared_variables).start()

    for i in range(0, camera_amount):

        # Create camera stream
        cam = Camera(id = i, cam_id=source_list[i], shared_variables=shared_variables, DETECTION_OPTIMIZE_SIZE=DETECTION_OPTIMIZE_SIZE).start()

        # Start Object detection on camera
        Obj_Detection( id = i, shared_variables=shared_variables).start()

        # Set Visualization mode
        if UTILIZE_ALL_MONITOR_SPACE:
            Vizualise(id = i, shared_variables=shared_variables, pos = monitor_box_list[i]).start()
        elif VISUALIZATION_OFFSET_AND_SIZE:
            Vizualise(id = i, shared_variables=shared_variables, pos = VISUALIZATION_OFFSET_AND_SIZE).start()
        else:
            Vizualise(id = i, shared_variables=shared_variables).start()


        print("Created instance ", i," with camera, detection and vizualisation.")


# Main start here
if __name__ == "__main__":
    f = Figlet(font='slant')
    print (f.renderText('Number of Persons in Room'))
    print("Please hold on while we receive cameras and start detection threads...")

    if is_docker():
        print("Running on docker!")
        UTILIZE_ALL_MONITOR_SPACE = False # Set this to maximize visual size of all images
        VISUALIZATION_OFFSET_AND_SIZE = False # If UTILIZE_ALL_MONITOR_SPACE is false, use this size instead, set to False if you want all screen to load on eachother with camera default size.
        MONITOR_INDEX_LIST = False # fill this list with the index numbers of monitors to use [1 2 3]
        monitor_list = None
    else:
        print("Collecting Monitor information...")

        print("----- Print Monitor List -----")
        monitor_list = detect_monitors()
        print(monitor_list)
        print("----- Monitor List End -----")

    print("Setting up source_list...")

    print("Adding local cameras...")

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
    create_instances(source_list, monitor_list)
