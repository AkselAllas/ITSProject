import time
import cv2
import logging

logging.basicConfig(level=logging.DEBUG)

from pyardrone import ARDrone
from pyardrone.video import VideoClient
from contextlib import suppress

drone = ARDrone()
drone.navdata_ready.wait()  # wait until NavData is ready
with suppress(KeyboardInterrupt):
    while True:
        print(drone.state)

drone.video_ready.wait()
try:
    while True:
        cv2.imshow('im', drone.frame)
        if cv2.waitKey(10) == ord(' '):
            break
finally:
    drone.close()

#while not drone.state.fly_mask:
    #drone.takeoff()

#time.sleep(20)              # hover for a while

#while drone.state.fly_mask:
    #drone.land()