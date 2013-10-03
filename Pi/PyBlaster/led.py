""" led.py LED GPIO handler for PyBlaster

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""


import RPi.GPIO as GPIO
import time

LED_GREEN = 12
LED_YELLOW = 16
LED_RED = 18
LED_BLUE = 22


class LED:
  """
  """

  def __init__(self, parent):
    """
    """
    self.parent = parent

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

  def reset_leds(self):
    """
    """
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.setup(LED_YELLOW, GPIO.OUT)
    GPIO.setup(LED_RED, GPIO.OUT)
    GPIO.setup(LED_BLUE, GPIO.OUT)
    self.set_leds(0)

  def show_init_done(self):
    for i in range(1):
      for led in range(4):
        self.set_led(led, 1)
        time.sleep(0.1)
        self.set_led(led, 0)

  def set_led(self, num, state):
    if num == 0: self.set_led_green(state)
    if num == 1: self.set_led_yellow(state)
    if num == 2: self.set_led_red(state)
    if num == 3: self.set_led_blue(state)

  def set_leds(self, state):
    for led in range(3):
      self.set_led(led, state)

  def set_led_green(self, state):
    GPIO.output(LED_GREEN, state)

  def set_led_yellow(self, state):
    GPIO.output(LED_YELLOW, state)

  def set_led_red(self, state):
    GPIO.output(LED_RED, state)

  def set_led_blue(self, state):
    GPIO.output(LED_BLUE, state)

  def cleanup(self):
    """
    """
    self.set_leds(0)

    GPIO.cleanup()

