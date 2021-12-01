# Author : Michael Dittman
# 12/1/21
# Basic code to detect objects in image for mmWave data capture project

# Credits
#
# Cody Fizette (https://github.com/cfizette), Abhishek Kumar Annamraju (https://github.com/abhi-kumar) for the various haar cascades
# used in this project


import numpy as np
import cv2
import time

# Get the haar cascades and create classifier objects
face_cascade_default = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
car_cascade_profile = cv2.CascadeClassifier('cas1.xml')
stop_sign_cascade_profile = cv2.CascadeClassifier('stop_sign.xml')
traffic_light_cascade_profile = cv2.CascadeClassifier('traffic_light.xml')


cap = cv2.VideoCapture(0)

while True:

    # Capture the image
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces_default = face_cascade_default.detectMultiScale(gray, 1.3, 5)
    car_profile = car_cascade_profile.detectMultiScale(gray, 1.3, 5)
    stop_sign = stop_sign_cascade_profile.detectMultiScale(gray, 1.3, 5)
    traffic_light = traffic_light_cascade_profile.detectMultiScale(gray, 1.3, 5)

    # Write some Text
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 500)
    fontScale = 1
    fontColor = (0, 0, 255)
    lineType = 2

    # Detect faces in picture
    for (x, y, w, h) in faces_default:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(img, 'person',
                    (x + w + 10, y + h),
                    font,
                    fontScale,
                    (0, 0, 255),
                    lineType)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

    # Detect stop signs
    for (x, y, w, h) in car_profile:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(img, 'car',
                    (x + w + 10, y + h),
                    font,
                    fontScale,
                    (255, 0, 0),
                    lineType)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

    # Detect stop signs
    for (x, y, w, h) in stop_sign:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(img, 'stop_sign',
                    (x + w + 10, y + h),
                    font,
                    fontScale,
                    (255, 0, 0),
                    lineType)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

    # Detect traffic_lights
    for (x, y, w, h) in traffic_light:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(img, 'traffic_light',
                    (x + w + 10, y + h),
                    font,
                    fontScale,
                    (255, 0, 0),
                    lineType)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
