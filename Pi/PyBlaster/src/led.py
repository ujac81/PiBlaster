""" led.py -- LED GPIO handler for PyBlaster

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import RPi.GPIO as GPIO
import time

# port number on GPIO in BOARD mode
LED_GREEN = 12
LED_YELLOW = 16
LED_RED = 18
LED_BLUE = 22

class LED:
    """LED GPIO handler for PyBlaster"""

    def __init__(self, parent):
        """Initialize GPIO to BOARD mode and disable warnings"""

        self.parent = parent

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

    def reset_leds(self):
        """Assign GPIO ports and turn of LEDs"""

        GPIO.setup(LED_GREEN, GPIO.OUT)
        GPIO.setup(LED_YELLOW, GPIO.OUT)
        GPIO.setup(LED_RED, GPIO.OUT)
        GPIO.setup(LED_BLUE, GPIO.OUT)
        self.set_leds(0)

    def show_init_done(self):
        """Let LEDs flash to indicate that PyBlaster initialization is done"""

        for i in range(1):
            for led in range(4):
                self.set_led(led, 1)
                time.sleep(0.1)
                self.set_led(led, 0)

    def set_led(self, num, state):
        """Set specific LED to state"""

        if num == 0: self.set_led_green(state)
        if num == 1: self.set_led_yellow(state)
        if num == 2: self.set_led_red(state)
        if num == 3: self.set_led_blue(state)

    def set_leds(self, state):
        """Set all LEDs to state"""

        for led in range(4):
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
        """Turn of LEDs and close GPIO"""

        self.set_leds(0)
        GPIO.cleanup()

