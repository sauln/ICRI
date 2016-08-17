# Welcome to blineVRP 

Prototype for the ICRI algorithm found in 

 > Figliozzi,  M. A.  An  Iterative  Route  Construction  and  Improvement Algorithm for the Vehicle Routing Problem with Soft-Time Windows. Transportation Research Part C, Vol. 18, No. 5, pp. 668–679.

For source code visit [github/ICRI](http://github.com/sauln/ICRI).

This repository will both serve as a

* foundation for future research on stochastic generalizations of the problem and 
* to apply the solutions to real applicatoins, potentially for freight bicycle routing

## Features

Currently implements the rollout with a design that was considerate of future attempts for parallelization.  



## Requirements
* Python3 - 
* Numpy   - some numerical optimizations
* Click   - mostly deprecated
* mkdocs  - to build the documentation

## Installation

`git clone http://github.com/sauln/ICRI.git`

`pip install requirements.txt`

## Commands

* `./run_program.sh` - Run current bleeding edge; tests, routing for r101, and visualization

## Project Organization

    ├── LICENSE
    ├── Makefile             <- Makefile with commands like `make data` or `make train`
    ├── README.md            <- The top-level README for developers using this project.
    ├── data
    │   ├── interim          <- Intermediate data that has been transformed.
    │   └── raw              <- The original, immutable data dump.
    │
    ├── docs                 <- A mkdocs documentation project 
    │
    ├── reports              <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures          <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt     <- The requirements file for reproducing the analysis environment, e.g.
    │                           generated with `pip freeze > requirements.txt`
    │
    └── src                  <- Source code for use in this project.
        ├── __init__.py      <- Makes src a Python module
        │
        ├── main             <- Source code
        │   ├── BaseObjects  <- Objects. Vehicles, Routes, Customers, etc
        │   └── Algorithms   <- Algorithms and functions. Cost, RollOut, GNNH, etc
        │
        ├── test             <- Tests for source code - should have one-to-one files with source code
        │   ├── BaseObjects  <- 
        │   └── Algorithms   
        │
        ├── data             <- Scripts to download or generate data
        │
        └── visualization    <- Scripts to create exploratory and results oriented visualizations


This documentation was build with the help of [mkdocs.org](http://mkdocs.org).
