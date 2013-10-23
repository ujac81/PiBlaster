#!/usr/bin/env python
""" pyblaster.py daemon for PiBlaster project

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""


import log
from log import Log
from led import LED
from usbmanager import UsbManager
from settings import Settings
from dbhandle import DBHandle
from rfcommserver import RFCommServer
from evalcmd import EvalCmd

import sys, os, time, signal


class PyBlaster:
  """
  """

  def __init__(self):
    """whole project is run from this constructor
    """

    # +++++++++++++++ Init +++++++++++++++ #

    self.keep_run   = 0 # used in run for daemon loop, reset by SIGTERM

    self.log          = Log(self)
    self.settings     = Settings(self)
    self.led          = LED(self)
    self.dbhandle     = DBHandle(self)
    self.usb          = UsbManager(self)
    self.rfcomm       = RFCommServer(self)
    self.cmd          = EvalCmd(self)

    self.led.reset_leds()

    # invoke arg parser and parse config or create new config if not found
    self.settings.parse()

    # check if we can load database, create otherwise
    self.dbhandle.dbconnect()

    # load connected usb before bluetooth
    self.usb.check_new_usb()

    # open cmd fifo to read commands
    self.cmd.open_fifo()

    # fire up bluetooth service
    self.rfcomm.start_server()

    # +++++++++++++++ Daemoninze +++++++++++++++ #

    self.check_pidfile()
    self.daemonize()
    self.create_pidfile()

    self.led.show_init_done()

    # +++++++++++++++ Daemon loop +++++++++++++++ #

    self.run()

    # +++++++++++++++ Finalize +++++++++++++++ #

    self.led.cleanup()
    self.delete_pidfile()


  def run(self):
    """
    """

    # expensive operations like new usb drive check should not be run every loop run
    poll_count    = 0

    # -e flag set, run only init and exit directly
    self.keep_run = 0 if self.settings.exitafterinit else 1


    reset_poll_count = self.settings.keep_alive_count * self.settings.usb_count

    # # # # # # DAEMON LOOP ENTRY # # # # # #

    while self.keep_run:

      poll_count += 1

      # check cmd fifo for new commands
      self.cmd.read_fifo()

      # check bluetooth channel for new messages/connections
      self.rfcomm.read_socket()

      time.sleep(self.settings.polltime / 1000.) # 30ms default in config

      # keep alive led
      if poll_count % self.settings.keep_alive_count == 0:
        self.led.set_led_green(1)
      if ( poll_count - self.settings.flash_count ) % self.settings.keep_alive_count == 0:
        self.led.set_led_green(0)

      # check for new USB drives
      if poll_count % self.settings.usb_count == 0:
        # if new usb device found, a new usbdev instance will be created, including dir and mp3 entries
        # if usb device got lost, all coresponding entries will be removed
        self.usb.check_new_usb()

      # multiple of all poll counts --> may reset poll count at reset_poll_count
      if poll_count >= reset_poll_count:
        poll_count = 0

      # end daemon loop

    # # # # # # DAEMON LOOP EXIT # # # # # #

    self.log.write(log.MESSAGE, "---- closed regularly ----")

  # end run() #

  def daemonize(self):
    """
    """

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
    """ Signal handler to stop daemon loop
    """
    self.keep_run = 0


  def check_pidfile(self):
    """Check if daemon already running, throw if pid file found
    """

    if os.path.exists(self.settings.pidfile):
      self.log.write(log.EMERGENCY, "Found pid file for pyblaster, another process running?")
      raise Exception("pid file found")


  def create_pidfile(self):
    """Write getpid() to file after daemonize()
    """

    try:
      fpid = open(self.settings.pidfile, "w")
    except IOError:
      self.log.write(log.EMERGENCY, "failed to create pidfile "+self.settings.pidfile)
      raise

    fpid.write("%s\n" % os.getpid())


  def delete_pidfile(self):
    """Try to remove pid file after daemon should exit
    """
    if os.path.exists(self.settings.pidfile):
      try:
        os.remove(self.settings.pidfile)
      except OSError:
        self.log.write(log.EMERGENCY, "failed to remove pidfile "+self.settings.pidfile)
        raise


  def kill_other_pyblaster(self):
    """Check if pid found in pid file and try to kill this (old) process
    """
    if not os.path.exists(self.settings.pidfile): return

    try:
      f = open(self.settings.pidfile, "r")
    except IOError:
      self.log.write(log.EMERGENCY, "failed to read pidfile "+self.settings.pidfile)
      raise

    pid = int(f.readline().strip())

    print("Trying to kill old process with pid %s..." % pid)

    try:
      os.kill(pid, signal.SIGTERM)
    except OSError:
      self.log.write(log.EMERGENCY, "failed to kill process with pid %s" % pid)
      raise

    exit(0)



if __name__ == '__main__':
  blaster = PyBlaster()
  blaster.run()