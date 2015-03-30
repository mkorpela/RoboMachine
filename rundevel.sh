#!/usr/bin/env bash
PYTHONPATH=src/ python -m robomachine.runner --output $1.txt --generation-algorithm random $1.robomachine
pybot $1.txt

