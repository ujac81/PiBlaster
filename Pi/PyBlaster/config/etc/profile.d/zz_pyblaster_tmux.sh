#!/bin/bash


[ -r /etc/default/pyblaster ] && . /etc/default/pyblaster

if [ "$PYBLASTER_RUN_TMUX" = 1 ]; then
  if [ "x$TERM" = "xlinux" ]; then
    if [ ! -f /tmp/.pyblaster-tmux-launched ]; then
      touch /tmp/.pyblaster-tmux-launched
      /opt/PyBlaster/bin/pyblaster-tmux.sh
    fi
  fi
fi
