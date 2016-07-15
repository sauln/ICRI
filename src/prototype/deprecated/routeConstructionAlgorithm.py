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
from src.model.Route import Route, Routes

#Edge


    

'''

I'm starting to think of a complete refactor.

putting emphasis on the route object

how can we model it more like a graph, rather than a set of edges.

i want static type checking at compile time - everything would be so much easier...


objects:
Routes - an object of routes
 - this will keep our stack of routes
 - it will return a set of potentially free nodes
 - assume that when the next best addition is to not continue, we will
   attempt to continue on with this path in the future.

Routes::freeNodes() -> [Customers] 
    - all 

operations: 
buildGreedyRoute(start, customers, end) -> route
'''






 
def greedyRoute(cf:        g.CostFunction, 
                delta:     [int], 
                start:     Customer, 
                customers: [Customer], 
                depot:     Customer) -> Route:
    tmpCS = list(customers)
    tmpCS.remove(start) # this is O(n) and shouldn't be
    croute = aux.H_gamma(cf, delta, start, tmpCS, depot)
    return croute



def H_c(costFunction, depot, customers, width: int, Delta: [[float]]):
    cs = list(customers)
    
    delta = Delta[0]

    #setup first node in chain so the loop can continue easily 
    #nextEdge = Edge(depot, depot, 0)
    
    nextNode = depot

    routes = Routes()
    route = Route()

    #route.append(nextEdge)
    route.append(nextNode, 0)
    routes.rlist.append(route)

    iters = len(cs)
    iters = 3
    for i in range(iters):
        # find top best next routes - returns a set of edges
        # use Routes::freeNodes() instead of nextEdge.end
        # need to know which route each end is associated with
        #for ne in routes.rlist:
        #    bestCs.append(costFunction.w(delta, ne.end, cs, depot, width) )
        #
        #potentialRoutes = [(c.end, greedyRoute(costFunction, delta, c.end, cs, depot)) \
        #                        for c in bestCs]
        ''' These next few lines are the only things that are different in the main
            loops of Hc and Hg.'''
       

       
        print("From node {}".format(nextNode.custNo))    
        print(cs)    

        bestCs = costFunction.bestNodes(delta, routes.rlist, cs, depot, width)
        print("Best next nodes are: {}".format(bestCs))

        potentialRoutes = [(route, node, greedyRoute(costFunction, delta, node, cs, depot)) \
            for route, node, cost in bestCs]

        print("Cost of potential full routes are: {}".format([p for p in potentialRoutes]))


        nextCust, nextRoute = min(potentialRoutes, key = lambda r,n,c: r.cost())
        print("Best choice is: {}".format(nextCust))

        nextNode = (nextCust, costFunction.g(delta, nextCust, nextCust))
        print("Adding this edge to graph: {}".format(nextEdge))

        route.append(*nextEdge)
        print("Now, most complete graph so far: {}".format(route))
        print("Total current cost of that graph: {}".format(route.cost()))
        cs.remove(nextCust)
        print("Remaining custoemrs to plot: {}".format(cs))

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


