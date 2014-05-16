""" led.py -- LED GPIO handler for PyBlaster

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import RPi.GPIO as GPIO
import time

# port number on GPIO in BCM mode
LED_GREEN = 2
LED_YELLOW = 3
LED_RED = 4
LED_BLUE = 17
LED_WHITE = 27

class LED:
    """LED GPIO handler for PyBlaster"""

    def __init__(self, parent):
        """Initialize GPIO to BOARD mode and disable warnings"""

        self.parent = parent
        self.state = [0]*4

        GPIO.setmode(GPIO.BCM)
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

        if num == 0:
            self.set_led_green(state)
        if num == 1:
            self.set_led_yellow(state)
        if num == 2:
            self.set_led_red(state)
        if num == 3:
            self.set_led_blue(state)

    def set_leds(self, state):
        """Set all LEDs to state"""

        for led in range(4):
            self.set_led(led, state)

    def set_led_green(self, state):
        GPIO.output(LED_GREEN, state)
        self.state[0] = state

    def set_led_yellow(self, state):
        GPIO.output(LED_YELLOW, state)
        self.state[1] = state

    def set_led_red(self, state):
        GPIO.output(LED_RED, state)
        self.state[2] = state

    def set_led_blue(self, state):
        GPIO.output(LED_BLUE, state)
        self.state[3] = state

    def toggle_led_yellow(self):
        if self.state[1]:
            self.set_led(1, 0)
        else:
            self.set_led(1, 1)

    def cleanup(self):
        """Turn of LEDs and close GPIO"""

        self.set_leds(0)
        GPIO.cleanup()
