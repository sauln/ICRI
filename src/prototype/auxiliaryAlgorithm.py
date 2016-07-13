# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import pickle

import numpy as np

from src.model.SolomonProblem import Customer, SolomonProblem
import src.model.CostFunction as g
import src.model.Matrices as mat
import src.model.Route as rt


def H_gamma(cf:        g.CostFunction, 
            delta:     [int], 
            startCust: Customer, 
            customers: [Customer], 
            depot:     Customer) -> [rt.Edge]:
    #H_gamma is supposed to return a set of routes
    #  - if a customer is infeasible, the cost of starting a new route is used

    #print("Begin H_gamma for {}".format(startCust))
    customers = list(customers)
    route = rt.Route()

    #start with a stub
    nextEdge = rt.Edge(startCust, startCust, 0) 
    route.append(nextEdge)

    for i in range(len(customers)):
        nextEdge = cf.w(delta, nextEdge.end, customers, depot, 1)[0]
        
        route.append(nextEdge)
        customers.remove(nextEdge.end)
   

    # Add the final trip back to the depot.
    lastCost = cf.g(delta, nextEdge.end, depot)
    route.append(rt.Edge(nextEdge.end, depot, lastCost))
    #route.route.insert(0, rt.Edge(startCust, route[0].start, \
    #    cf.g(delta, startCust, route[0].start)))

    print("New first 3 of route: {} => {} => {}".format(route[0], route[1], route[2]))

    return route


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info("Begin auxiliary algorithm file")
    logger.info('Loading Solomon Problem file {}'.format(input_filepath))

    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)

    logger.info('Generating matrices for problem')
    cf = g.CostFunction(sp.customers) 
    
    depot = sp.customers[0]
    cs    = sp.customers[1:]
    delta = [1]*7
    
    route = H_gamma(cf, delta, depot, cs, depot)    
    print(route)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

