# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import pickle

import numpy as np

from src.model.SolomonProblem import Customer, SolomonProblem
import src.prototype.auxiliaryAlgorithm as aux
import src.model.CostFunction as g
import src.model.Matrices as mat
from src.model.Route import Route, Edge


     

 
def greedyRoute(cf:        g.CostFunction, 
                delta:     [int], 
                start:     Customer, 
                customers: [Customer], 
                depot:     Customer) -> Route:
    tmpCS = list(customers)
    tmpCS.remove(start)
    croute = aux.H_gamma(cf, delta, start, tmpCS, depot)
    return croute



def H_c(costFunction, depot, customers, width: int, Delta: [[float]]):
    cs = list(customers)
    
    delta = Delta[0]

    #setup first node in chain so the loop can continue easily 
    lastEdge = Edge(depot, depot, 0)
    
    route = Route()
    for i in range(len(cs)):
    
        # find top best next routes - returns a set of edges
        bestCs = costFunction.w(delta, lastEdge.end, cs, depot, width)
       
        #
        potentialRoutes = [(c.end, greedyRoute(costFunction, delta, c.end, cs, depot)) \
                                for c in bestCs]
        lastCust = min(potentialRoutes, key = lambda r: r[1].cost())[0]
        lastEdge = Edge(lastEdge.end, lastCust, 0)
        route.append(lastEdge)
        cs.remove(lastCust)

    route.append(Edge(route[-1].end, depot, costFunction.g(delta, route[-1].end, depot)))

    return route
        
def routeConstruction(solomonProblem: SolomonProblem, 
                      costFunction: g.CostFunction) -> Route:
    print("Begin route construction")
    w = 10

    depot = solomonProblem.customers[0]
    cs    = list(solomonProblem.customers[1:])
    delta = [1]*7

    route = H_c(costFunction, depot, cs, w, [delta]) 
    #naive = aux.H_gamma(costFunction, delta, depot, solomonProblem.customers[1:], depot)
    return route


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info("Begin route construction algorithm file")
    logger.info('Loading Solomon Problem file {}'.format(input_filepath))

    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)

    logger.info('Generating matrices for problem')
    logger.info('Constructing routes!')
    
    cf = g.CostFunction(sp.customers) 
    r = routeConstruction(sp, cf)
    print(r)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()


