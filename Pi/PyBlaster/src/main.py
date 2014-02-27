#!/usr/bin/env python
"""main.py -- will be removed.

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

from pyblaster import PyBlaster
import sys


def main():
    """Init PyBlaster daemon
    """

    #try:
    blaster = PyBlaster()
    #except:
        #blaster.led.set_led_red(1)
        #e = sys.exc_info()[0]
        #print("ERROR [GOT EXCEPTION] %s" % e)



if __name__ == '__main__':
    main()
