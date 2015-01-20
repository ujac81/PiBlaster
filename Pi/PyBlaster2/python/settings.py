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

    def __init__(self, main=None):
        """Parse command line and load config"""

        self.main = main

        # Config defaults, add all values here.
        # Add new key/value pairs to new_config() and read_config().

        self.daemonize = False  # True if should fork
        self.is_daemonized = False  # True if forked
        # Just initialize everything, do not enter daemon loop.
        self.exitafterinit = False
        self.loglevel = -1
        self.pidifile = "/var/run/pyblaster.pid"
        self.configfile = "/etc/pyblaster2/pyblaster.conf"
        self.logfile = "/var/log/pyblaster2.log"
        self.polltime = 30  # daemon poll time in ms
        self.pin1_default = "1234"  # bluetooth connect PIN
        self.pin2_default = "4567"  # Confirm delete/move PIN
        self.puk = "1234567890"  # Required to change PINs or other settings
        self.pin1 = None  # loaded from db
        self.pin2 = None  # loaded from db
        self.dbfile = "/var/lib/pyblaster2/pyblaster.sqlite"
        self.use_lirc = False  # Listen on infrared device (requires lirc)
        self.pidfile = "/var/run/pyblaster2.pid"
        self.rebuilddb = False  # If set to true database will be rebuilt.

    def parse(self):
        """ Parse command line args, set defaults and invoke self.read_config()

            pre:  parent.log is accessible
            post: settings object ready
        """

        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--daemonize", help="run as daemon",
                            action="store_true")
        parser.add_argument("-q", "--quiet", help="no output",
                            action="store_true")
        parser.add_argument("-e", "--exit", help="exit after init",
                            action="store_true")
        parser.add_argument("-k", "--kill",
                            help="try to kill running instance of pyblaster",
                            action="store_true")
        parser.add_argument("-f", "--force",
                            help="force overwrite of pid file",
                            action="store_true")
        parser.add_argument("-v", "--verbosity", type=int,
                            help="set log level 0-7")
        parser.add_argument("-c", "--config", type=str,
                            help="use this pyblaster.conf",
                            default=self.configfile)

        args = parser.parse_args()

        self.daemonize = True if args.daemonize else False
        self.exitafterinit = True if args.exit else False

        if args.verbosity:
            self.loglevel = args.verbosity

        self.configfile = os.path.expanduser(args.config)

        if args.quiet:
            self.loglevel = log.OFF

        self.read_config()

        if args.kill:
            self.main.kill_other_pyblaster()

        if args.force:
            self.main.delete_pidfile()

    def read_config(self):
        """Parse file in --config (defaults to /etc/pyblaster2/pyblaster.conf)
        """

        try:
            f = open(self.configfile, "r")
        except IOError:
            self.main.log.write(log.EMERGENCY,
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

            self.main.log.write(log.DEBUG3,
                                "[CONFIG READ]: key: %s -- value: %s" %
                                (key, val))

            try:
                if key == "loglevel" and self.loglevel == -1:
                    self.loglevel = int(val)
                if key == "logfile":
                    self.logfile = val
                if key == "polltime":
                    self.polltime = int(val)
                if key == "pidfile":
                    self.pidfile = val
                if key == "dbfile":
                    self.dbfile = os.path.expanduser(val)
                if key == "initial_pin1":
                    self.pin1_default = val
                if key == "initial_pin2":
                    self.pin2_default = val
                if key == "puk":
                    self.puk = val
                if key == "use_lirc" and val == "1":
                    self.use_lirc = True

            except ValueError:
                self.main.log.write(log.EMERGENCY, "Failed to convert %s "
                                                    "for key %s in config" %
                                                    (val, key))
                raise

            # for line

        # If log level has not been changed by command line or config, set it.
        if self.loglevel == -1:
            self.loglevel = log.DEBUG3

