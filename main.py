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


def fps_calc(current_time, last_frame_shown):
    fps = round(1 / (current_time - last_frame_shown), 1)
    return fps, current_time


def add_fps(image, fps):
    cv2.putText(image, "FPS: " + str(fps), (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    return image


drone = ARDrone()
# drone.send(at.CONFIG("video:video_codec", "131")) # Livestream 720p w/ hw encoder, no record
# time.sleep(2) # Let the Drone accept the config first
drone.navdata_ready.wait()
drone.video_ready.wait()

# yolo preparation
config = 'tiny_yolo/yolov3.cfg'
weights = 'tiny_yolo/yolov3.weights'
net, background = tiny_yolo.yolo_update.init_yolo(config, weights)

fps = 0
cv2.namedWindow('Detection and tracking')
last_frame_shown = time.time()
time_s = time.time()
go_back = False

try:
    # threading.Thread(target=recordVideo, args=(drone,)).start()
    # navThread = threading.Thread(target=printNavdata, args=(drone,)).start()
    out = cv2.VideoWriter('test-flight-with-yolo-4.mp4', 0x7634706d, 2.0, (640,360))
    with suppress(KeyboardInterrupt):
        land_time = time.time() + 15
        while True:
            # image = cv2.resize(image,(608,608), interpolation = cv2.INTER_AREA)
            if not drone.state.fly_mask:
                drone.takeoff()

            image = drone.frame
            fps, last_frame_shown = fps_calc(time.time(), last_frame_shown)

            if time.time() > land_time:
                while drone.state.fly_mask:
                    drone.land()
                break

            bbox = tiny_yolo.yolo_update.get_bounding_box(image, net, background)
            if bbox:
                x, y, w, h = bbox

                image = tiny_yolo.yolo_update.add_bounding_box(image, bbox)
                image = tiny_yolo.yolo_update.add_size(image, w)

                ## Control drone
                if drone.state.fly_mask:
                    if w < 170:
                        go_back=False
                    if w >= 170:
                        drone.move(backward=0.9)
                        go_back=True
                    else:
                        drone.move(forward=0.24)
            else:
                if go_back:
                    drone.move(backward=0.9)
                else:
                    drone.move(forward=0.28)


            image = add_fps(image, fps)
            cv2.imshow('Detection and tracking', image)
            out.write(image)

            if cv2.waitKey(10) == ord(' '):
                break
        out.release()
        # playVideo(drone)
        sys.exit()
finally:
    while drone.state.fly_mask:
        drone.land()
    drone.close()
