#!/bin/bash
PYTHONPATH=src/ python -m robomachine.runner --output $1.txt $1.robomachine
pybot $1.txt

