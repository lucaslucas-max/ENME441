# bugclass.py
import time
import random
import RPi.GPIO as GPIO
from shifter import Shifter

class Bug:
    def __init__(self, timestep=0.1, x=3, isWrapOn=False):
        """
        timestep: time step size in seconds
        x: initial LED position (0–7)
        isWrapOn: if True, LED wraps around edges
        """
        self.timestep = timestep
        self.x = x
        self.isWrapOn = isWrapOn

        # Private Shifter object for LED control
        DATA, LATCH, CLOCK = 23, 24, 25
        self.__shifter = Shifter(DATA, CLOCK, LATCH)

        # Control flag for running loop
        self._running = False

    def __update_display(self):
        """Private: update the LEDs to show the current position."""
        pattern = 1 << self.x
        self.__shifter.shiftByte(pattern)

    def start(self):
        """Start moving the LED in a random walk."""
        self._running = True
        try:
            while self._running:
                self.__update_display()
                time.sleep(self.timestep)

                # Move LED left or right randomly
                move = random.choice([-1, 1])
                self.x += move

                if self.isWrapOn:
                    # Wrap around edges
                    self.x %= 8
                else:
                    # Keep LED inside range
                    if self.x < 0:
                        self.x = 0
                    elif self.x > 7:
                        self.x = 7
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop movement and clear LEDs."""
        self._running = False
        self.__shifter.shiftByte(0b00000000)
        GPIO.cleanup()
