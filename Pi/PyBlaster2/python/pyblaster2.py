#!/usr/bin/env python2
""" pyblaster.py -- Daemon for PiBlaster project

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import os
import signal
import time

import log

from cmd import Cmd
from gpio import PB_GPIO, LED, Buttons
from log import Log
from mpc import MPC
from settings import Settings
from sql import DBHandle


class PyBlaster:
    """Daemon for PiBlaster project"""

    def __init__(self):
        """Whole project is run from this constructor
        """

        # +++++++++++++++ Init +++++++++++++++ #

        self.keep_run = 1  # used in run for daemon loop, reset by SIGTERM
        self.ret_code = 0  # return code to command line (10 = shutdown)

        # +++++++++++++++ Objects +++++++++++++++ #

        # Each inner object will get reference to PyBlaster as self.main.

        self.log = Log(self)
        self.settings = Settings(self)
        PB_GPIO.init_gpio()
        self.led = LED(self)
        self.buttons = Buttons(self)
        self.dbhandle = DBHandle(self)
        self.cmd = Cmd(self)
        self.mpc = MPC(self)

        # +++++++++++++++ Init Objects +++++++++++++++ #

        # Make sure to run init functions in proper order!
        # Some might depend upon others ;)

        self.led.reset_leds()
        self.settings.parse()
        self.dbhandle.dbconnect()
        self.mpc.connect()

        # +++++++++++++++ Daemoninze +++++++++++++++ #

        self.check_pidfile()
        self.daemonize()
        self.create_pidfile()

        # +++++++++++++++ Daemon loop +++++++++++++++ #

        self.led.show_init_done()
        self.buttons.start()
        self.run()

        # +++++++++++++++ Finalize +++++++++++++++ #

        self.log.write(log.MESSAGE, "Joining threads...")

        # join remaining threads
        self.buttons.join()
        self.mpc.join()

        self.log.write(log.MESSAGE, "leaving...")

        # cleanup
        self.mpc.exit_client()
        self.delete_pidfile()
        PB_GPIO.cleanup()

    def run(self):
        """Daemon loop"""

        # Expensive operations like new usb drive check
        # should not be run every loop run.
        poll_count = 0
        led_count = 1

        # -e flag is set, run only init and exit directly.
        # self.keep_run = 0 if self.settings.exitafterinit else 1

        # # # # # # DAEMON LOOP ENTRY # # # # # #

        self.log.write(log.MESSAGE, "Entering daemon loop...")

        while self.keep_run:

            poll_count += 1

            time.sleep(30. / 1000.)  # 30ms default in config

            if self.buttons.has_button_events():
                self.buttons.read_buttons()

            if self.mpc.has_idle_event():
                self.mpc.process_event()

            # TODO: play LEDs while playing -- if paused, do something else...

            if poll_count % 10 == 0:
                self.led.play_leds(led_count)
                led_count += 1


            # end daemon loop #

        # # # # # # DAEMON LOOP EXIT # # # # # #

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
            # self.log.write(log.EMERGENCY, "Failed to fork daemon")
            raise

        if pid == 0:
            os.setsid()
            try:
                pid = os.fork()
            except OSError:
                # self.log.write(log.EMERGENCY, "Failed to fork daemon")
                raise

            if pid == 0:
                os.chdir("/tmp")
                os.umask(0)
            else:
                exit(0)
        else:
            exit(0)

        self.settings.is_daemonized = True
        self.log.init_log()
        self.log.write(log.MESSAGE, "daemonized.")

    def term_handler(self, *args):
        """ Signal handler to stop daemon loop"""
        self.log.write(log.MESSAGE, "Got TERM or INT signal -- leaving!")
        self.keep_run = 0

    def check_pidfile(self):
        """Check if daemon already running, throw if pid file found"""

        if os.path.exists(self.settings.pidfile):
            self.log.write(log.EMERGENCY, "Found pid file for pyblaster, "
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

        if not os.path.exists(self.settings.pidfile):
            return

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


if __name__ == '__main__':
    blaster = PyBlaster()
