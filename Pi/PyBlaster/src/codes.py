"""codes.py -- code list for communication to android APP



@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""



PASS_OK         = 1         # correct password sent
PASS_ERROR      = 2         # wrong password


SHOW_DEVICES    = 101       # return on showdevices command
LS_FULL_DIR     = 102       # return on lsfulldir command
LS_DIRS         = 103       # return on lsdirs command
LS_FILES        = 104       # return on lsfiles command

PL_ADD_OK       = 201       # answer on plappendmultiple
PL_SHOW         = 202
