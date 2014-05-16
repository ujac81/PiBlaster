#!/usr/bin/env python
""" pyblaster.py -- Daemon for PiBlaster project

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""
import os
import signal
import time

import log
from buttons import Buttons
from dbhandle import DBHandle
from evalcmd import EvalCmd
from led import LED
from lircthread import LircThread
from log import Log
from play import Play
from playlistmanager import PlayListManager
from rfcommserver import RFCommServer
from settings import Settings
from usbmanager import UsbManager


class PyBlaster:
    """Daemon for PiBlaster project"""

    def __init__(self):
        """Whole project is run from this constructor
        """

        # +++++++++++++++ Init +++++++++++++++ #

        self.keep_run = 0  # used in run for daemon loop, reset by SIGTERM

        self.log = Log(self)
        self.settings = Settings(self)
        self.led = LED(self)
        self.dbhandle = DBHandle(self)
        self.usb = UsbManager(self)
        self.rfcomm = RFCommServer(self)
        self.cmd = EvalCmd(self)
        self.listmngr = PlayListManager(self)
        self.play = Play(self)
        self.lirc = LircThread(self)
        self.buttons = Buttons(self)
        self.keep_run = 1

        self.led.reset_leds()

        # invoke arg parser and parse config or create new config if not found
        self.settings.parse()

        # check if we can load database, create otherwise
        self.dbhandle.dbconnect()

        # load connected usb before bluetooth
        self.usb.check_new_usb()

        # load latest playlist from database
        self.listmngr.load_active_playlist()

        # open cmd fifo to read commands
        self.cmd.open_fifo()

        # fire up bluetooth service
        self.rfcomm.start_server()

        # start lirc thread
        self.lirc.start()

        # fire up one thread per each button
        self.buttons.start_threads()

        # +++++++++++++++ Daemoninze +++++++++++++++ #

        self.check_pidfile()
        self.daemonize()
        self.create_pidfile()

        self.led.show_init_done()

        # +++++++++++++++ Daemon loop +++++++++++++++ #

        self.run()

        # +++++++++++++++ Finalize +++++++++++++++ #

        self.listmngr.save_active()
        self.led.cleanup()
        self.delete_pidfile()

    def run(self):
        """Daemon loop"""

        # Expensive operations like new usb drive check
        # should not be run every loop run.
        poll_count = 0

        # -e flag is set, run only init and exit directly.
        self.keep_run = 0 if self.settings.exitafterinit else 1

        reset_poll_count = self.settings.keep_alive_count * \
                           self.settings.usb_count

        # # # # # # DAEMON LOOP ENTRY # # # # # #

        while self.keep_run:

            poll_count += 1

            # Check cmd fifo for new commands.
            self.cmd.read_fifo()

            # Check button events
            self.buttons.read_buttons()

            # Check bluetooth channel for new messages/connections.
            self.rfcomm.read_socket()

            # Check if lirc thread has command in queue
            if self.lirc.queue_not_empty():
                ircmd = self.lirc.read_command()
                if ircmd is not None:
                    self.cmd.evalcmd(ircmd, "lirc")

            # Check if song has ended
            self.play.check_pygame_events()

            # read bluetooth has internal BT timeout of 1sec,
            # but if connection got lost, fast polling will occur.
            time.sleep(self.settings.polltime / 1000.)  # 30ms default in
                                                        # config
            self.led.set_led_green((poll_count/10) % 2)

            # Check for new USB drives.
            if poll_count % self.settings.usb_count == 0:
                # If new usb device found, new usbdev instance will be created,
                # including dir and mp3 entries.
                # If usb device got lost, all its entries will be removed.
                self.usb.check_new_usb()

            # Multiple of all poll counts reached:
            # may reset poll count at reset_poll_count.
            if poll_count >= reset_poll_count:
                poll_count = 0

            # end daemon loop #

        # # # # # # DAEMON LOOP EXIT # # # # # #

        # join remaining threads
        self.lirc.join()

        self.log.write(log.MESSAGE, "---- closed regularly ----")

    # end run() #

    def daemonize(self):
        """Fork process and disable print in log object"""

        signal.signal(signal.SIGTERM, self.term_handler)
        signal.signal(signal.SIGINT, self.term_handler)

        if not self.settings.daemonize:
            self.log.init_log()
            return

        self.log.write(log.DEBUG1, "daemonizing")

        try:
            pid = os.fork()
        except OSError:
            self.log.write(log.EMERGENCY, "Failed to fork daemon")
            raise

        if ( pid == 0 ):
            os.setsid()
            try:
                pid = os.fork()
            except OSError:
                self.log.write(log.EMERGENCY, "Failed to fork daemon")
                raise

            if ( pid == 0 ):
                os.chdir("/tmp")
                os.umask(0)
            else:
                os._exit(0)
        else:
            os._exit(0)

        self.settings.is_daemonized = True
        self.log.init_log()
        self.log.write(log.MESSAGE, "daemonized.")

    # end daemonize() #

    def term_handler(self, *args):
        """ Signal handler to stop daemon loop"""
        self.keep_run = 0

    def check_pidfile(self):
        """Check if daemon already running, throw if pid file found"""

        if os.path.exists(self.settings.pidfile):
            self.log.write(log.EMERGENCY, "Found pid file for pyblaster, "\
                           "another process running?")
            raise Exception("pid file found")

    def create_pidfile(self):
        """Write getpid() to file after daemonize()"""

        try:
            fpid = open(self.settings.pidfile, "w")
        except IOError:
            self.log.write(log.EMERGENCY, "failed to create pidfile %s" %
                           self.settings.pidfile)
            raise

        fpid.write("%s\n" % os.getpid())

    def delete_pidfile(self):
        """Try to remove pid file after daemon should exit"""

        if os.path.exists(self.settings.pidfile):
            try:
                os.remove(self.settings.pidfile)
            except OSError:
                self.log.write(log.EMERGENCY, "failed to remove pidfile %s" %
                               self.settings.pidfile)
                raise

    def kill_other_pyblaster(self):
        """Check if pid found in pid file and try to kill this (old) process"""

        if not os.path.exists(self.settings.pidfile): return

        try:
            f = open(self.settings.pidfile, "r")
        except IOError:
            self.log.write(log.EMERGENCY, "failed to read pidfile %s" %
                           self.settings.pidfile)
            raise

        pid = int(f.readline().strip())

        print("Trying to kill old process with pid %s..." % pid)

        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            self.log.write(log.EMERGENCY,
                           "failed to kill process with pid %s" % pid)
            raise

        exit(0)

        # end kill_other_pyblaster() #


if __name__ == '__main__':
    blaster = PyBlaster()

