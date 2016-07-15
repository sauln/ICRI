# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv

import pickle
import sortedcontainers

#from src.model.CostFunction import CostFunction
from src.visualization.visualize import PlotRoutes 
from src.main.Matrices import Matrices
from src.main.Routes import Routes

def isFeasible(matrix, start, end):
    return start.serviceTime() + matrix.timeMatrix[start.custNo, end.custNo] <= \
           end.dueDate + end.serviceLen

def heuristic(matrix, delta: [float], custStart, custEnd, depot):
    # Infeasible nodes would be filtered before here - 
    start = custStart

    cost = delta[0] * (start.custNo == 0) +\
           delta[1] * matrix.distMatrix[start.custNo, custEnd.custNo] +\
           delta[2] * matrix.timeMatrix[start.custNo, custEnd.custNo]

    return (start, custEnd, cost) 

def getBestNode(matrix, delta, routes, customers, depot):
    cs = sortedcontainers.SortedListWithKey(key=lambda x: x[3])
    # with lots of routes, this could become unreasonable
    # is there any faster way than to look at all of them?
    for r in routes:
        for c in customers:
            res = (r,) + heuristic(matrix, delta, r[-1], c, depot) 
            cs.add(res)

    return cs[0]

def buildRoute(matrix, delta, start, customers, depot):
    routes = Routes(start)

    nextNode = start        
    for i in range(len(customers)):
        route, start, bestNext, cost = \
            getBestNode(matrix, delta, routes.rList, customers, depot)

        if(start.custNo == 0): #the depot
            routes.rList.append([start, bestNext])
        else:
            route.append(bestNext)
        customers.remove(bestNext)
    
    return routes

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info("Begin auxiliary algorithm file")
    logger.info('Loading Solomon Problem file {}'.format(input_filepath))

    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)

    logger.info('Generating matrices for problem')
    
    m = Matrices(sp.customers)
    depot = sp.customers[0]
    cs    = sp.customers[1:]
    delta = [1]*7
   
    routes = buildRoute(m, delta, depot, cs, depot)    
    print(routes)
    PlotRoutes(routes)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

