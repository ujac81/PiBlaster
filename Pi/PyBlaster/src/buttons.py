""" buttons.py -- GPIO handler for push buttons

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import Queue
import RPi.GPIO as GPIO
import threading
import time

import log

# port number on GPIO in BCM mode
BUTTON_GREEN = 14
BUTTON_YELLOW = 15
BUTTON_RED = 18
BUTTON_BLUE = 23
BUTTON_WHITE = 24


class ButtonThread(threading.Thread):
    """Check if button pressed and push press events into queue -- threaded
    """

    def __init__(self, root, pins, names, queue, queue_lock):
        """Init thread object

        Do not init GPIO pin here, might not be initialized.

        :param root: PyBlaster main object
        :param pin: GPIO port number in BCM mode
        :param name: Name of the button for queuing
        :param queue: queue object to push pressed events into
        :param queue_lock: lock queue while insertion
        """

        threading.Thread.__init__(self)
        self.root = root
        self.pins = pins
        self.names = names
        self.queue = queue
        self.queue_lock = queue_lock
        self.prev_in = [0] * len(self.pins)

    def run(self):
        """Read button while keep_run in root object is true
        """

        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN)

        while self.root.keep_run:
            time.sleep(0.05)  # TODO: to config
            for i in range(len(self.pins)):
                inpt = GPIO.input(self.pins[i])
                if (not self.prev_in[i]) and inpt:
                    self.queue_lock.acquire()
                    self.queue.put([self.pins[i], self.names[i]])
                    self.queue_lock.release()
                self.prev_in[i] = inpt

                # Blue and white buttons are vol up and down.
                # These should have hold functionality.
                if self.pins[i] == BUTTON_BLUE or self.pins[i] == BUTTON_WHITE:
                    self.prev_in[i] = 0

    # end run()

# end class ButtonThread #


class Buttons:
    """Manage one thread for each button.
    """

    def __init__(self, root):
        """Create one thread for each push button using name and GPIO port
        """

        self.root = root
        self.queue = Queue.Queue()  # use one queue for all buttons
        self.queue_lock = threading.Lock()

        self.btn_thread = \
            ButtonThread(root, [BUTTON_GREEN, BUTTON_YELLOW, BUTTON_RED,
                                BUTTON_BLUE, BUTTON_WHITE],
                         ["green", "yellow", "red", "blue", "white"],
                         self.queue, self.queue_lock)

    def start(self):
        """Let each button thread start.

        Not called in __init__() because of GPIO init.
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

    # end read_last_button_event() #

    def read_buttons(self):
        """

        """

        event = self.read_last_button_event()
        if event is None:
            return

        button_color = event[1]
        self.root.log.write(log.MESSAGE, "--- Button \"%s\" pressed" %
                                         button_color)

        if button_color == "green":
            self.root.cmd.evalcmd("playpause", "button")
        if button_color == "yellow":
            self.root.cmd.evalcmd("playnext", "button")
        if button_color == "red":
            self.root.cmd.evalcmd("poweroff", "button")
        if button_color == "blue":
            self.root.cmd.evalcmd("volinc", "button")
        if button_color == "white":
            self.root.cmd.evalcmd("voldec", "button")
