SESSION_NAME="server"

tmux new-session -d -s $SESSION_NAME

# List of your Python scripts
SCRIPTS=(
    "cd ui && yarn start"
    "cd compute/zeromq && source venv/bin/activate && python proxy.py"
    # TODO navigation, localization scripts
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