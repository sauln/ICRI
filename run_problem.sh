#!/bin/bash

PROBLEM=$1

if [ -z "$1" ] 
    then
    PROBLEM=r101
fi


echo Begin setup for problem $PROBLEM



# Convert the problem to usable format


# Convert the original Solomon Problem dataset into a set saved using our structs.
python3 src/data/make_dataset.py data/raw/$PROBLEM.txt data/interim/$PROBLEM.p


# Run all tests
python3 src/model/TestMatrices.py
python3 src/model/TestSolomonProblem.py

# Plot the dataset with the depot highlighted.
#python3 src/visualization/visualize.py data/interim/$PROBLEM.p

# Generate a route

