""" led.py -- LED GPIO handler for PyBlaster

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import RPi.GPIO as GPIO
import threading
import time

# port number on GPIO in BCM mode
# Do not interfere with DAC+ snd-card:
# ----- hifiberry dac+ config -----
# setgpio 2 ALT0 UP # I2C communication DAC chip
# setgpio 3 ALT0 UP # I2C communication DAC chip
# setgpio 6 INPUT DEFAULT # do not use, reserved for Master clock
# setgpio 18 ALT0 DEFAULT # I2S
# setgpio 19 ALT0 DEFAULT # I2S
# setgpio 20 ALT0 DEFAULT # I2S
# setgpio 21 ALT0 DEFAULT # I2S
# ----- END -----
LED_GREEN = 4
LED_YELLOW = 27
LED_RED = 10
LED_BLUE = 14
LED_WHITE = 23


class LED:
    """LED GPIO handler for PyBlaster"""

    def __init__(self, parent):
        """Initialize GPIO to BCM mode and disable warnings"""

        self.parent = parent
        self.state = [0]*5
        self.init_done = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def reset_leds(self):
        """Assign GPIO ports and turn of LEDs"""

        GPIO.setup(LED_GREEN, GPIO.OUT)
        GPIO.setup(LED_YELLOW, GPIO.OUT)
        GPIO.setup(LED_RED, GPIO.OUT)
        GPIO.setup(LED_BLUE, GPIO.OUT)
        GPIO.setup(LED_WHITE, GPIO.OUT)
        self.init_done = True
        self.set_leds(0)

    def show_init_done(self):
        """Let LEDs flash to indicate that PyBlaster initialization is done"""

        for i in range(1):
            for led in range(5):
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
        if num == 4:
            self.set_led_white(state)

    def set_leds(self, state):
        """Set all LEDs to state"""

        for led in range(4):
            self.set_led(led, state)

    def set_led_green(self, state):
        self.set_led_by_gpio(state, 0, LED_GREEN)

    def set_led_yellow(self, state):
        self.set_led_by_gpio(state, 1, LED_YELLOW)

    def set_led_red(self, state):
        self.set_led_by_gpio(state, 2, LED_RED)

    def set_led_blue(self, state):
        self.set_led_by_gpio(state, 3, LED_BLUE)

    def set_led_white(self, state):
        self.set_led_by_gpio(state, 4, LED_WHITE)

    def toggle_led_yellow(self):
        if self.state[1]:
            self.set_led(1, 0)
        else:
            self.set_led(1, 1)

    def set_led_by_gpio(self, state, stateid, port):
        if not self.init_done:
            return
        GPIO.output(port, state)
        self.state[stateid] = state

    def cleanup(self):
        """Turn of LEDs and close GPIO"""

        self.init_done = False
        self.set_leds(0)
        GPIO.cleanup()

    def flash_led(self, led_code, flash_time):
        """Let a LED flash a certain amount of time and set LED port to LOW
        afterwards.

        Uses threading.Timer with GPIO.output() as callback.
        """

        if not self.init_done:
            # disallow flash if GPIO not initialized
            return
        GPIO.output(led_code, 1)
        timer = threading.Timer(flash_time, GPIO.output, [led_code, 0])
        timer.start()
