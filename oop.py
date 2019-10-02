# -*- coding: utf-8 -*-
import cv2
import dlib
import threading
import time
import numpy

class oop(object):
	"""Hướng đối tượng"""
	def __init__(self, training, name, pathVideo, t1, t2, t3, t4):
		super(oop, self).__init__()
		self.training = training
		self.name = name
		self.pathVideo = pathVideo
		self.t1 = t1 #scaleFactor
		self.t2 = t2 #minNeightbor
		self.t3 = t3 #width
		self.t4 = t4 #height

	#set ten va stt
	def setObj(self, objNames, objid):
	    time.sleep(1)
	    objNames[ objid ] =self.name +"#" + str(objid)

	def detectAndTrackMultipleObjs(self): #Nhớ: hàm của python lúc nào cũng có self
	    objCascades = cv2.CascadeClassifier(self.training)
	    capture = cv2.VideoCapture(self.pathVideo)

	    cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
	    cv2.namedWindow("Result-image", cv2.WINDOW_AUTOSIZE)

	    cv2.moveWindow("Image",0,0)
	    cv2.moveWindow("Result-image",340,0)

	    cv2.startWindowThread()

	    #Mau cua khung theo doi
	    rectangleColor = (0,0,255)

	    #Kich thuoc khung
	    SMALL_SIZE=(640,480)
	    LARGER_SIZE=(832,624)

	    #bien toan cuc chua so frame vs stt
	    frameCounter = 0
	    currentObjID = 0

	    #Dic chứa corel track
	    objTrackers = {}
	    objNames = {}

	    try:
	        while True:
	            ret,fullSizeBaseImage = capture.read()
	            if not ret:
	            	break
	            
	            baseImage = cv2.resize( fullSizeBaseImage, SMALL_SIZE)

	            resultImage = baseImage.copy()


	            frameCounter += 1 

	            objidsToDelete = []
	            for objid in objTrackers.keys():
	                trackingQuality = objTrackers[ objid ].update( baseImage )

	                if trackingQuality < 4: #add doi tuong vao danh sach xoa
	                    objidsToDelete.append( objid )

	            for objid in objidsToDelete:
	                print("Xoa doi tuong " + str(objid) + " ra khoi danh sach theo doi")
	                objTrackers.pop( objid , None ) #xoa trong Dic chua ban dau

	          	#Sau 2 frame thi nhan dang 1 lan (Video khong bi giat, giam thoi gian xu ly, neu 1
	          	# doi tuong chi xuat hien trong 1 frame la vo ly vi luc doi tuong lam sao ma chuyen dong dc?)
	            if (frameCounter % 2) == 0:

	                gray = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)

	                objs = objCascades.detectMultiScale( gray, self.t1, self.t2, minSize=( self.t3, self.t4) )

	                for (_x,_y,_w,_h) in objs:
	                    x = int(_x)
	                    y = int(_y)
	                    w = int(_w)
	                    h = int(_h)

	                    x_bar = x + (w/2)
	                    y_bar = y + (h/2)

	                    ok_objID = None

	                    #Kiểm tra coi tâm của đối tượng đã nằm trong vùng theo dõi chưa?
	                    #Và tâm của vùng theo dõi đã ở trong đối tượng chưa?
	                    #Nếu đúng thì ok còn chưa thì đối tượng đó chưa đc theo dõi
	                    for objid in objTrackers.keys():
	                        t_pos =  objTrackers[objid].get_position() #lay vi tri cua nhung doi tuong dc theo doi

	                        t_x = int(t_pos.left())
	                        t_y = int(t_pos.top())
	                        t_w = int(t_pos.width())
	                        t_h = int(t_pos.height())

	                        t_x_bar = t_x + t_w/2 #lay tam
	                        t_y_bar = t_y + t_h/2 #lay tam

	                        if ( ( t_x <= x_bar   <= (t_x + t_w)) and 
	                             ( t_y <= y_bar   <= (t_y + t_h)) and 
	                             ( x   <= t_x_bar <= (x   + w  )) and 
	                             ( y   <= t_y_bar <= (y   + h  ))):
	                            ok_objID = objid

	                    if ok_objID is None:

	                        print("Theo doi doi tuong " + str(currentObjID))
	                        tracker = dlib.correlation_tracker()
	                        tracker.start_track(baseImage,
	                                            dlib.rectangle( x, y, x+w, y+h))

	                        objTrackers[ currentObjID ] = tracker #add vào mảng

	                        t = threading.Thread( target = self.setObj ,
	                                               args=(objNames, currentObjID)) #threading hàm
	                        t.start()

	                        currentObjID += 1
	                    #if ok_objID:
	                    #	print ("Do nothing")

	            for objid in objTrackers.keys():
	                t_pos =  objTrackers[objid].get_position()

	                t_x = int(t_pos.left())
	                t_y = int(t_pos.top())
	                t_w = int(t_pos.width())
	                t_h = int(t_pos.height())

	                #ve khung theo doi
	                cv2.rectangle(resultImage, (t_x, t_y),
	                                        (t_x + t_w , t_y + t_h),
	                                        rectangleColor ,2)
	                #ve tam (center)
	                cv2.circle(resultImage,( t_x + int(t_w/2), t_y + int(t_h/2)), 2 , (255,0,0) , -1 )

	                #Viet vi tri len tam
	                cv2.putText(resultImage,"({},".format(t_x+int(t_w/2)) + "{})".format(t_y+int(t_h/2)),
	                				( t_x + int(t_w/2)-15, t_y + int(t_h/2)+15),
	                                cv2.FONT_HERSHEY_PLAIN,
	                                1, (255, 255, 255), 1)

	                if objid in objNames.keys():
	                    cv2.putText(resultImage, objNames[objid] , 
	                                (int(t_x), int(t_y)-5), 
	                                cv2.FONT_HERSHEY_PLAIN,
	                                1, (255, 255, 255), 1)
	                else:
	                    cv2.putText(resultImage, "detecting..." , 
	                                (int(t_x), int(t_y)-5), 
	                                cv2.FONT_HERSHEY_PLAIN,
	                                1, (255, 255, 255), 1)

	            kq = cv2.resize(resultImage,
	                                     LARGER_SIZE)

	            if cv2.waitKey(1) & 0xFF == 27:
	            	break
	            
	            cv2.imshow("Image", baseImage)
	            cv2.imshow("Result-image", kq)

	    except KeyboardInterrupt as e:
	        pass
	    capture.release()
	    cv2.destroyAllWindows()