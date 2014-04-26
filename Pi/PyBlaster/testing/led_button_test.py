""" led_button_test.py -- test suite for LED push buttons


@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import Queue
import RPi.GPIO as GPIO
import threading
import time

LED_GREEN = 2
LED_YELLOW = 3
LED_RED = 4
LED_BLUE = 17
LED_WHITE = 27

BUTTON_GREEN = 14
BUTTON_YELLOW = 15
BUTTON_RED = 18
BUTTON_BLUE = 23
BUTTON_WHITE = 24


class LED:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def reset_leds(self):
        """Assign GPIO ports and turn of LEDs"""

        GPIO.setup(LED_GREEN, GPIO.OUT)
        GPIO.setup(LED_YELLOW, GPIO.OUT)
        GPIO.setup(LED_RED, GPIO.OUT)
        GPIO.setup(LED_BLUE, GPIO.OUT)
        GPIO.setup(LED_WHITE, GPIO.OUT)
        self.set_leds(0)

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
        for led in range(5):
            self.set_led(led, state)

    def set_led_green(self, state):
        GPIO.output(LED_GREEN, state)

    def set_led_yellow(self, state):
        GPIO.output(LED_YELLOW, state)

    def set_led_red(self, state):
        GPIO.output(LED_RED, state)

    def set_led_blue(self, state):
        GPIO.output(LED_BLUE, state)

    def set_led_white(self, state):
        GPIO.output(LED_WHITE, state)

    def cleanup(self):
        self.set_leds(0)
        GPIO.cleanup()


class ButtonThread(threading.Thread):
    """

    """

    def __init__(self, main, pin, name, queue, queue_lock):
        """"

        """"

        threading.Thread.__init__(self)
        self.main = main
        self.pin = pin
        self.name = name
        self.queue = queue
        self.queue_lock = queue_lock
        self.main = None  # TODO: need main
        self.keep_run = 1  # TODO: via main

    def run(self):
        """

        """

        GPIO.setup(self.pin, GPIO.IN)

        prev_in = 0
        while self.keep_run:  # TODO: via main
            time.sleep(0.01)
            inpt = GPIO.input(self.pin)
            if (not prev_in) and inpt:
                self.queue_lock.acquire()
                self.queue.put([self.pin, self.name])
                self.queue_lock.release()

            prev_in = inpt

    # end run()


class Buttons:

    def __init__(self, main):
        """

        """

        self.main = main
        self.queue = Queue.Queue()
        self.queue_lock = threading.Lock()

        self.btn_threads = []
        self.btn_threads.append(ButtonThread(main, BUTTON_GREEN, "green",
                                             self.queue, self.queue_lock))
        self.btn_threads.append(ButtonThread(main, BUTTON_YELLOW, "yellow",
                                             self.queue, self.queue_lock))
        self.btn_threads.append(ButtonThread(main, BUTTON_RED, "red",
                                             self.queue, self.queue_lock))
        self.btn_threads.append(ButtonThread(main, BUTTON_BLUE, "blue",
                                             self.queue, self.queue_lock))
        self.btn_threads.append(ButtonThread(main, BUTTON_WHITE, "white",
                                             self.queue, self.queue_lock))

    def start_threads(self):
        """

        """

        for t in self.btn_threads:
            t.start()






def main():
    """Init PyBlaster daemon
    """

    led = LED()
    led.reset_leds()

    button = Button()

    poll = 0

    prev_in = 0

    while 1:
        led.set_leds(poll % 2)
        time.sleep(500./1000.)  # 500ms

        inpt = GPIO.input(BUTTON_RED)
        if (not prev_in) and inpt:
            print("Button pressed")

        prev_in = inpt
        poll += 1



    led.cleanup()

if __name__ == '__main__':
    main()
