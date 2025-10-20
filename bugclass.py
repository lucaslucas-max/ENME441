import RPi.GPIO as GPIO
import random
import time
GPIO.setmode(GPIO.BCM)

class shifter:
    def __init__(self, serialPin, latchPin, clockPin):
        self.serialPin = serialPin
        self.latchPin = latchPin
        self.clockPin = clockPin

        GPIO.setup(self.serialPin, GPIO.OUT)
        GPIO.setup(self.latchPin, GPIO.OUT, initial=0) 
        GPIO.setup(self.clockPin, GPIO.OUT, initial=0)
        
    def ping(self, p): 
        GPIO.output(p,1)
        time.sleep(0)
        GPIO.output(p,0)

    def shiftByte(self, b):
        for i in range(8):
            GPIO.output(self.serialPin, b & (1<<i))
            self.ping(self.clockPin)
        self.ping(self.latchPin) 

class Bug:
    def __init__(self, __shifter, timestep = 0.1, x = 3, isWrapOn = False):
        self.timestep = timestep 
        self.x = x 
        self.isWrapOn = isWrapOn
        self.__shifter = __shifter
        self.running = False
    
    def move(self):
        if not self.running:
            return
        pattern = 1 << self.x
        self.__shifter.shiftByte(pattern)
        time.sleep(self.timestep)

    
        step = random.choice([-1, 1])
        self.x += step

        if self.isWrapOn:
            self.x %= 8
        else:
            if self.x < 0:
                self.x = 0
            elif self.x > 7:
                self.x = 7
        
    def stop(self):
        self.running = False
        self.__shifter.shiftByte(0b00000000)
