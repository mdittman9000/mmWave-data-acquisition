import cv2
from datetime import datetime
# Open the Camera
cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    # Put current DateTime on each frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,str(datetime.now()),(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
    # Display the image
    cv2.imshow('a',img)
    # wait for keypress
    k = cv2.waitKey(10)
    if k == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

