# bugclass.py
import time
import random
import RPi.GPIO as GPIO
from shifter import Shifter
import threading

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

        # Control flags
        self._running = False
        self._thread = None

    def __update_display(self):
        """Private: update the LEDs to show the current position."""
        pattern = 1 << self.x
        self.__shifter.shiftByte(pattern)

    def __run(self):
        """Private thread loop for movement."""
        try:
            while self._running:
                self.__update_display()
                time.sleep(self.timestep)

                # Move LED left or right randomly
                move = random.choice([-1, 1])
                self.x += move

                if self.isWrapOn:
                    self.x %= 8
                else:
                    if self.x < 0:
                        self.x = 0
                    elif self.x > 7:
                        self.x = 7
        except Exception as e:
            print("Error in bug thread:", e)
        finally:
            self.__shifter.shiftByte(0b00000000)

    def start(self):
        """Start movement in a new thread."""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self.__run, daemon=True)
            self._thread.start()

    def stop(self):
        """Stop movement and clear LEDs."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=0.5)
        self.__shifter.shiftByte(0b00000000)
