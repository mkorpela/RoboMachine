#!/bin/bash
PYTHONPATH=src/ python -m robomachine.runner $1.robomachine $1.txt
pybot $1.txt

