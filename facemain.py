# -*- coding: utf-8 -*-
import socket
import urllib2
import numpy as np
import cv2
import PyBaiduYuyin as pby
from facepp import API
from facepp import File
import cv2.cv as cv
import datetime

baidu_api_key = "VcH8GXmN6hZIqBxf4HG4DxFU"
baidu_api_sec = "vmTVsaiGMtrnEm018H820NhrCWuY8GkU"

API_KEY = '1f62e1802e3bdcaa3f1b8c0713eb824a'
API_SECRET = 'Y5FWySkIlL-LWxSLQy9MzXcOt4NgiEZ9'
api = API(API_KEY, API_SECRET)
tts = pby.TTS(app_key=baidu_api_key, secret_key=baidu_api_sec)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
path = './frame/x.jpg'
#connect camera and set width & hiehgt
cap = cv2.VideoCapture(0)
cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

imgs_count = 0
mark = 0
current_person = ''
identify_count = 0
while(True):
    #leemos un frame y lo guardamos
    imgs_count += 1
    ret, img = cap.read()
    if img is None:
        waitKey(10)
        continue;
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, 1.5, 2)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        cv2.rectangle(img,(x,y),(x+w,y+h),(125,255,0),2)
        #face = img[y:y+h,x:x+w]
        face = img_gray
        cv2.imwrite(path,face)
        print "Face detected"
        if imgs_count - mark > 20:
            mark = imgs_count
            print "Recognizing........."
            try:
                t1 = datetime.datetime.now()
                rst = api.recognition.identify(img = File(path),\
                 group_name = 'test', mode='oneface', async = False)
                t2 = datetime.datetime.now()
                print (t2-t1).microseconds
            except (socket.error, urllib2.URLError) as e:
                continue
            mark = imgs_count

            if len(rst['face']) > 0:
                name = rst['face'][0]['candidate'][0]['person_name']
                print name
                greet = name + u'下午好'
                if current_person != name:
                    current_person = name
                    identify_count = 1
                else:
                    identify_count += 1
                if identify_count == 3:
                    tts.say(text=greet.encode('utf8'))

    else:
        print "No any face in view."

    #Mostramos la imagen
    cv2.imshow('Face Recognition',img)
    #con la tecla 'q' salimos del programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
