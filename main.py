#!/usr/bin/env python3
import time
import cv2
import threading
import sys
import logging

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

try:
    # threading.Thread(target=recordVideo, args=(drone,)).start()
    # navThread = threading.Thread(target=printNavdata, args=(drone,)).start()
    threading.Thread(target=hoverDrone, args=(drone,)).start()
    # out = cv2.VideoWriter('record-cup.mp4', 0x7634706d, 30.0, (640,360))
    with suppress(KeyboardInterrupt):
        while True:
            # out.write(drone.frame)
            cv2.imshow('im', drone.frame)
            if cv2.waitKey(10) == ord(' '):
                break
        # out.release()
        # playVideo(drone)
        sys.exit()
finally:
    drone.close()