#!/bin/sh

# new tmux session assuming 256 colors
tmux -2 new-session -d -s pyblaster

# create window
tmux new-window -t pyblaster:1 -n 'PyBlaster'

tmux split-window -h -p 40
tmux select-pane -t 0
tmux send-keys "tail -f /var/log/pyblaster.log" C-m
tmux split-window -v -p 20
tmux send-keys "top" C-m

tmux select-pane -R
tmux send-keys "alsamixer" C-m
tmux split-window -v -p 60
tmux send-keys "alsamixer -D equal" C-m
tmux split-window -v -p 33
tmux send-keys "tail -f /var/log/dmesg" C-m

tmux select-pane -t 0
tmux -2 attach-session -t pyblaster
