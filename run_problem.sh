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
echo TestMatrices.py
python3 src/test/TestMatrices.py

echo TestSolomonProblem.py
python3 src/test/TestSolomonProblem.py

#echo TestBasicOps.py
#python3 src/test/TestBasicOps.py

echo TestRoutes.py
python3 src/test/TestRoutes.py

echo TestVehicle.py
python3 src/test/TestVehicle.py

echo TestHeuristic.py
python3 src/test/TestHeuristic.py

#python3 src/main/basicOps.py data/interim/$PROBLEM.p
