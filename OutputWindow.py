from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QDate
from PyQt5.QtWidgets import QDialog, QMessageBox
import cv2
import face_recognition as fr
import numpy as np
import datetime
import os
#import csv
#import Attendance_Project as ap

path = "Images"      #path where pictures are store
images = []          #store images
students = []        #store names of the students

myList = os.listdir(path)      #have names like Esha.jpg, Vivek,jpg

for name in myList:
    curImg = cv2.imread(f"{path}/{name}")           #read images from the folder
    images.append(curImg)
    students.append(os.path.splitext(name)[0])      #store names as Esha, Vivek

class Ui_OutputWindow(QDialog):
    def __init__(self):
        super(Ui_OutputWindow, self).__init__()
        loadUi("./outputwindow.ui", self)
        
        self.logic = 0
        self.value = 0
        self.start = 0
        self.end = 0
        self.name = ""
        self.ClockIn = False
        
        self.startHour = self.endHour = 0
        self.startMin = self.endMin = 0
        self.startSec = self.endSec = 0
        
        self.SCREENSHOT.clicked.connect(self.onClickSS)        
        self.TEXT.setText("WELCOME!!")
        
        #Update time
        now = QDate.currentDate()
        current_date = now.toString(' ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime(" %I:%M %p")
        self.DATE.setText(current_date)
        self.TIME.setText(current_time)
        
        self.CLOCK_IN.clicked.connect(self.In)
        self.CLOCK_OUT.clicked.connect(self.Out)
        
                
    @pyqtSlot()
    #Storing Names of the Students from the Picture Caption
       
    #Finding encodings for the images
    def findEncoding(self, images):
        encodeList = []    #store the encodings for the images
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = fr.face_encodings(img)[0]
            encodeList.append(encode)        
        return encodeList


    def markAttendance(self, name):
        with open("Attendance.csv", "r+") as f:
            myData = f.readlines()
            nameList = []
            for line in myData:
                entry = line.split(",")
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.datetime.now()
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{name}, {dtString}")
                
    def startVideo(self):
        self.TEXT.setText("Clock In to Capture an Image!!")
        
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        encodeListKnown = self.findEncoding(images)
        
        while self.capture.isOpened():
            
            success, img = self.capture.read()
            
            if success == True:
                self.displayImage(img, 1)
                cv2.waitKey()
                
                if self.ClockIn == True:
                
                    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
                    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    
                    faceWeb = fr.face_locations(imgS)
                    encodeWeb = fr.face_encodings(imgS, faceWeb)                
                    
                    for encodeFace, faceLoc in zip(encodeWeb, faceWeb):
                        
                        matches =  fr.compare_faces(encodeListKnown, encodeFace)        
                        faceDis = fr.face_distance(encodeListKnown, encodeFace)
                        
                        matchIndex = np.argmin(faceDis) 
                        
                        if matches[matchIndex]:
                            name = students[matchIndex].upper()
                            self.NAME.setText(f" {name}")
                            if name != "UNKNOWN":
                                self.markAttendance(name)
                        else:
                            name = "UNKNOWN"
                                             
                        y1, x2, y2, x1 = faceLoc
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2 - 20), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        
                
                    if self.logic == 2:
                        
                        buttonReply = QMessageBox.question(self, 'Screenshot', 'Save or not?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        self.logic = 1
                        
                        if buttonReply == QMessageBox.Yes:
                            self.value = self.value + 1
                            cv2.imwrite("C:\Users\ASUS1\Desktop\Minor Project 3\Screenshot\%s.jpg"%(self.value), img)
                                                    
                            self.TEXT.setText("Your Image Saved!!\nFor another Screenshot press \"SCREENSHOT\" again.")
                        else:
                            self.TEXT.setText("Screenshot not Captured!")
                            continue
                    else:
                        self.logic = 1
                        
    
    def In(self):
        
        buttonReply = QMessageBox.question(self, 'Welcome', 'Are you Clocking In?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if buttonReply == QMessageBox.Yes:  
            self.ClockIn = True
            self.TEXT.setText("Kindly Press \"SCREENSHOT\" to Capture an Image!!")
            self.STATUS.setText(" Clocked In")
            self.start = datetime.datetime.now().strftime(" %I:%M:%S")
            self.startHour = int(self.start[1:3])
            self.startMin = int(self.start[4:6])
            self.startSec = int(self.start[7:])
            
            self.HOUR.setText(" Calculati")
            self.MIN.setText("ng!!....")
            self.SEC.setText(" ")
        else:
            self.ClockIn = False
    
    
    def Out(self):
        buttonReply = QMessageBox.question(self, 'Class Over', 'Are you Clocking Out?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if buttonReply == QMessageBox.Yes:  
            self.STATUS.setText(" Clocked Out")
            
            self.end = datetime.datetime.now().strftime(" %I:%M:%S")
            self.endHour = int(self.end[1:3])
            self.endMin = int(self.end[4:6])
            self.endSec = int(self.end[7:])
            self.HOUR.setText(f" {abs(self.endHour - self.startHour)}h")
            self.MIN.setText(f" {abs(self.endMin - self.startMin)}m")
            self.SEC.setText(f" {abs(self.endSec - self.startSec)}s")
            
            self.WebCam.setText("CLASS OVER!!")
            self.TEXT.setText("Class Over! No Screenshot will be captured now.")
            #self.NAME.setText("Attandance Marked!")
            
            self.capture.release()
            cv2.destroyAllWindows()
    
    
    def onClickSS(self):
        self.logic = 2
        
        
    def displayImage(self, image, window = 1):
        
        image = cv2.resize(image, (640, 480))
    
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.WebCam.setPixmap(QPixmap.fromImage(outImage))
            self.WebCam.setScaledContents(True)
        