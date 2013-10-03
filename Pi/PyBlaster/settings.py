"""settings.py


@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import log
from log import Log

import argparse
import os.path

class Settings:
  """Command and config file parser -- holds all settings variables for whole project
  """

  def __init__(self, parent=None):
    """initialize settings -- parse command line and load config
    """
    self.parent = parent

    # config defaults, add all values here #
    # add new key/value pairs to new_config() and read_config()

    self.daemonize        = False
    self.exitafterinit    = False
    self.rebuilddb        = False
    self.loglevel         = log.DEBUG3
    self.pidifile         = "/tmp/pyblaster.pid"
    self.configfile       = "~/.pyblaster.conf"
    self.logfile          = "/tmp/pyblaster.log"
    self.polltime         = 30                    # daemon poll time in ms
    self.flash_count      = 2                     # flash activity LED n poll
    self.keep_alive_count = 20                    # let activity LED flash every n polls
    self.usb_count        = 30                    # check usb drives every n polls
    self.dbfile           = "~/.pyblaster.sqlite" # database file for device and playlist storage


  def parse(self):
    """ Parse command line args, set defaults and invoke self.read_config()

      pre:  parent.log is accessible
      post: settings object ready
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--daemonize",            help="run as daemon",               action="store_true")
    parser.add_argument("-n", "--newconfig",            help="write new pyblaster.conf",    action="store_true")
    parser.add_argument("-q", "--quiet",                help="no output",                   action="store_true")
    parser.add_argument("-e", "--exit",                 help="exit after init",             action="store_true")
    parser.add_argument("-r", "--rebuilddb",            help="force recreation of database",action="store_true")
    parser.add_argument("-k", "--kill",                 help="try to kill running instance of pyblaster", action="store_true")
    parser.add_argument("-f", "--force",                help="force overwrite of pid file", action="store_true")
    parser.add_argument("-v", "--verbosity",  type=int, help="set log level 0-7")
    parser.add_argument("-c", "--config",     type=str, help="use this pyblaster.conf",     default=self.configfile)

    args = parser.parse_args()

    self.loglevel_from_cmd  = False   # if False, may overwrite loglevel in read_config()
    self.is_daemonized      = False   # changed to true by PyBlaster.daemonize() if daemonized

    self.daemonize      = True if args.daemonize  else False
    self.exitafterinit  = True if args.exit       else False
    self.rebuilddb      = True if args.rebuilddb  else False

    if args.verbosity:
      self.loglevel           = args.verbosity
      self.loglevel_from_cmd  = True

    self.configfile = os.path.expanduser(args.config)

    if args.newconfig: self.new_config()
    if args.quiet:
      self.loglevel = log.OFF
      self.loglevel_from_cmd = True

    self.read_config()

    if args.kill:
      self.parent.kill_other_pyblaster()

    if args.force:
      self.parent.delete_pidfile()

    # end parse() #

  def new_config(self):
    """create new config file at --config location (defaults to ~/.pyblaster.conf)
    """

    self.parent.log.write(log.SHOW, "Creating new config file "+self.configfile)

    msg = """# Default config file for PyBlaster -- created by -n switch

####################################
# debug
####################################

loglevel 8

logfile /tmp/pyblaster.log

pidfile /tmp/pyblaster.pid


####################################
# timings
####################################

# sleep N ms in each loop
polltime 30

# number of poll cycles for LED flash
flash_count 2

# flash green keep alive every N polls
keep_alive_count 20


####################################
# Database
####################################

dbfile /root/.pyblaster.sqlite


"""

    try:
      f = open(self.configfile, "w")
    except IOError:
      self.parent.log.write(log.EMERGENCY, "Settings.new_config(): Failed to write config file "+self.configfile)
      raise
    f.write(msg)

    # end new_config() #


  def read_config(self):
    """Parse file in --config (defaults to ~/.pyblaster.conf) -- if not found, new_config() will be invoked
    """

    if not os.path.exists(self.configfile): self.new_config()

    try:
      f = open(self.configfile, "r")
    except IOError:
      self.parent.log.write(log.EMERGENCY, "Failed to open config file "+self.configfile)
      raise

    for line in f:
      if line.startswith('#') or len(line) < 3 or line.count(' ', 0, len(line)-2) < 1: continue

      key = line.split(None, 1)[0].strip()
      val = line.split(None, 1)[1].strip()

      self.parent.log.write(log.DEBUG3, "[CONFIG READ]: key: %s -- value: %s" % ( key, val ))

      try:
        if key == "loglevel" and not self.loglevel_from_cmd:
          self.loglevel = int(val)

        if key == "logfile":
          self.logfile = val
          #self.parent.log.init_log()

        if key == "polltime":         self.polltime         = int(val)
        if key == "pidfile":          self.pidfile          = val
        if key == "flash_count":      self.flash_count      = int(val)
        if key == "keep_alive_count": self.keep_alive_count = int(val)
        if key == "dbfile":           self.dbfile           = os.path.expanduser(val)

      except ValueError:
        self.parent.log.write(log.EMERGENCY, "Failed to convert %s for key %s in config" % ( val, key ) )
        raise

    # for line







  # end read_config() #







