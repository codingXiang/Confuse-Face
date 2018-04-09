import numpy as np
import cv2
from PIL import Image
import math, operator
from functools import reduce
from GUI import GUI
import os
import random, string

class FaceRecognition(object):
    def __init__(self, classifier_path, threshold):
        self.threshold = threshold
        self.face_cascade = cv2.CascadeClassifier(str(classifier_path))
        self.confused_cascade = cv2.CascadeClassifier("haarcascades\\confused.xml")
        self.other_count = 0
        self.confused_count = 0
    def create_origin_face(self):
        self.open_camera('create_origin_face', 'origin')
        cv2.waitKey(1000)
        self.catch_face('origin.jpg', 'origin')
        GUI.popupmsg("新增人臉完成")
    def detect_face(self):
        cv2.namedWindow("detect face")
        cap = cv2.VideoCapture(0)
        while (cap.isOpened()):
            ret, img = cap.read()
            faces = self.face_cascade.detectMultiScale(img, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img, "catch face", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 255)
            cv2.imshow("detect face", img)
            if ret == True:
                key = cv2.waitKey(50)
                if key == ord("q") or key == ord("Q"):
                    break
        cap.release()
        cv2.destroyAllWindows()
    def detect_confused_emotion(self):
        cv2.namedWindow("detect confused emotion")
        cap = cv2.VideoCapture(0)
        while (cap.isOpened()):
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            confused = self.confused_cascade.detectMultiScale(gray, 1.1, minSize=(150, 150))
            for (x, y, w, h) in confused:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img, "Confused :(", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 255)
            cv2.imshow("detect confused emotion", img)
            if ret == True:
                key = cv2.waitKey(50)
                if key == ord("q") or key == ord("Q"):
                    break
        cap.release()
        cv2.destroyAllWindows()
    def add_new_emotion(self):
        cv2.namedWindow("create emotion")
        cap = cv2.VideoCapture(0)
        while (cap.isOpened()):
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(img, 1.2, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img, "Catch Face", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 255)
            cv2.imshow("create emotion", img)
            if ret == True:
                key = cv2.waitKey(50)
                if key == ord("o") or key == ord("O"):
                    cv2.imwrite(str("other" + str(self.other_count) + '.jpg'), gray)
                    image = Image.open(str("other" + str(self.other_count) + '.jpg'))
                    imageCrop = image.crop((x, y, x + w, y + h))
                    imageResize = imageCrop.resize((150, 150), Image.ANTIALIAS)
                    imageResize.save(str("other" + str(self.other_count) + '.jpg'))
                    self.other_count += 1
                if key == ord("c") or key == ord("C"):
                    cv2.imwrite(str("confused" + str(self.confused_count) + '.jpg'), gray)
                    image = Image.open(str("confused" + str(self.confused_count) + '.jpg'))
                    imageCrop = image.crop((x, y, x + w, y + h))
                    imageResize = imageCrop.resize((150, 150), Image.ANTIALIAS)
                    imageResize.save(str("confused" + str(self.confused_count) + '.jpg'))
                    self.confused_count += 1
                if key == ord("q") or key == ord("Q"):
                    break
        cap.release()
        cv2.destroyAllWindows()
    def verify_process(self):
        self.open_camera('Face Recognition', 'output')
        cv2.waitKey(1000)
        self.catch_face('output.jpg', 'output')
        distance = self.face_distance('origin0', 'output0')
        if (self.verify_face(distance)):
            GUI.popupmsg("驗證成功！")
        else:
            GUI.popupmsg("驗證失敗！")
        try:
            os.remove("output0.jpg")
        except:pass

    def open_camera(self, window_name, save_filename):
        cv2.namedWindow(window_name)
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):
            ret , img = cap.read()
            cv2.imshow(window_name, img)
            if ret == True:
                key = cv2.waitKey(200)
                if key == ord("a") or key == ord("A"):
                    cv2.imwrite(str(save_filename + '.jpg'),img)
                    break
        cap.release()
        cv2.destroyAllWindows()
    def catch_face(self, path, output_filename):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        num = 0
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.rectangle(gray, (x, y), (x + w , y + h), (255, 0, 0), 2)
            filename = output_filename + str(num) + ".jpg"
            image = Image.open(path)
            imageCrop = image.crop((x, y, x + w, y + h))
            imageResize = imageCrop.resize((150, 150), Image.ANTIALIAS)
            imageResize.save(filename)
            num += 1
        cv2.imshow(path, img)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
    def face_distance(self, origin_name, after_name):
        h1 = Image.open(str(origin_name + '.jpg')).histogram()
        h2 = Image.open(str(after_name + '.jpg')).histogram()
        rms12 = math.sqrt(reduce(operator.add,map(lambda a, b: (a-b)**2, h1, h2))/len(h1))
        return rms12
    def verify_face(self, distance):
        print(distance)
        if (distance < self.threshold):
            return True
        return False
