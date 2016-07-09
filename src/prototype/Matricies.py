# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import pickle
import numpy as np


from src.model.SolomonProblem import Customer, SolomonProblem



def distEuclid(x,y):
    return np.sqrt((x.xcoord - y.xcoord)**2 + (x.ycoord - y.ycoord)**2)


def distanceMatrix(customers):

    distance_matrix = np.empty([len(customers), len(customers)])


    # there were some basic matrix multiplications that did this, werent' there?
    for i in range(len(customers)):
        for j in range(len(customers)):
            distance_matrix[i,j] = distEuclid(customers[i], customers[j])



    return distance_matrix








class stub():
    def __init__(self, x, y):
        self.xcoord = x
        self.ycoord = y








@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info("Write unite tests")
    logger.info("Loan the customers")
    logger.info("Generate distance matrices")
    logger.info('Loading problem file {}'.format(input_filepath))

    with open(input_filepath, "rb") as f:
        problem = pickle.load(f)
        customers = problem.customers

    #logger.info("\n".join(c.__str__() for c in customers))
    logger.info(distance(stub(0,1), stub(1,1)))


    





if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

