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

    def __init__(self, root, pin, name, queue, queue_lock):
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
        self.pin = pin
        self.name = name
        self.queue = queue
        self.queue_lock = queue_lock

    def run(self):
        """Read button while keep_run in root object is true
        """

        GPIO.setup(self.pin, GPIO.IN)

        prev_in = 0
        while self.root.keep_run:
            time.sleep(0.01)  # TODO: to config
            inpt = GPIO.input(self.pin)
            if (not prev_in) and inpt:
                self.queue_lock.acquire()
                self.queue.put([self.pin, self.name])
                self.queue_lock.release()

            prev_in = inpt

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
        """Let each button thread start.

        Not called in __init__() because of GPIO init.
        """
        for t in self.btn_threads:
            t.start()

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


