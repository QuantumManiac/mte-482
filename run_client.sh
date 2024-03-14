#!/usr/bin/zsh
SESSION_NAME="client"

tmux new-session -d -s $SESSION_NAME

# List of your Python scripts
SCRIPTS=(
    "cd power/power_management && . venv/bin/activate && sudo python power_management.py"
    "cd compute/io && . venv/bin/activate && sudo python sensors.py"
    "cd compute/io && . venv/bin/activate && python serial_to_arduino.py"
    "cd localization/qr && . venv/bin/activate && python camera.py"
)

# First script execution - need to handle the first pane differently
tmux send-keys -t $SESSION_NAME "${SCRIPTS[0]}" C-m

# Execute the rest of the scripts in new panes
for (( i=1; i<${#SCRIPTS[@]}; i++ ))
do
    # Split the window vertically
    tmux split-window -v
    # Select the newly created pane
    tmux select-pane -t $i
    # Execute the script
    tmux send-keys -t $SESSION_NAME "${SCRIPTS[$i]}" C-m
done

# Finally, attach to the tmux session
tmux attach-session -t $SESSION_NAME