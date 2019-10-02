import numpy as np
import cv2

cap = cv2.VideoCapture(0)
i=0
t=0
s="ii55"
while(True):
    ret, frame = cap.read()
    i+=1
    if not ret:
    	break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.rectangle(gray, (200-1, 270-1),(400+1, 470+1),(0,255,0),1)

    new_img = gray[270:470,200:400]

    cv2.imshow('frame2',new_img)

    if (i%5)==0:
    	t+=1
    	cv2.imwrite('i4/'+ s + str(t) + '.png', new_img)
	
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()