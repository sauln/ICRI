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
python3 src/model/TestCostFunction.py
#python3 src/prototype/TestRouteConstructionAlgorithm.py
#python3 src/prototype/TestAuxiliaryAlgorithm.py


python3 src/prototype/basicOps.py data/interim/$PROBLEM.p


#python3 src/prototype/routeConstructionAlgorithm.py data/interim/$PROBLEM.p
#python3 src/prototype/auxiliaryAlgorithm.py data/interim/$PROBLEM.p
#mypy src/prototype/routeConstructionAlgorithm.py data/interim/$PROBLEM.p



# Plot the dataset with the depot highlighted.
#python3 src/visualization/visualize.py data/interim/$PROBLEM.p

# Generate a route

