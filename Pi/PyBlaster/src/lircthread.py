"""lircthread.py -- Thread to read remote controller via lirc

"""

import Queue
import lirc
import threading
import time


class LircThread(threading.Thread):
    """

    """

    def __init__(self, main):
        """

        """
        threading.Thread.__init__(self)
        self.main = main
        self.queue = Queue.Queue()
        self.queue_lock = threading.Lock()

        self.lircsock = None

    # end __init__() #

    def run(self):
        """

        """
        #if not self.main.settings.use_lirc:
        #    return

        self.lircsock = lirc.init("pyblaster", "/root/.lircrc",
                                  blocking=False)

        while self.main.keep_run:
            read = lirc.nextcode()
            if len(read):
                self.queue_lock.acquire()
                self.queue.put(read[0])
                self.queue_lock.release()
            time.sleep(self.main.settings.polltime / 1000.)

        lirc.deinit()

    # end run() #

    def queue_not_empty(self):
        if not self.queue.empty():
            return True
        return False

    def read_command(self):
        """dry run queue and return last command if such -- None else
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
