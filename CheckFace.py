import cv2
import numpy as np
import pickle
import sys
import os
import time

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_detector(frame):

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return None,None

    roi = []
    cord = []

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        cv2.rectangle(frame, (x,y-30), (x+w,y), (0,255,255), -1)
        cv2.putText(frame, 'Unknown', (x+2,y-10), 4, 0.6, (0,0,0), 1)
        croi = frame[y:y+h, x:x+w]
        l = []
        l.append((x,y))
        l.append((x+w,y+h))
        cord.append(l)
        roi.append(cv2.resize(croi, (200, 200)))
    return roi,cord

if __name__ == '__main__':

    totalModel = 0

    with open('train/FaceData/imagecount.txt','r') as f:
        totalModel = int(f.read())+1

    modelNameList = []

    for i in range(totalModel):
        modelNameList.append('train/FaceData/'+str(i)+'.cv2')

    nameList = []
    modelList = []
    pmodelList = []

    for i in range(totalModel):
        modelList.append(cv2.createLBPHFaceRecognizer())

    for i in range(totalModel):
        modelList[i].load(modelNameList[i])

    with open('train/FaceData/nameList','r') as f:
                nameList = pickle.load(f)

    try:

        if sys.argv[1]=='-dir':

            if os.path.exists(sys.argv[2]):
                frame = cv2.imread(sys.argv[2])
                frame = cv2.resize(frame,(500,500))
                faces,positions = face_detector(frame)

                if faces is None:
                    print('Face not Recognised')

                else:
                    try:
                        flag = 0
                        for i,face in enumerate(faces):
                            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                            for j,model in enumerate(modelList):
                                results = model.predict(face)

                                if results[1] < 500:
                                    confidence = int( 100 * (1 - (results[1])/400) )

                                    if confidence>=70:
                                        flag = 1
                                        cv2.rectangle(frame, (positions[i][0][0],positions[i][0][1]-30), (positions[i][1][0],positions[i][0][1]), (0,255,0), -1)
                                        cv2.putText(frame, nameList[j], (positions[i][0][0]+2,positions[i][0][1]-10), 4, 0.6, (0,0,0), 1)
                                        cv2.rectangle(frame, positions[i][0], positions[i][1], (0,0,255), 2)
                                        os.unlink('/home/pi/script/camera/Intruder.jpg')
                                        cv2.imwrite('/home/pi/script/camera/'+nameList[j]+'.jpg',frame)

                            if flag == 0:
                                os.unlink('/home/pi/script/camera/Intruder.jpg')
                                cv2.imwrite('/home/pi/script/camera/Intruder.jpg',frame)
                    except:
                        pass

            else:
                pass

    except:
        pass
