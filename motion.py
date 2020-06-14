# 02/2020
# code from https://youtu.be/MkcUgPhOlP8
# I modify the code to fit the needs
import cv2
import numpy as np
# not official from facebook
from fbchat import Client
from fbchat.models import *
import fbchat       
from getpass import getpass
from datetime import datetime


cap = cv2.VideoCapture(0)  # 0 to open laptop cam or ip address

ret, frame1 = cap.read()
ret, frame2 = cap.read()

user = "munyoudoum" # your facebook username
# type your password
client = fbchat.Client(user, getpass())

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900: # 900 = size of motion
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), \
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        # check when the time(seconds) is  between 00s 10s
        
        if "00" < datetime.now().strftime("%S") < "10":
            # create a picture file
            cv2.imwrite('01.png', frame1)
            # send a message on Facebook
            client.sendLocalImage(
                "01.png",
                message=Message(text="MOTION DETECTED"),
                thread_id=client.uid,
                thread_type=ThreadType.USER)
                
    image = cv2.resize(frame1, (1280, 720))

    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    # press esc to stop the camera
    if cv2.waitKey(40) == 27:
        break
client.logout()
cv2.destroyAllWindows()
cap.release()
