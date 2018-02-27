import cv2, numpy as np, time
import RPi.GPIO as GPIO

width, height = 480, 360
sensitivity = 100


ForwRight = 23        # forward right
BackRight = 24        # backward right
ForwLeft = 8        # forward left
BackLeft = 7        # backward left
enA = 25
enB = 9

	
#print "setting up motors"
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(ForwRight, GPIO.OUT)
GPIO.setup(BackRight, GPIO.OUT)
GPIO.setup(ForwLeft, GPIO.OUT)
GPIO.setup(BackLeft, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)

def stop():
	GPIO.output(ForwRight, False)
	GPIO.output(BackRight, False)
	GPIO.output(ForwLeft, False)
	GPIO.output(BackLeft, False)

stop()
GPIO.output(enA, True)
GPIO.output(enB, True)
		

def forward():
	print("mov forw")		
	GPIO.output(imp1, True)
	GPIO.output(imp3, True)
	time.sleep(t)
	GPIO.output(imp1, False)
	GPIO.output(imp3, False)
	
def forward_left():
	print("mov forw left")
	GPIO.output(imp3, True)
	time.sleep(tt)
	GPIO.output(imp3, False)
	
def forward_right():
	print("mov forw right")
	GPIO.output(imp1, True)
	time.sleep(t)
	GPIO.output(imp1, False)
	
def turn_left():
	print("turn left")
	GPIO.output(imp1, True)
	GPIO.output(imp4, True)
	time.sleep(t)
	GPIO.output(imp1, False)
	GPIO.output(imp4, False)
	
def turn_right():
	print("turn right")
	GPIO.output(imp2, True)
	GPIO.output(imp3, True)
	time.sleep(t)
	GPIO.output(imp2, False)
	GPIO.output(imp3, False)	
	


		
	
#def forward():
#	print("mov forw")
#	stop()		
#	GPIO.output(ForwRight, True)
#	GPIO.output(ForwLeft, True)
#	
#def forward_left():
#	print("mov forw left")
#	stop()
#	GPIO.output(ForwLeft, True)
#	
#def forward_right():
#	print("mov forw right")
#	stop()
#	GPIO.output(ForwRight, True)
#	
#def turn_left():
#	print("turn left")
#	GPIO.output(ForwRight, True)
#	GPIO.output(BackLeft, True)
#	
#def turn_right():
#	print("turn right")
#	stop()
#	GPIO.output(BackRight, True)
#	GPIO.output(ForwLeft, True)





	
def detect_pit(frame):
	""" Returns whether or not the green pit is in the specified frame (and is large enough) """
	# construct a mask for the color "green" in hsv, then perform a series of dilations and erosions to remove any small blobs left in the mask
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	green_mask = cv2.inRange(hsv, (29, 86, 6), (64, 255, 255))
	green_mask = cv2.erode(green_mask, None, iterations=2)
	green_mask = cv2.dilate(green_mask, None, iterations=2)

	image,contours,hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)		# find contours
	if (len(contours) == 0):
#		print("No green contours found at all!")
		return False
	cnt = max(contours, key=cv2.contourArea)
	area = cv2.contourArea(cnt)

	return area > 4000


def detect_redsurface(frame):
	""" Returns if a large enough red surface is in the specified frame """	
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	red_mask = cv2.inRange(hsv, (0, 50, 50), (0, 255, 255))

	image,contours,hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)	
	if (len(contours) == 0):	return False
	cnt = max(contours, key=cv2.contourArea)
	area = cv2.contourArea(cnt)
	return area > 2000

def detect_bluesurface(frame):
	""" Returns if a large enough blue surface is in the specified frame """	
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	blue_mask = cv2.inRange(hsv, (20, 50, 50), (120, 255, 255))

	image,contours,hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)	
	if (len(contours) == 0):	return False
	cnt = max(contours, key=cv2.contourArea)
	area = cv2.contourArea(cnt)
	return area > 1500

def detect_lanes_yellow(frame):
	""" Returns if a large enough yellow surface is in the specified frame """ # for yellow lines	
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#	yellow_mask = cv2.inRange(hsv, (6, 50, 50), (30, 255, 255)) # to be tested
#
#	image,contours,hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)	
#	if (len(contours) == 0):	return False
#	cnt = max(contours, key=cv2.contourArea)
#	area = cv2.contourArea(cnt)
#	return area > 1500


	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	yellow_mask = cv2.inRange(hsv, (6, 50, 50), (30, 255, 255))
	yellow_mask = cv2.erode(yellow_mask, None, iterations=2)
	yellow_mask = cv2.dilate(yellow_mask, None, iterations=2)

	# get the contours of the white mask and draw them
	image,contours,hierarchy = cv2.findContours(yellow_mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	if (len(contours) == 0): print("No contours found at all!")
#	cv2.drawContours(frame, contours, -1 , (0,255,0), 3) # draw all contours found
	# each individual contour is a Numpy array of (x,y) coordinates of the boundary points of the object.

	left_cnts = []; right_cnts = []
	for cnt in contours[:5]:	# first 5 elements
		M = cv2.moments(cnt) # moments of mass
		cx = int(M['m10']/M['m00']); cy = int(M['m01']/M['m00'])
		area = cv2.contourArea(cnt)

		if cy > height/2 and 70 < area < 2000:
			if cx < width/2:
				left_cnts.append(cnt)
			elif cx > width/2:
				right_cnts.append(cnt)

	cv2.drawContours(frame, left_cnts, -1, (0,255,0), 3)
	cv2.drawContours(frame, right_cnts, -1, (0,255,0), 3)

	# line fitting on found contours
	rows,cols = yellow_mask.copy().shape[:2]
	if len(left_cnts) > 0:
		[vx,vy,x,y] = cv2.fitLine(left_cnts[0], cv2.DIST_L2,0,0.01,0.01)
		lefty = int((-x*vy/vx) + y); righty = int(((cols-x)*vy/vx)+y)
		p1_left, p2_left = (cols-1,righty), (0,lefty)
		cv2.line(frame, p1_left, p2_left,(0,0,255),2)
		slope_left = float(p2_left[1] - p1_left[1]) / (p2_left[0] - p1_left[0])
	else: slope_left = 0

	if len(right_cnts) > 0:
		[vx,vy,x,y] = cv2.fitLine(right_cnts[0], cv2.DIST_L2,0,0.01,0.01)
		lefty = int((-x*vy/vx) + y); righty = int(((cols-x)*vy/vx)+y)
		p1_right, p2_right = (cols-1,righty), (0,lefty)
		cv2.line(frame, p1_right, p2_right,(0,0,255),2)
		slope_right = float(p2_right[1] - p1_right[1]) / (p2_right[0] - p1_right[0])
	else: slope_right = 0
	
	if len(left_cnts)== 0 and len(right_cnts)== 0:
		print("No contour found!")

	return(slope_left, slope_right)




def detect_lanes(frame):
	""" Returns the slope of the left and right lanes detected in the frame """
	# construct a mask for the color "white" in hsv, then perform a series of dilations and erosions to remove any small blobs left in the mask
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	white_mask = cv2.inRange(hsv, (0, 0, 255 - sensitivity), (255, sensitivity, 255))
	white_mask = cv2.erode(white_mask, None, iterations=2)
	white_mask = cv2.dilate(white_mask, None, iterations=2)

	# get the contours of the white mask and draw them
	image,contours,hierarchy = cv2.findContours(white_mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	if (len(contours) == 0): print("No contours found at all!")
#	cv2.drawContours(frame, contours, -1 , (0,255,0), 3) # draw all contours found
	# each individual contour is a Numpy array of (x,y) coordinates of the boundary points of the object.

	left_cnts = []; right_cnts = []
	for cnt in contours[:6]:	# first 5 elements
		M = cv2.moments(cnt) # moments of mass
		cx = int(M['m10']/M['m00']); cy = int(M['m01']/M['m00'])
		area = cv2.contourArea(cnt)
#		(x,y),(MA,ma),angle = cv2.fitEllipse(cnt)   	# orientation	###### FOR GAME 1-2!
		# used to filter out lines that are too horizontal
		if cy > height/2 and 125 < area < 4000: # and angle <= 80 and angle >= 100: ### FOR GAME 1-2!
			if cx < width/2:
				left_cnts.append(cnt)
			elif cx > width/2:
				right_cnts.append(cnt)


	cv2.drawContours(frame, left_cnts, -1, (0,255,0), 3)
	cv2.drawContours(frame, right_cnts, -1, (0,255,0), 3)

	# line fitting on found contours
	rows,cols = white_mask.copy().shape[:2]
	if len(left_cnts) > 0:
		[vx,vy,x,y] = cv2.fitLine(left_cnts[0], cv2.DIST_L2,0,0.01,0.01)
		lefty = int((-x*vy/vx) + y); righty = int(((cols-x)*vy/vx)+y)
		p1_left, p2_left = (cols-1,righty), (0,lefty)
		cv2.line(frame, p1_left, p2_left,(0,0,255),2)
		slope_left = float(p2_left[1] - p1_left[1]) / (p2_left[0] - p1_left[0])
	else: slope_left = 0

	if len(right_cnts) > 0:
		[vx,vy,x,y] = cv2.fitLine(right_cnts[0], cv2.DIST_L2,0,0.01,0.01)
		lefty = int((-x*vy/vx) + y); righty = int(((cols-x)*vy/vx)+y)
		p1_right, p2_right = (cols-1,righty), (0,lefty)
		cv2.line(frame, p1_right, p2_right,(0,0,255),2)
		slope_right = float(p2_right[1] - p1_right[1]) / (p2_right[0] - p1_right[0])
	else: slope_right = 0
	
	if len(left_cnts)== 0 and len(right_cnts)== 0:
		print("No contour found!")

	return(slope_left, slope_right)