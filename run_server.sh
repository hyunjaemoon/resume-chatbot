#!/bin/bash

# Get the file path of the current file
root_file_path=$(dirname "$0")

# Virtual environment
python3 -m venv "$root_file_path/.venv"
source "$root_file_path/.venv/bin/activate"

# Install dependencies
pip install -r "$root_file_path/requirements.txt"

# Open the browser
open http://localhost:8080

# Run the server
python3 "$root_file_path/server.py"