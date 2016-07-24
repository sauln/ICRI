# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import pickle

from src.main.SolomonProblem import SolomonProblem
from src.main.Customer import Customer
import src.visualization.visualize as viz

@click.command()
@click.argument('output_filepath', type=click.Path())
def main(output_filepath):
    logger = logging.getLogger(__name__)
    logger.info('Creating simple SP {}'.format(output_filepath))

    num_vehicles = 10
    capacity = 10
    problem_name = "Simple test problem"

    customers = []

    customerData = [ [0,  0,  0,  0,  0,  20, 0],
                     [1,  1,  1,  1,  1,   5, 1],
                     [2,  1,  0,  3,  5,   8, 2],
                     [3,  2,  2,  1,  4,  10, 3],
                     [4,  5,  5,  3,  3,  10, 3],
                     [5,  3,  2,  3, 15,  19, 3],
                     [6,  1,  2,  1,  0,   1, 2] ]
    


    for c in customerData:
        customers.append(Customer(*c))

    problem = SolomonProblem(problem_name, num_vehicles, capacity, customers) 
    with open(output_filepath, "wb") as f:
        pickle.dump(problem, f)

    logger.info("problem: %s", problem)

    viz.visualizeRoute(problem)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

