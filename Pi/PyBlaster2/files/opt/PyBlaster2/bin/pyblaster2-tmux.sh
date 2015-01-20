#!/bin/sh

# Do not run script if tmux running

[ `ps aux | grep -c " tmux "` -gt 1 ] && exit 0

setterm -blank 0

# new tmux session assuming 256 colors
tmux -2 new-session -d -s pyblaster

# create window
tmux new-window -t pyblaster:1 -n 'PyBlaster'

tmux split-window -h -p 40
tmux select-pane -t 0
tmux send-keys "/opt/PyBlaster2/bin/run-pyblaster2-terminal.sh" C-m
tmux split-window -v -p 20
tmux send-keys "top" C-m

tmux select-pane -R
tmux send-keys "sudo alsamixer" C-m
tmux split-window -v -p 60
tmux send-keys "sudo alsamixer -D equal" C-m
tmux split-window -v -p 33
tmux send-keys "tail -f /var/log/dmesg" C-m

tmux select-pane -t 0
tmux -2 attach-session -t pyblaster
