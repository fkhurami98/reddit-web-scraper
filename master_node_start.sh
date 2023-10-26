#!/bin/bash

command -v python3 >/dev/null 2>&1 || { echo >&2 "Python 3 is required but it's not installed.  Aborting."; exit 1; }

python3 distributed_helpers/master_node.py
