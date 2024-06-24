#!/bin/bash

python3 -m pip install -r requirements.txt --break-system-packages
cd ./src
python3 main.py
