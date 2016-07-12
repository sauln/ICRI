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
from src.model.Route import Route, Node





def naiveRoute(solomonProblem, matrices):
    cf = g.CostFunction(matrices) 
    depot = solomonProblem.customers[0]
    delta = [1]*7
    naive = aux.H_gamma(cf, delta, depot, solomonProblem.customers[1:], depot)
    return naive

def H_c(H_gamma, w, c, C, LLimit, W, delta):
    pass

def findRoutes(cf, delta, start, customers, depot):
    tmpCS = list(customers)
    tmpCS.remove(start)
    croute = aux.H_gamma(cf, delta, start, tmpCS, depot)
    return croute

def routeConstruction(solomonProblem, costFunction):
    #start from depot
    # find the best 10 next notes
    # run the auxalgorithm on these 10 and choose the best of them

    print("Begin route construction")
    w = 10

    cf = costFunction
       
    depot = solomonProblem.customers[0]
    cs    = list(solomonProblem.customers[1:])
    delta = [1]*7

    # should the route get the matrices?
    route = Route()
    route.append(Node(depot, depot,0))
   
    # does not account for the depot node in the route construction cost!
    for i in range(len(cs)):
        bestCs = cf.w(delta, route[-1].end, cs, depot, w)
         
        potentialRoutes = [(c.end, findRoutes(cf, delta, c.end, cs, depot)) for c in bestCs]
        best = min(potentialRoutes, key = lambda r: r[1].cost())
        print("Best: {}".format(best))
        print(type(best[0]))
        route.append(Node(route[-1].end, best[0], 0))
        cs.remove(best[0])

    route.append(Node(route[-1].end, depot, cf.g(delta, route[-1].end, depot)))

    naive = aux.H_gamma(cf, delta, depot, solomonProblem.customers[1:], depot)
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

