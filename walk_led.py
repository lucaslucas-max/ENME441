import time
import random
import RPi.GPIO as GPIO
from shifter import Shifter  # Import your class

# --- Configuration ---
DATA_PIN = 23
CLOCK_PIN = 25
LATCH_PIN = 24
STEP_DELAY = 0.05  # seconds
NUM_LEDS = 8

# --- Instantiate the Shifter object ---
shifter = Shifter(DATA_PIN, CLOCK_PIN, LATCH_PIN)

# --- Initialize the LED position ---
position = NUM_LEDS // 2  # start in the middle

try:
    while True:
        # Create a pattern with one active LED at current position
        pattern = 1 << position
        shifter.shiftByte(pattern)
        
        # Wait for the next step
        time.sleep(STEP_DELAY)
        
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
