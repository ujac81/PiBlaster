"""gpio.py -- Handle LED and buttons for PyBlaster.

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import Queue
import RPi.GPIO as GPIO
import threading
import time

import log

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
LED_GREEN = 15
LED_YELLOW = 24
LED_RED = 12
LED_BLUE = 17
LED_WHITE = 11

BUTTON_GREEN = 14
BUTTON_YELLOW = 23
BUTTON_RED = 25
BUTTON_BLUE = 27
BUTTON_WHITE = 9


class PB_GPIO:
    """Prepare GPIOs for PyBlaster"""

    @staticmethod
    def init_gpio():
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    @staticmethod
    def cleanup():
        GPIO.cleanup()


class LED:
    """LED GPIO handler for PyBlaster"""

    def __init__(self, main):
        """Initialize GPIO to BCM mode and disable warnings"""

        self.main = main
        self.state = [0]*5
        self.init_done = False

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

        for led in range(5):
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

        if state == 1:
            self.state[stateid] += 1
            GPIO.output(port, 1)
        elif state == 0:
            self.state[stateid] -= 1
        if self.state[stateid] <= 0:
            self.state[stateid] = 0
            GPIO.output(port, 0)

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

    def play_leds(self, count):
        """

        :param count:
        :return:
        """
        self.set_led((count-1) % 5, 0)
        self.set_led(count % 5, 1)


class ButtonThread(threading.Thread):
    """Check if button pressed and push press events into queue -- threaded

    Created by Buttons.
    """

    def __init__(self, main, pins, names, queue, queue_lock):
        """Init thread object

        Do not init GPIO pin here, might not be initialized.

        :param main: PyBlaster main object
        :param pins: GPIO port numbers in BCM mode
        :param names: Names of the button for queuing
        :param queue: queue object to push pressed events into
        :param queue_lock: lock queue while insertion
        """

        threading.Thread.__init__(self)
        self.main = main
        self.pins = pins
        self.names = names
        self.queue = queue
        self.queue_lock = queue_lock
        # Remember button state if button is pressed longer than one poll.

        # CAUTION: depending on your wiring and on some other unknown
        # circumstances, a released button might be in HIGH or LOW state.
        # For my wiring it's HIGH (1), so I need to invert all
        # "button pressed" logics. If your buttons are in LOW state, invert
        # all boolean conditions.
        self.prev_in = [1] * len(self.pins)  # init for released buttons

    def run(self):
        """Read button while keep_run in root object is true
        """

        for i in range(len(self.pins)):
            GPIO.setup(self.pins[i], GPIO.IN)
            self.prev_in[i] = GPIO.input(self.pins[i])

        while self.main.keep_run:
            time.sleep(0.01)  # TODO: to config
            for i in range(len(self.pins)):
                inpt = GPIO.input(self.pins[i])
                if self.prev_in[i] != inpt:
                    if inpt:
                        print("Btn %d (%d) released" % (i, self.pins[i]))
                    else:
                        print("Btn %d (%d) pressed" % (i, self.pins[i]))
                    # self.queue_lock.acquire()
                    # self.queue.put([self.pins[i], self.names[i]])
                    # self.queue_lock.release()
                self.prev_in[i] = inpt

                # # Blue and white buttons are vol up and down.
                # # These should have hold functionality.
                # if self.pins[i] == BUTTON_BLUE or self.pins[i] == BUTTON_WHITE:
                #     self.prev_in[i] = 1

        self.main.log.write(log.MESSAGE, "[THREAD] Button reader leaving...")


class Buttons:
    """Manage button thread and check if any button sent command to queue.

    Button thread will read button state every 0.0X seconds and queue
    changed state to this object's queue.
    Main loop will ask this object for button events and invoke read_buttons()
    if such.
    """

    def __init__(self, main):
        """Create thread for push buttons using names and GPIO ports

        Thread is not started from here -- need to wait until LED class
        initialized GPIO.
        """

        self.main = main
        self.queue = Queue.Queue()  # use one queue for all buttons
        self.queue_lock = threading.Lock()

        self.btn_thread = \
            ButtonThread(main,
                         [BUTTON_GREEN, BUTTON_YELLOW, BUTTON_RED,
                          BUTTON_BLUE, BUTTON_WHITE],
                         ["green", "yellow", "red", "blue", "white"],
                         self.queue, self.queue_lock)

    def start(self):
        """Let each button thread start.

        Not called in __init__() because of later GPIO init in LED class.
        """
        self.btn_thread.start()

    def join(self):
        """Join all button threads after keep_run in root is False.
        """
        self.btn_thread.join()

    def has_button_events(self):
        """True if button events in queue
        """
        if not self.queue.empty():
            return True
        return False

    def read_last_button_event(self):
        """dry run queue and return last command if such -- None else

        :returns: None if no push event or [pin, button_name]
        """
        result = None

        while not self.queue.empty():
            self.queue_lock.acquire()
            try:
                result = self.queue.get_nowait()
            except Queue.Empty:
                self.queue_lock.release()
                return None
            self.queue_lock.release()

        return result

    def read_buttons(self):
        """Execute command if button event found.

        Called by main loop if has_button_events() is true.
        """
        event = self.read_last_button_event()
        if event is None:
            return

        button_color = event[1]
        self.main.log.write(log.MESSAGE, "--- Button \"%s\" pressed" %
                                         button_color)

        if button_color == "green":
            self.main.cmd.eval("playpause", "button")
        if button_color == "yellow":
            self.main.cmd.eval("playnext", "button")
        if button_color == "red":
            self.main.cmd.eval("poweroff", "button")
        if button_color == "blue":
            self.main.cmd.eval("volinc", "button")
        if button_color == "white":
            self.main.cmd.eval("voldec", "button")
