import RPi.GPIO as GPIO
import math
import time 

f = 0.2
start = time.time()
theta = (math.pi)/11

GPIO.setmode(GPIO.BCM)
p=4
ptwo = 17
GPIO.setup(p, GPIO.OUT)
GPIO.setup(ptwo, GPIO.OUT)

pwm = GPIO.PWM(p, 500)
pwmtwo = GPIO.PWM(ptwo, 500)
pwm.start(0)
pwmtwo.start(0)

try:
	while True:
		t = time.time() - start
		B = (math.sin(2*math.pi*f*t))**2
		Btwo = (math.sin(2*math.pi*f*t - theta))**2
		duty = B * 100
		dutytwo = Btwo * 100
		pwm.ChangeDutyCycle(duty)
		pwmtwo.ChangeDutyCycle(dutytwo)

except KeyboardInterrupt:
	pass

pwm.stop()
GPIO.cleanup()
