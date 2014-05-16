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
        self.state_green = False
        self.state_yellow = False
        self.state_red = False
        self.state_blue = False
        self.state_white = False

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

    def set_led_green(self, state=-1):
        do_state = not self.state_green
        if state == 1:
            do_state = True
        elif state == 0:
            do_state = False
        self.state_green = do_state
        GPIO.output(LED_GREEN, do_state)

    def set_led_yellow(self, state=-1):
        do_state = not self.state_yellow
        if state == 1:
            do_state = True
        elif state == 0:
            do_state = False
        self.state_yellow = do_state
        GPIO.output(LED_YELLOW, do_state)

    def set_led_red(self, state=-1):
        do_state = not self.state_red
        if state == 1:
            do_state = True
        elif state == 0:
            do_state = False
        self.state_red = do_state
        GPIO.output(LED_RED, do_state)

    def set_led_blue(self, state=-1):
        do_state = not self.state_blue
        if state == 1:
            do_state = True
        elif state == 0:
            do_state = False
        self.state_blue = do_state
        GPIO.output(LED_BLUE, do_state)

    def set_led_white(self, state=-1):
        do_state = not self.state_white
        if state == 1:
            do_state = True
        elif state == 0:
            do_state = False
        self.state_white = do_state
        GPIO.output(LED_WHITE, do_state)

    def cleanup(self):
        self.set_leds(0)
        GPIO.cleanup()


class ButtonThread(threading.Thread):
    """

    """

    def __init__(self, root, pin, name, queue, queue_lock):
        """
        """

        threading.Thread.__init__(self)
        self.root = root  # TODO: need main
        self.pin = pin
        self.name = name
        self.queue = queue
        self.queue_lock = queue_lock
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

    def queue_not_empty(self):
        if not self.queue.empty():
            return True
        return False

    def read_queue(self):

        result = None



class Buttons:

    def __init__(self, root):
        """

        """

        self.root = root
        self.queue = Queue.Queue()
        self.queue_lock = threading.Lock()

        self.btn_threads = []
        self.btn_threads.append(ButtonThread(root, BUTTON_GREEN, "green",
                                             self.queue, self.queue_lock))
        self.btn_threads.append(ButtonThread(root, BUTTON_YELLOW, "yellow",
                                             self.queue, self.queue_lock))
        self.btn_threads.append(ButtonThread(root, BUTTON_RED, "red",
                                             self.queue, self.queue_lock))
        self.btn_threads.append(ButtonThread(root, BUTTON_BLUE, "blue",
                                             self.queue, self.queue_lock))
        self.btn_threads.append(ButtonThread(root, BUTTON_WHITE, "white",
                                             self.queue, self.queue_lock))

    def start_threads(self):
        """

        """

        for t in self.btn_threads:
            t.start()

    def get_last_button_pushed(self):
        """

        """






def main():
    """Init PyBlaster daemon
    """

    led = LED()
    led.reset_leds()

    buttons = Buttons(root=None)
    buttons.start_threads()

    # poll = 0

    while 1:
        prev_in_green = 0
        prev_in_yellow = 0
        prev_in_red = 0
        prev_in_blue = 0
        prev_in_white = 0

        # led.set_leds(poll % 2)

        time.sleep(50./1000.)  # 50ms

        inpt = GPIO.input(BUTTON_GREEN)
        if (not prev_in_green) and inpt:
            print("Green button pressed")
            led.set_led_green()
            prev_in_green = inpt

        inpt = GPIO.input(BUTTON_YELLOW)
        if (not prev_in_yellow) and inpt:
            print("Yellow button pressed")
            led.set_led_yellow()
            prev_in_yellow = inpt

        inpt = GPIO.input(BUTTON_RED)
        if (not prev_in_red) and inpt:
            print("Red button pressed")
            led.set_led_red()
            prev_in_red = inpt

        inpt = GPIO.input(BUTTON_BLUE)
        if (not prev_in_blue) and inpt:
            print("Blue button pressed")
            led.set_led_blue()
            prev_in_blue = inpt

        inpt = GPIO.input(BUTTON_WHITE)
        if (not prev_in_white) and inpt:
            print("White button pressed")
            led.set_led_white()
            prev_in_white = inpt

        # poll += 1

    led.cleanup()


if __name__ == '__main__':
    main()
