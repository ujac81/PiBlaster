"""codes.py -- code list for communication to android APP



@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

PASS_OK = 1         # correct password sent
PASS_ERROR = 2      # wrong password

SHOW_DEVICES = 101  # return on showdevices command
LS_FULL_DIR = 102   # return on lsfulldir command
LS_DIRS = 103       # return on lsdirs command
LS_FILES = 104      # return on lsfiles command

PL_ADD_OK = 201     # answer on plappendmultiple
PL_SHOW = 202
PL_JUMP_OK = 203    # jumped to double-tapped item
PL_MODIFIED = 204   # if PL changed -- reload PL

SEARCH_RES = 220    # show search result list

PLAY_PAUSE = 301    # answer on playpause
PLAY_PREV = 302     # answer on playprev
PLAY_NEXT = 303     # answer on playnext
PLAY_INFO = 304     # answer on playstatus

KEEP_ALIVE = 1000   # answer on keepalive

