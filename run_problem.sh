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
python3 src/test/TestMatrices.py
python3 src/test/TestSolomonProblem.py
python3 src/test/TestCostFunction.py

python3 src/main/basicOps.py data/interim/$PROBLEM.p

