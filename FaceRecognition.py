import cv2
#import numpy as np
import face_recognition as fr

img = fr.load_image_file("Images\Elon Musk.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

imgTest = fr.load_image_file("Images\Elon Musk Test.jpg")
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

imgLoc = fr.face_locations(img)[0]
encodeImg = fr.face_encodings(img)[0]
cv2.rectangle(img, (imgLoc[3], imgLoc[0]), (imgLoc[1], imgLoc[2]), (255,100,200), 4)

imgTestLoc = fr.face_locations(imgTest)[0]
encodeImgTest = fr.face_encodings(imgTest)[0]
cv2.rectangle(imgTest, (imgTestLoc[3], imgTestLoc[0]), (imgTestLoc[1], imgTestLoc[2]), (255,0,255), 4)

results = fr.compare_faces([encodeImg], encodeImgTest)
print(results)

cv2.imshow("Elon Musk", img)
cv2.imshow("Elon Musk Test", imgTest)
cv2.waitKey(0)