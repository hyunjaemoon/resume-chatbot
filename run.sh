#!/bin/bash

# Get the file path of the current file
root_file_path=$(dirname "$0")

# Virtual environment
python3 -m venv "$root_file_path/.venv"
source "$root_file_path/.venv/bin/activate"

# Install dependencies
pip install -r "$root_file_path/requirements.txt"

# Run the server
mesop main.py --port 8080