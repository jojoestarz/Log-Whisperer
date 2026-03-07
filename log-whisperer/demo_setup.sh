#!/bin/bash
# Tmux automation script for Log Whisperer demo
# Creates a 3-pane layout: API server, Rerun viewer, CLI trigger

SESSION="log-whisperer"

# Check if session exists
tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
    # Create new session
    tmux new-session -d -s $SESSION -n "demo"
    
    # Split into 3 panes
    tmux split-window -h -t $SESSION:0
    tmux split-window -v -t $SESSION:0.1
    
    # Pane 0: API server
    tmux send-keys -t $SESSION:0.0 "cd log-whisperer && source venv/bin/activate" C-m
    tmux send-keys -t $SESSION:0.0 "python api/main.py" C-m
    
    # Pane 1: Rerun viewer
    tmux send-keys -t $SESSION:0.1 "cd log-whisperer && source venv/bin/activate" C-m
    tmux send-keys -t $SESSION:0.1 "python viz/timeline.py" C-m
    
    # Pane 2: CLI (ready for commands)
    tmux send-keys -t $SESSION:0.2 "cd log-whisperer && source venv/bin/activate" C-m
    tmux send-keys -t $SESSION:0.2 "echo 'Ready! Run: python cli/main.py trigger'" C-m
    
    # Select pane 2 (CLI)
    tmux select-pane -t $SESSION:0.2
fi

# Attach to session
tmux attach-session -t $SESSION
