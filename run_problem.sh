#!/bin/bash

PROBLEM=$1

if [ -z "$1" ] 
    then
    PROBLEM=r101
fi

echo Begin setup for problem $PROBLEM

# Convert the original Solomon Problem dataset into a set saved using our structs.
python3 src/data/make_dataset.py data/raw/$PROBLEM.txt data/interim/$PROBLEM.p

# Run all tests
python3 -m unittest -v src.test.BaseObjects
python3 -m unittest -v src.test.Algorithms

python3 src/main/run.py data/interim/$PROBLEM.p

