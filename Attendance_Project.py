import cv2
import numpy as np
import face_recognition as fr
import os
from datetime import datetime

path = "Images"      #path where pictures are store
images = []          #store images
students = []        #store names of the students

#Storing Names of the Students from the Picture Caption

myList = os.listdir(path)      #have names like Esha.jpg, Vivek,jpg

for name in myList:
    curImg = cv2.imread(f"{path}/{name}")           #read images from the folder
    images.append(curImg)
    students.append(os.path.splitext(name)[0])      #store names as Esha, Vivek
    
print("Students in the Class..\n", students)


#Finding encodings for the images
def findEncoding(images):
    encodeList = []    #store the encodings for the images
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)        
    return encodeList

encodeListKnown = findEncoding(images)
print("\nEncoding Completed...")


def markAttendance(name):
    with open("Attendance.csv", "r+") as f:
        myData = f.readlines()
        nameList = []
        for line in myData:
            entry = line.split(",")
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.writelines(f"\n{name}, {dtString}")
            
 

#Intializing Web Cam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    success, img = cap.read()
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
        else:
            name = "UNKNOWN"
        
        y1, x2, y2, x1 = faceLoc
        #Because we have reduced the size of the image captured to fit the rectangle 
        #we are multipling coordinates by 4
        #y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)  #For face
        cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,255,0), cv2.FILLED) #For name
        cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2) 
        markAttendance(name)         
        
            
    #Making Bound Rectangle
    cv2.imshow("Web Cam", img)
    key = cv2.waitKey(1)
    if key > 0:               #close with ECS button
        break
    
cap.release() #Turn off the camera
cv2.destroyAllWindows()


