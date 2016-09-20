# -*- coding: utf-8 -*-
import os
import time
import logging
from dotenv import find_dotenv, load_dotenv

import pickle
import sortedcontainers
import numpy as np

import src

logger = logging.getLogger(__name__)




def main():
    problem_number = "r101"
    input_filepath = "data/raw/{}.txt".format(problem_number)
    output_filepath = "data/interim/{}.p".format(problem_number)
    intermediate_filepath = "data/interim/solution_{}.p".format(problem_number)
    
    
    logger.info('Setup Parameters and Dispatch')
    sp = src.DataBuilder(input_filepath, output_filepath).problem
    src.Parameters().build(sp, 10, 10)
    dispatch = src.Dispatch(sp.customers)
    

    logger.info('Construct routes')
    solution = src.RollOut().run(dispatch)
    
    logger.info("Save intermediate solution.")
    with open(intermediate_filepath, "wb") as f:
        pickle.dump(solution, f)

    logger.info("Inition solution - there are {} vehicles with {} allowed"\
        .format(len(solution.vehicles), sp.numVehicles)) 
    #Plotter().plotDispatch(solution).show()

    logger.info("Running improvement algorithm on solution")
    newSolution = src.Improvement().run(solution)
    Plotter().beforeAndAfter(solution, newSolution).show()

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()

