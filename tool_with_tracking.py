import numpy as np
import cv2
import dlib

tracker = dlib.correlation_tracker()
cap = cv2.VideoCapture(0)
s = ""

okk, frame = cap.read()
if not okk:
	print ('Cannot read video file')
	sys.exit()

gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
bbox = cv2.selectROI(gray, False)

tracker.start_track(gray,dlib.rectangle(int(bbox[0]),int(bbox[1]),int(bbox[0] + bbox[2]),int(bbox[1] + bbox[3])))
i=0
t=0
while(True):
    ret, frame = cap.read()
    i+=1
    if not ret:
    	break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    tq = tracker.update(gray)
    if tq > 4:
	    tracked_position =  tracker.get_position()
	    x = int(tracked_position.left())
	    y = int(tracked_position.top())
	    w = int(tracked_position.width())
	    h = int(tracked_position.height())
	    cv2.rectangle(gray, (x, y),(x + w , y + h),(255,255,255),2)
	    new_img=gray[y:y+h,x:x+w]
	    cv2.imshow('frame2',new_img)
	    if (i%5)==0:
	    	t+=1
	    	cv2.imwrite('image/'+ s + str(t) + '.png', new_img)



    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()