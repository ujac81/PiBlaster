"""mpc.py -- Manage connection to MusicPlayerDaemon

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

from mpd import MPDClient
import Queue
import threading
import time

import log


class MPDIdler(threading.Thread):

    def __init__(self, main, queue, queue_lock):
        """

        :param main:
        :param queue:
        :param queue_lock:
        :return:
        """

        threading.Thread.__init__(self)

        self.main = main
        self.queue = queue
        self.queue_lock = queue_lock
        self.client = None

    def connect(self):
        """

        :return:
        """
        self.client = MPDClient()
        self.client.timeout = 10
        self.client.connect('localhost', 6600)

    def run(self):
        """

        :return:
        """

        self.connect()

        while self.main.keep_run:
            res = self.client.idle()
            self.queue_lock.acquire()
            self.queue.put(res)
            self.queue_lock.release()

        self.client.disconnect()


class MPC:
    """

    """

    def __init__(self, main):
        """

        :param main:
        :return:
        """

        self.main = main
        self.client = None
        self.queue = Queue.Queue()
        self.queue_lock = threading.Lock()
        self.idler = MPDIdler(self.main, self.queue, self.queue_lock)

    def connect(self):
        """

        :return:
        """

        self.client = MPDClient()
        self.client.timeout = 10
        self.client.connect('localhost', 6600)
        self.idler.start()

    def has_idle_event(self):
        """True if idler events in queue
        """
        if not self.queue.empty():
            return True
        return False

    def process_event(self):
        """

        :return:
        """
        self.queue_lock.acquire()
        try:
            event = self.queue.get_nowait()
        except Queue.Empty:
            self.queue_lock.release()
            return
        self.queue_lock.release()

        self.main.log.write(log.MESSAGE, "[MPD event]: %s" % event)

    def join(self):
        """Join all button threads after keep_run in root is False.
        """
        self.idler.join()

