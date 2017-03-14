#!/usr/bin/env bash
python -m robomachine.runner --tests-max 20 --actions-max 8 --to-state 'Login Page' --output $1.robot --generation-algorithm random  --do-not-execute --generate-graph $1.robomachine
pybot $1.robot