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
        """Private method to toggle a pin high then low."""
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0)
        GPIO.output(pin, GPIO.LOW)
    
    def shiftByte(self, data):
        """Shift out one byte of data to the shift register."""
        for i in range(8):
            GPIO.output(self.serialPin, (data >> i) & 1)
            self._ping(self.clockPin)
        self._ping(self.latchPin)

# --- Example usage ---
if __name__ == "__main__":
    try:
        dataPin, latchPin, clockPin = 23, 24, 25
        shifter = Shifter(dataPin, clockPin, latchPin)
        
        pattern = 0b01100110
        shifter.shiftByte(pattern)
        
        # Keep running
        while True:
            pass
    except KeyboardInterrupt:
        GPIO.cleanup()
