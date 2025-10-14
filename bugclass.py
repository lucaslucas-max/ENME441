import time
import random
import RPi.GPIO as GPIO
from shifter import Shifter

class Bug:
  def __init__(self, timestep=0.1, x=3, isWrapOn= False):
    self.timestep = timestep
    self.x = x
    self.isWrapOn = False

    Data = 23
    Latch = 24
    Clock = 25
    self.__Shifter = Shifter(Data, Clock, Latch)

    self._running = False

  def display(self):
    pattern = 1 << self.x
    self.__shifter.shiftByte(pattern)

  def start(self):
    self._running = True
    try:
      while self._running:
        self.__update_display()
        time.sleep(self.timestep)
        move = random.choice([-1, 1])
        self.x += move
        if self.x < 0:
          self.x = 0
        elif self.x > 7:
          self.x = 7

    except KeyboardInterrupt:
      self.stop()

def stop(self):
  self._running = False
  self.__shifter.shiftByte(0b00000000)
  GPIO.cleanup()
