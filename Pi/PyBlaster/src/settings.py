"""settings.py -- All settings for PyBlaster project

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import argparse
import os.path

import log


class Settings:
    """Command and config file parser

    Holds all settings variables for whole project
    """

    def __init__(self, parent=None):
        """Parse command line and load config"""

        self.parent = parent

        # Config defaults, add all values here.
        # Add new key/value pairs to new_config() and read_config().

        self.daemonize = False
        self.is_daemonized = False
        self.exitafterinit = False
        self.rebuilddb = False
        self.loglevel = log.DEBUG3
        self.pidifile = "/var/run/pyblaster.pid"
        self.fifoin = None
        self.cmdout = None
        self.configfile = "/etc/pyblaster.conf"
        self.logfile = "/var/log/pyblaster.log"
        self.polltime = 30          # daemon poll time in ms
        self.flash_count = 2        # flash activity LED n poll
        self.keep_alive_count = 20  # let activity LED flash every n polls
        self.pin1_default = "1234"
        self.pin2_default = "4567"
        self.puk = "1234567890"
        self.pin1 = None  # loaded from db
        self.pin2 = None  # loaded from db
        self.dbfile = "/var/lib/pyblaster/pyblaster.sqlite"
        self.use_lirc = False
        self.loglevel_from_cmd = False
        self.pidfile = "/var/run/pyblaster.pid"
        self.default_vol_change = 4
        self.localdirs = []

        # end __init__() #

    def parse(self):
        """ Parse command line args, set defaults and invoke self.read_config()

            pre:    parent.log is accessible
            post: settings object ready
        """

        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--daemonize",
                            help="run as daemon",
                            action="store_true")
        parser.add_argument("-n", "--newconfig",
                            help="write new pyblaster.conf",
                            action="store_true")
        parser.add_argument("-q", "--quiet",
                            help="no output",
                            action="store_true")
        parser.add_argument("-e", "--exit",
                            help="exit after init",
                            action="store_true")
        parser.add_argument("-r", "--rebuilddb",
                            help="force recreation of database",
                            action="store_true")
        parser.add_argument("-k", "--kill",
                            help="try to kill running instance of pyblaster",
                            action="store_true")
        parser.add_argument("-f", "--force",
                            help="force overwrite of pid file",
                            action="store_true")
        parser.add_argument("-v", "--verbosity",
                            type=int,
                            help="set log level 0-7")
        parser.add_argument("-c", "--config",
                            type=str,
                            help="use this pyblaster.conf",
                            default=self.configfile)

        args = parser.parse_args()

        # If False, may overwrite loglevel in read_config().
        self.loglevel_from_cmd = False
        # Changed to true by PyBlaster.daemonize() if daemonized.
        self.is_daemonized = False

        self.daemonize = True if args.daemonize else False
        self.exitafterinit = True if args.exit else False
        self.rebuilddb = True if args.rebuilddb else False

        if args.verbosity:
            self.loglevel = args.verbosity
            self.loglevel_from_cmd = True

        self.configfile = os.path.expanduser(args.config)

        if args.newconfig:
            self.new_config()
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
        """Create new config file at --config location

        Defaults to ~/.pyblaster.conf.
        """

        self.parent.log.write(log.SHOW,
                              "Creating new config file %s" % self.configfile)

        msg = """# Default config file for PyBlaster -- created by -n switch

####################################
# debug
####################################

loglevel 8

logfile /var/log/pyblaster.log

pidfile /var/run/pyblaster.pid


####################################
# command
####################################

# input fifo -- comment out to disable
fifoin    /var/lib/pyblaster/pyblaster.cmd


# cmd output stream as simple file, no pipe or other stuff,
# overwritten on start
cmdout    /var/lib/pyblaster/pyblastercmd.log


####################################
# Database
####################################

dbfile /var/lib/pyblaster/pyblaster.sqlite

####################################
# Control
####################################

use_lirc 1


####################################
# Passwords
####################################

# Initial connection password.
# Will be transfered to database if not inside.
# May be changed in database via command interface
# using puk.
# If database is rebuilt for some reason (broken, format changes, ...)
# pin will be reset to this value.
initial_pin 1234

# Same behaviour as above.
# This key is not required for connection, but for deleting files
# or reseting database or other invasive actions.
initial_pin2 4567

# Required for password changes.
# Passwords will be changed in database, values above are only defaults.
puk 1234567890


####################################
# extra dirs
####################################

local_dirs /local


"""

        try:
            f = open(self.configfile, "w")
        except IOError:
            self.parent.log.write(log.EMERGENCY,
                                  "Settings.new_config(): Failed to write "
                                  "config file %s" % self.configfile)
            raise
        f.write(msg)

        # end new_config() #

    def read_config(self):
        """Parse file in --config (defaults to ~/.pyblaster.conf)

        If not found, new_config() will be invoked.
        """

        if not os.path.exists(self.configfile):
            self.new_config()

        try:
            f = open(self.configfile, "r")
        except IOError:
            self.parent.log.write(log.EMERGENCY,
                                  "Failed to open config file %s" %
                                  self.configfile)
            raise

        for line in f:
            if line.startswith('#') \
                    or len(line) < 3 \
                    or line.count(' ', 0, len(line)-2) < 1:
                continue

            key = line.split(None, 1)[0].strip()
            val = line.split(None, 1)[1].strip()

            self.parent.log.write(log.DEBUG3,
                                  "[CONFIG READ]: key: %s -- value: %s" %
                                  (key, val))

            try:
                if key == "loglevel" and not self.loglevel_from_cmd:
                    self.loglevel = int(val)
                if key == "logfile":
                    self.logfile = val
                if key == "polltime":
                    self.polltime = int(val)
                if key == "pidfile":
                    self.pidfile = val
                if key == "flash_count":
                    self.flash_count = int(val)
                if key == "keep_alive_count":
                    self.keep_alive_count = int(val)
                if key == "dbfile":
                    self.dbfile = os.path.expanduser(val)
                if key == "fifoin":
                    self.fifoin = os.path.expanduser(val)
                if key == "cmdout":
                    self.cmdout = os.path.expanduser(val)
                if key == "intial_pin1":
                    self.pin1_default = val
                if key == "intial_pin2":
                    self.pin2_default = val
                if key == "puk":
                    self.puk = val
                if key == "use_lirc":
                    if val == "1":
                        self.use_lirc = True
                if key == "local_dirs":
                    self.localdirs = val.split()

            except ValueError:
                self.parent.log.write(log.EMERGENCY, "Failed to convert %s "
                                                     "for key %s in config" %
                                                     (val, key))
                raise

            # for line

        # end read_config() #
