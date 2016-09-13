# About
This software suite implements a basic roll out approach for the Solomon set of vehicle
routing problems.  It uses as it's base heuristic the generalized nearest neighbors
algorithm. 

There are a set of base objects that are very obviously objects and a set of algorithms
and grouped functions.

I have tried to isolate all of the points of interest into just a few places.


## How to

### Data
Original problem sets defined by Solomon are found in `data/raw`

Solutions of the rollout and objects from various stages of the process are found in `data/interim`

Results for the hyperparameter optimization and other experiments, such as profiling and time tests are found in `data/processed`

### Code outline

`src/data/make_dataset.py` is the main file for converting the raw Solomon problems into our basic Python Solomon Problem object.

`src/demo` contains two files for completing time trials of the code.  The `Problem_builder.py` will create new partially randomized customer sets from existing customer sets and `time_trial.py` will run a lengthy time trial experiment and generate plots and tables.

`src/main/Algorithms/GridSearch.py` supplies a number of different hyper-parameter optimizations.

There is a very basic grid search using a Latin Hypercube, a random search (need bibliography page), and a shadow cost search.  ( there's gotta be a better name than shadow cost search)




