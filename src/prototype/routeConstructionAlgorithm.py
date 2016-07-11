# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import pickle

import numpy as np

from src.model.SolomonProblem import Customer, SolomonProblem
import src.prototype.auxiliaryAlgorithm as aux
import src.prototype.generalizedCost as g
import src.model.Matrices as mat
from src.model.Route import Route


def naiveRoute(solomonProblem, matrices):
    cf = g.CostFunction(matrices) 
    depot = solomonProblem.customers[0]
    delta = [1]*7
    naive = aux.H_gamma(cf, delta, depot, solomonProblem.customers[1:], depot)
    return naive


def partitionFeasible(timeMatrix, start, customers):
    # a feasible customer is one whose last time is greater than start.time + travel_time
    
    #def feasible(timeMatrix, start, end):
    #    return end.dueDate - end.serviceLen >= \
    #        start._serviceTime + timeMatrix[start.custNo, end.custNo]

    feasible = filter(lambda c: \
        start.serviceTime + timeMatrix[start.custNo,c.custNo] <= \
        c.dueDate + c.serviceLen, customers)

    infeasible = [c for c in customers if c not in feasible]
    return (feasible, infeasible)



def routeConstruction(solomonProblem, matrices):
    #start from depot
    # find the best 10 next notes
    # run the auxalgorithm on these 10 and choose the best of them

    print("Begin route construction")
    w = 10

    cf = g.CostFunction(matrices) 
       
    depot = solomonProblem.customers[0]
    cs    = list(solomonProblem.customers[1:])
    delta = [1]*7
    
    route = Route()
    route.append((0,depot))
   
    # does not account for the depot node in the route construction cost!
    for i in range(len(cs)):
        #print("Loop section {}".format(i)) 
        infeasible, feasible = partitionFeasible(matrices.timeMatrix, route[-1][1], cs)
        bestCs = cf.w(delta, route[-1][1], cs, depot, w)
         
        potentialRoutes = []
        for c in bestCs:
            tmpCS = list(cs)
            tmpCS.remove(c[1])
            croute = aux.H_gamma(cf, delta, c[1], tmpCS,  depot)
            potentialRoutes.append((c, croute))
    


        best = min(potentialRoutes, key = lambda r: r[1].cost())
           
        route.append(best[0])
        cs.remove(best[0][1])

    route.append((cf.g(delta, route[-1][1], depot), depot))

    naive = aux.H_gamma(cf, delta, depot, solomonProblem.customers[1:], depot)
    return route


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info('Loading Solomon Problem file {}'.format(input_filepath))

    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)

    logger.info('Generating matrices for problem')
    m = mat.Matrices(sp.customers)

    logger.info('Constructing routes!')
    routeConstruction(sp, m)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

