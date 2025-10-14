import time
import random
import RPi.GPIO as GPIO
from shifter import Shifter  

DATA_PIN = 23
CLOCK_PIN = 25
LATCH_PIN = 24
NUM_LEDS = 8

shifter = Shifter(DATA_PIN, CLOCK_PIN, LATCH_PIN)
position = NUM_LEDS // 2 

try:
    while True:
        pattern = 1 << position
        shifter.shiftByte(pattern)
    
        time.sleep(0.05)
        
        # Randomly move left (-1) or right (+1)
        move = random.choice([-1, 1])
        position += move
        
        # Prevent going beyond the edges
        if position < 0:
            position = 0
        elif position >= NUM_LEDS:
            position = NUM_LEDS - 1

except KeyboardInterrupt:
    GPIO.cleanup()
