import RPi.GPIO as GPIO
import math
import time 

f = 0.2
start = time.time()

GPIO.setmode(GPIO.BCM)
p=4
GPIO.setup(p, GPIO.OUT)

pwm = GPIO.PWM(p, 500)
pwm.start(0)

try:
	while True:
		t = time.time() - start
		B = (math.sin(2*math.pi*f*t))**2
		duty = brightness * 100
		pwm.ChangeDutyCycle(duty)

except KeyboardInterrupt:
	pass

pwm.stop()
GPIO.cleanup()
