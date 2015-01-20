#!/bin/bash

NAME=pyblaster2
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

DAEMON="$PYBLASTER_PATH/pyblaster2.py"
DAEMON_ARGS="-f -c ${PYBLASTER_CONF}"

echo 1 > /tmp/pyblaster_respawn

do_poweroff=0
setterm -blank 0

(while [ "`cat /tmp/pyblaster_respawn`" = 1 ]; do

  sudo $DAEMON $DAEMON_ARGS || \
  {
    exit_code=$?
    [ $exit_code -eq 10 ] && \
    {
      echo 0 > /tmp/pyblaster_respawn
      do_poweroff=1
      break
    }
    [ "$PYBLASTER_TERMINAL_MODE" = 1 ] && \
    {
      echo
      echo "!!!!! PyBlaster died !!!!!"
      echo "Restarting in 10 secs, do 'service pyblaster stop' to prevent respawn."
    }
    sleep $PYBLASTER_AUTO_RESPAWN_TIMEOUT
  }
  sleep 1
done
rm /tmp/pyblaster_respawn
[ $do_poweroff -eq 1 ] && sudo /sbin/poweroff)&

