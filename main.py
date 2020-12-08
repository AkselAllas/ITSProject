#!/usr/bin/env python3
import time
import cv2
import threading
import sys
import logging
import tiny_yolo
import tiny_yolo.video_class
import tiny_yolo.yolo_update

logging.basicConfig(level=logging.DEBUG)

from pyardrone import ARDrone
from pyardrone import at
from pyardrone.video import VideoClient
from contextlib import suppress

def playVideo(drone):
    while True:
        cv2.imshow('im', drone.frame)
        if cv2.waitKey(10) == ord(' '):
            break

def recordVideo(drone):  
    while True:
        out.write(drone.frame)

def printMetadata(drone):
    while True:
        print(drone.navdata.metadata)

def printNavdata(drone):
    while True:
        print(drone.navdata)

def printState(drone):
    while True:
        print(drone.state)

def printFrameSize(drone):
    while True:
        print(drone.frame.size())

def hoverDrone(drone):
    while not drone.state.fly_mask:
        drone.takeoff()
    time.sleep(2)
    t_end = time.time() + 3
    while time.time() < t_end:
        drone.move(forward=0.15)
    time.sleep(3)
    while drone.state.fly_mask:
        drone.land()

drone = ARDrone()
# drone.send(at.CONFIG("video:video_codec", "131")) # Livestream 720p w/ hw encoder, no record
# time.sleep(2) # Let the Drone accept the config first
drone.navdata_ready.wait()
drone.video_ready.wait()

#yolo preparation
config = 'yolov3.cfg'
weights = 'yolov3.weights'
net, background = tiny_yolo.yolo_update.init_yolo(config, weights)
video = tiny_yolo.video_class.VideoHandler(src='vid.mp4')

i = 0
fps = 0
cv2.namedWindow('Detection and tracking')

time_s = time.time()

try:
    # threading.Thread(target=recordVideo, args=(drone,)).start()
    # navThread = threading.Thread(target=printNavdata, args=(drone,)).start()
    threading.Thread(target=hoverDrone, args=(drone,)).start()
    # out = cv2.VideoWriter('record-cup.mp4', 0x7634706d, 30.0, (640,360))
    with suppress(KeyboardInterrupt):
        while True:
            # image = cv2.resize(image,(608,608), interpolation = cv2.INTER_AREA)


            image = drone.frame
            cv2.setWindowTitle('Detection and tracking')

            bbox = tiny_yolo.get_bounding_box(image, net, background)
            x, y, w, h = bbox

            if bbox is not None:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(image, p1, p2, (255, 0, 0), 2, 1)

            #Control drone
            if (w>180):
                drone.move(backward=0.5)
            else:
                if not drone.state.fly_mask:
                    drone.takeoff()
                t_end = time_s + 3
                if time.time() < t_end:
                    drone.move(forward=0.15)
                if time.time() < t_end+3:
                    drone.land()

            cv2.imshow('Detection and tracking', image)

            if cv2.waitKey(10) == ord(' '):
                break
        # out.release()
        # playVideo(drone)
        sys.exit()
finally:
    drone.close()
