"""log.py -- Logging object for PyBlaster

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import datetime

OFF = 0
SHOW = 1
EMERGENCY = 2
ERROR = 3
WARNING = 4
MESSAGE = 5
DEBUG1 = 6
DEBUG2 = 7
DEBUG3 = 8


class Log:
    """Handler to conditionally print/write log messages to stdout/logfile"""

    def __init__(self, main=None):
        """Use init_log() after Settings has been set up"""

        self.main = main
        self.flog = None  # log file handler

    def init_log(self):
        """Create log file using logfile location from settings.

            Invoked via Settings.read_config().

            pre: settings has valid logfile attribute
        """

        try:
            self.flog = open(self.main.settings.logfile, "a")
            self.flog.write("\n")
            self.flog.write("    ===== new pyblaster startup =====    \n")
            self.flog.write("\n")
            self.flog.flush()
        except IOError:
            self.write(EMERGENCY, "Failed to open log file %s" %
                       self.main.settings.logfile)
            raise

    def write(self, level, msg):
        """Write message to stdout/logfile

        Writes, if level is less or equal settings.loglevel.
        Flashes red LED if level is log.EMERGENCY.
        Assuming program will die now.
        """

        if level > self.main.settings.loglevel:
            return

        if not self.main.settings.is_daemonized:
            print(msg)

        if self.flog:
            msg2 = '[' + datetime.datetime.now().strftime('%Y%m%d %H:%M:%S') \
                   + '] ' + msg
            self.flog.write(msg2 + "\n")
            self.flog.flush()

        if level <= EMERGENCY:
            self.main.led.set_led_red()
