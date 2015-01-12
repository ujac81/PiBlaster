#!/bin/bash


[ -r /etc/default/pyblaster ] && . /etc/default/pyblaster

[ "$PYBLASTER_RUN_TMUX" = 1 ] || exit 0

[ "x$L1" = "xtty1" ] && /opt/PyBlaster/bin/pyblaster-tmux.sh



