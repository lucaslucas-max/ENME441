import RPi.GPIO as GPIO
import math
import time 

f = 0.2
start = time.time()
theta = (math.pi)/11

GPIO.setmode(GPIO.BCM)
p=4
ptwo = 17
pthree = 18
pfour = 19
pfive = 20
psix = 21
pseven = 22
peight = 23
pnine = 24
pten = 25

GPIO.setup(p, GPIO.OUT)
GPIO.setup(ptwo, GPIO.OUT)
GPIO.setup(pthree, GPIO.OUT)
GPIO.setup(pfour, GPIO.OUT)
GPIO.setup(pfive, GPIO.OUT)
GPIO.setup(psix, GPIO.OUT)
GPIO.setup(pseven, GPIO.OUT)
GPIO.setup(peight, GPIO.OUT)
GPIO.setup(pnine, GPIO.OUT)
GPIO.setup(pten, GPIO.OUT)

pwm = GPIO.PWM(p, 500)
pwmtwo = GPIO.PWM(ptwo, 500)
pwmthree = GPIO.PWM(pthree, 500)
pwmfour = GPIO.PWM(pfour, 500)
pwmfive = GPIO.PWM(pfive, 500)
pwmsix = GPIO.PWM(psix, 500)
pwmseven = GPIO.PWM(pseven, 500)
pwmeight = GPIO.PWM(peight, 500)
pwmnine = GPIO.PWM(pnine, 500)
pwmten = GPIO.PWM(pten, 500)

pwm.start(0)
pwmtwo.start(0)
pwmthree.start(0)
pwmfour.start(0)
pwmfive.start(0)
pwmsix.start(0)
pwmseven.start(0)
pwmeight.start(0)
pwmnine.start(0)
pwmten.start(0)

try:
	while True:
		t = time.time() - start
		B = (math.sin(2*math.pi*f*t))**2
		Btwo = (math.sin(2*math.pi*f*t - theta))**2
		Bthree = (math.sin(2*math.pi*f*t - theta*2))**2
		Bfour = (math.sin(2*math.pi*f*t - theta*3))**2
		Bfive = (math.sin(2*math.pi*f*t - theta*4))**2
		Bsix = (math.sin(2*math.pi*f*t - theta*5))**2
		Bseven = (math.sin(2*math.pi*f*t - theta*6))**2
		Beight = (math.sin(2*math.pi*f*t - theta*7))**2
		Bnine = (math.sin(2*math.pi*f*t - theta*8))**2
		Bten = (math.sin(2*math.pi*f*t - theta*9))**2

		duty = B * 100
		dutytwo = Btwo * 100
		dutythree = Bthree * 100
		dutyfour = Bfour * 100
		dutyfive = Bfive * 100
		dutysix = Bsix * 100
		dutyseven = Bseven * 100
		dutyeight = Beight * 100
		dutynine = Bnine * 100
		dutyten = Bten * 100

		pwm.ChangeDutyCycle(duty)
		pwmtwo.ChangeDutyCycle(dutytwo)
		pwmthree.ChangeDutyCycle(dutythree)
		pwmfour.ChangeDutyCycle(dutyfour)
		pwmfive.ChangeDutyCycle(dutyfive)
		pwmsix.ChangeDutyCycle(dutysix)
		pwmseven.ChangeDutyCycle(dutyseven)
		pwmeight.ChangeDutyCycle(dutyeight)
		pwmnine.ChangeDutyCycle(dutynine)
		pwmten.ChangeDutyCycle(dutyten)

except KeyboardInterrupt:
	pass

pwm.stop()
GPIO.cleanup()
