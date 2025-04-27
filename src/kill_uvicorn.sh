#!/bin/bash
# kill_uvicorn.sh (final, professional version)

PORT=8000
echo "Searching for processes on port $PORT..."
PIDS=$(lsof -t -i:$PORT)

if [ -z "$PIDS" ]; then
  echo "No process found on port $PORT."
else
  echo "Killing processes with PIDs: $PIDS"
  kill -9 $PIDS
  echo "Processes killed."
fi
