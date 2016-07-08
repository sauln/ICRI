#!/bin/bash

PROBLEM=$1
echo Begin setup for problem $PROBLEM

python3 src/data/make_dataset.py data/raw/$PROBLEM.txt data/interim/$PROBLEM.p
python3 src/visualization/visualize.py data/interim/$PROBLEM.p

