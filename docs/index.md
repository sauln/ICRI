# Welcome to blineVRP 


Prototype for the ICRI algorithm found in 

 > Figliozzi,  M. A.  An  Iterative  Route  Construction  and  Improvement Algorithm for the Vehicle Routing Problem with Soft-Time Windows. Transportation Research Part C, Vol. 18, No. 5, pp. 668–679.

For source code visit [github/ICRI](http://github.com/sauln/ICRI).

This repository will both serve as a

* foundation for future research on stochastic generalizations of the problem and 
* to apply the solutions to real applicatoins, potentially for B-line freight bicycle routing





## TODO
* Quantify robustness of the solution
* Write lots of documentation
* Develop sophisticated methods for modifying hyperparameters (delta)




## Features

Currently implements the algorithm using...


## Installation

`$git clone etc`

`$pip install requirements.txt`




## Commands

* `python run_program.py` - Run current bleeding edge; tests, routing for r101, and visualization

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.



## Project Organization

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A mkdocs documentation 
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        │   └── make_dataset.py
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize.py


This documentation was build with the help of [mkdocs.org](http://mkdocs.org).
