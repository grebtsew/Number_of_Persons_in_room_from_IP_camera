# Detect and calculate number of persons in room from several IP camera in real time using Tensorflow
A multithreaded program that calculate and detect number of persons in a room from an arbitary amount of cameras with Tensorflow object detection.

<p align="center" >
  <img width="200" height="200" src="images/arlo.jpg">
  <img width="200" height="200" src="images/ip1.jpg">
</p>
<p align="center" >
<img width="200" height="200" src="images/ip2.jpg">
<img width="200" height="200" src="images/ip3.jpg">
</p>

# Install & Run
This part describe the installation and running process.

## Install Docker
Firstly install Docker on your device.

```
# Build Container
docker build . --tag=persons-in-room:1.0

# Show downloaded & built images
docker images
```

## Run Docker (Windows)
Now we need to install a xLauncher for windows in order to allow docker to use a gui.

I recommend installing vcxsrv.

Useful and intresting tutorial on this subject:
https://dev.to/darksmile92/run-gui-app-in-linux-docker-container-on-windows-host-4kde

When a xLauncher is installed run the container with the following command:
```
docker run -ti --rm -e DISPLAY=127.0.0.1:0.0 persons-in-room:1.0 bash
```

## Run Docker (Linux/Ubuntu)
This all is a little more simple on linux. Run the following command:
```
docker run -ti --rm -e DISPLAY=127.0.0.1:0.0 -v /tmp/.X11-unix:/tmp/.X11-unix persons-in-room:1.0 bash
```
Useful link:
https://linoxide.com/linux-how-to/run-gui-apps-docker-container/

## Install Program locally
Here we describe how to install the implementation on your local computer.

1. Install python

2. Install required packages
```
pip3 install -r requirements.txt
```
3. Done!

## Run Program locally
1. Change variables in "main.py".
2. Run main.py:
```
python3 main.py
```

# What exactly does this program do?
Here we describe what this implementation actually does!

## Multithreading and OpenCV
This implementation uses multithreading for async tasks such as receiving and handling Camera streams.
OpenCV is used to collect and visualize the streams.

## Auto Screen Splitting
This implementation also contains a auto screen splitter. Letting you add an arbitary amount of cameras in the
source_list. The camera streams will be evenly shared among all screen connected to the computer.

## Tensorflow Object Detection
A simple tensorflow object detection is used. It is a faster-rcnn trained on the COCO-dataset.
All models needed to run the implementation is in this repo, all used models is provided by Google developer team.

## Image Difference Calculations
To decide if a person has already been detected we use an image template probability match method to detect image differences.
This method is mainly used to make sure that a person is not calculated several times when seen from several cameras at once.

## The System Structure

<p align="center" >
  <img width="400" height="400" src="images/NumberOfPersonsInRoom.png">
</p>

# Contributions
The code for object detection assume from:
 https://github.com/jamesloyys/Real-Time-Object-Detection.git
