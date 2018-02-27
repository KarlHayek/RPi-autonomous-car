import cv2, numpy as np, time
from vision import *
from picamera.array import PiRGBArray
from picamera import PiCamera	
	


real_testing = True
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
width, height = 480, 360
camera.resolution = (width, height)
camera.framerate = 12
rawCapture = PiRGBArray(camera, size=(width, height))

sensitivity = 100
slope_left = slope_right = 1
# allow the camera to warmup
time.sleep(0.1)




################################## MAIN GAME LOOP ####################################

isAtStartPos = real_testing
#isAtStartPos = False
finished_starting = False; in_race = False
start_time = time.time()

counter = 0
 
# capture frames from the camera
for Frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	frame = Frame.array
	
	counter += 1

	##########################
	# BEGINNING OF FRAME PROCESSING


	if isAtStartPos == True:		# Start position: robot is in the pit area
		if not finished_starting and not in_race:		# get the car started
			print ("starting"); forward();
			if time.time() - start_time >= 1:	# the car moves forward for 1 second
				finished_starting = True
		else:
			isAtStartPos = detect_pit(frame[height/2:height, 0:width]) # lower half of the frame
			print ("Start position"); forward()

	else:
		slope_left, slope_right = detect_lanes(frame)	# detect slopes of the treack lines
		print(slope_left, slope_right)
		
		if slope_left > 2: slope_left = 0	 	# if the left line goes outward to the left
		if slope_right < -2: slope_right = 0	# if the right line goes outward to the right

		if -0.4 > slope_left > -3 and 0.4 < slope_right < 3:
			forward()

		elif 0.4 < slope_right < 3 and slope_left <= -3 :
			forward_left()

		elif -0.4 > slope_left > -3 and slope_right >= 3:
			forward_right()
			
		elif slope_left == 0 and slope_right > 0.52:
			forward_left()
			
		elif slope_right == 0 and slope_left < -0.52:
			forward_right()
			
		elif slope_left == 0 and slope_right > 0:
			turn_left()

		elif slope_right == 0 and slope_left < 0:
			turn_right()
			


		elif slope_left == slope_right == 0:
			print("No line detected")
			stop()
			
		else:
			print("Don't know what to do")
			stop()






	##########################
	# END OF FRAME PROCESSING

	print("Count:", counter)
	if counter > 50: counter = 0
	
	cv2.imshow("road", frame)
	

	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		stop()
		break



## cleanup the camera and close any open windows
#camera.release()
#cv2.destroyAllWindows()
stop()