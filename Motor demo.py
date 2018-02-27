import RPi.GPIO as GPIO
import time

imp1 = 23        # forward right
imp2 = 24        # backward right
imp3 = 8        # forward left
imp4 = 7        # backward left
enA = 25
enB = 9

print "setting up motors"
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(imp1, GPIO.OUT)
GPIO.setup(imp2, GPIO.OUT)
GPIO.setup(imp3, GPIO.OUT)
GPIO.setup(imp4, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)




while True:
        
    GPIO.output(imp1, False)
    GPIO.output(imp2, False)
    GPIO.output(imp3, False)
    GPIO.output(imp4, False)

    GPIO.output(enA, True)
    GPIO.output(enB, True)
    
    print "Waiting For Sensor To Settle"
    
    time.sleep(1)

    print "Moving motor 1"
    
    GPIO.output(imp1, True)
    time.sleep(2)
    GPIO.output(imp1, False)

    print "Stoping motor 1"

    GPIO.cleanup()
