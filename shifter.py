import RPi.GPIO as GPIO
import time

class Shifter:
    def __init__(self, serialPin, clockPin, latchPin):
        self.serialPin = serialPin
        self.clockPin = clockPin
        self.latchPin = latchPin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.serialPin, GPIO.OUT)
        GPIO.setup(self.clockPin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.latchPin, GPIO.OUT, initial=GPIO.LOW)
    
    def _ping(self, pin):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0)
        GPIO.output(pin, GPIO.LOW)
    
    def shiftByte(self, data):
        for i in range(8):
            GPIO.output(self.serialPin, (data >> i) & 1)
            self._ping(self.clockPin)
        self._ping(self.latchPin)

        GPIO.cleanup()
