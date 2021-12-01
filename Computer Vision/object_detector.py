import cv2;

# haarcascade
trained_face_data = cv2.CascadeClassifier('model.xml');

# img = cv2.imread('robert.jpg')


webcam = cv2.VideoCapture(0)

while True:
    successful_frame_read, frame = webcam.read()
    grayscaled_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_coordinates = trained_face_data.detectMultiScale(grayscaled_img);

    for (x, y, w, h) in face_coordinates:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Webcam Detector', frame);
    key = cv2.waitKey(1)
    if key == 81 or key == 113:
        break

webcam.release();
# grayscaled_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# # detect faces

# face_coordinates = trained_face_data.detectMultiScale(grayscaled_img);

# # print(face_coordinates)
# (x,y,w,h) = face_coordinates[0]
# cv2.rectangle(img, (x, y),(x + w,y + h),(0,255,0),2)

# print(face_coordinates)

# cv2.imshow('Detector',img);

# cv2.waitKey();