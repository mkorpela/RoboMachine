#!/usr/bin/env bash
BASENAME=model

export PYTHONPATH=../..
INFILE=$BASENAME.robomachine
OUTFILE=$BASENAME.robot

python -m robomachine.runner --tests-max 20 --actions-max 8 \
          --to-state 'Login Page' \
          --output $OUTFILE --generate-dot-graph svg \
          --generation-algorithm allpairs-random \
          $INFILE