#!/bin/bash

# Function to kill process using a specific port
kill_port() {
    # Get the PID of the process using the port
    local pid=$(lsof -ti :$1)

    # If a process is using the port, kill it
    if [ ! -z "$pid" ]; then
        kill -9 $pid
    fi
}

# Navigate to backend
cd ~/dev/stock-app/backend

# Kill any process using port 8000 (or the port your FastAPI app uses)
kill_port 8000

# Start FastAPI
uvicorn main:app --reload &

# Navigate to frontend
cd ~/dev/stock-app/frontend

# Kill any process using port 3000 (or the port your React app uses)
kill_port 3000

# Start React app
npm start
