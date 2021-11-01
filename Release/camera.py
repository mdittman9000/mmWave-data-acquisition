import numpy as np
import os
import time
import cv2


filename = 'video.avi'
frames_per_second = 24.0
res = '720p'

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


def start_video_acquisition():
    """
    Function that starts video acquisition. This will serve as the entry point
    to the camera data
    :return: None
    """
    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

    while True:
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def start_video_acquisition_timed(seconds=10):
    """
    Function that starts video acquisition. This will serve as the entry point
    to the camera data
    :param seconds: The number of seconds to capture video for (Default value of 10 seconds)
    :return: None
    """

    # Get the current time
    start_time = time.time()

    # Store the elapsed time
    elapsed_time = time.time() - start_time

    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

    # While the amount of time passed is less than how long we want to record video for
    while elapsed_time < seconds:

        # Continue to retrieve frames from the camera
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame', frame)
        elapsed_time = int(time.time() - start_time)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()