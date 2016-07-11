# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import pickle

import numpy as np

from src.model.SolomonProblem import Customer, SolomonProblem
import src.prototype.generalizedCost as g
import src.model.Matrices as mat
import src.model.Route as rt

def H_gamma(cf, delta, startCust, customers, depot):
    #H_gamma is supposed to return a set of routes
    #  - if a customer is infeasible, the cost of starting a new route is used

    #print("Begin H_gamma for {}".format(startCust))
    customers = list(customers)
    route = rt.Route()

    # dangerous - is this start time correct 
    #startCust.serviceTime = startCust.readyTime + startCust.serviceLen
    route.append((0, startCust))

    for i in range(len(customers)):
        #print("Previous: {}".format(route[-1]))
        nextCust = cf.w(delta, route[-1][1], customers, depot, 1)[0]
        customers.remove(nextCust[1])
        #print("Found next best: {}".format(nextCust[1]))

        #print("Next: {} ".format(nextCust))
        #nextCust[1].serviceTime = \
        #    max(route[-1][1].serviceTime + cf.timeMatrix[route[-1][1], nextCust[1]]) 

        route.append(nextCust)

    
    route.append((cf.g(delta, route[-1][1], depot), depot))

    return route

def test_aux(solomonProblem, matrices):
    #run the generalized cost function to the entire customer set
    cf = g.CostFunction(matrices) 
    
    depot = solomonProblem.customers[0]
    cs    = solomonProblem.customers[1:]
    delta = [1]*7
    
    route = H_gamma(cf, delta, depot, cs, depot)    
    
    print(route)


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info('Loading Solomon Problem file {}'.format(input_filepath))

    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)

    logger.info('Generating matrices for problem')
    m = mat.Matrices(sp.customers)
    test_aux(sp, m)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()


