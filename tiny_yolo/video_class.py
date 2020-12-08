import sys
from threading import Thread
import cv2
import time

# from https://stackoverflow.com/questions/55099413/python-opencv-streaming-from-camera-multithreading-timestamps
import numpy as np


class VideoHandler(object):
    def __init__(self, src=2):
        self.video_cap = cv2.VideoCapture(src)
        self.video_cap.set(3, 320)
        self.video_cap.set(4, 180)

        # Exit if video not opened.
        if not self.video_cap.isOpened():
            print("Could not open video")
            sys.exit()
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.status = False
        self.cam_frame = None
        self.last_frame_shown = time.time()

    def last_frame(self):
        if self.status:
            frame_processed = np.copy(self.cam_frame)
        else:
            frame_processed = None
        fps_calculated = self.fps_calc()
        return self.status, frame_processed, fps_calculated

    def fps_calc(self):
        current_time = time.time()
        fps = round(1 / (current_time - self.last_frame_shown), 1)
        self.last_frame_shown = current_time
        return fps

    def update(self):
        while True:
            counter = 0
            if self.video_cap.isOpened():
                self.status, self.cam_frame = self.video_cap.read()
            else:
                counter += 1
                if counter > 1000:
                    break
            time.sleep(.01)

    def is_open(self):
        return self.video_cap.isOpened()


    def show_frame(self, frame):
        # Display frames in main program
        print("Show img")
        cv2.imshow('Detection and tracking', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            print("Quiting")
            self.video_cap.release()
            cv2.destroyAllWindows()
            exit(1)

    def quit(self):
        self.video_cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    video_stream_widget = VideoHandler()
    while True:
        try:
            status, frame, fps = video_stream_widget.last_frame()
            if status:
                video_stream_widget.show_frame(frame)
            else:
                status, frame = video_stream_widget.video_cap.read()
                print(status)
        except AttributeError:
            pass
