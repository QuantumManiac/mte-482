SESSION_NAME="client"

tmux new-session -d -s $SESSION_NAME

tmux send-keys -t $SESSION_NAME "cd power/power_management && sudo -s && . venv/bin/activate && python power_management.py" C-m

tmux split-window -v
tmux select-pane -t 1
tmux send-keys -t $SESSION_NAME "cd compute/io && sudo -s && . venv/bin/activate && python sensors.py" C-m


tmux split-window -v
tmux select-pane -t 2
tmux send-keys -t $SESSION_NAME "cd compute/io && . venv/bin/activate && python serial_to_arduino.py" C-m


tmux split-window -v
tmux select-pane -t 3
tmux send-keys -t $SESSION_NAME "cd localization/qr && . venv/bin/activate && python camera.py" C-m

# Finally, attach to the tmux session
tmux attach-session -t $SESSION_NAME