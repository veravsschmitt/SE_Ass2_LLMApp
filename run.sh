#!/bin/bash
set -e

# generate and avtivate virtual enviroment
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate

# install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# start app
python app.py
