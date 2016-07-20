# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv

import pickle
import sortedcontainers
import numpy as np

#from src.model.CostFunction import CostFunction
from src.visualization.visualize import PlotRoutes 
from src.main.Matrices import Matrices
from src.main.Routes import Route, Routes
from src.main.Validator import Validator

""" Feasibility functions """
def isNotFull(sp, route, end):
    curCapacity = route.capacity
    capacity = sp.capacity >= end.demand + curCapacity
    return capacity

def isValidTime(sp, route, end):
    """ For soft time windows, add losen constraints here """ 
    start = route[-1]

    # does the entire operation need to be done before the due date?
    travelTime = sp.timeMatrix[start.custNo, end.custNo]

    earliest = start.serviceTime() + travelTime #+ end.serviceLen 
    latest = end.dueDate

    validTime = earliest <= latest
    return validTime

def isFeasible(sp, route, end):
    notFull  = isNotFull(sp, route, end)
    validTime = isValidTime(sp, route, end)
    return (validTime and notFull)

def heuristic(sp, delta, r, e, depot): #s:start, e:end customers
    s = r[-1]

    # Infeasible nodes would be filtered before here - 
    prevDeparture = s.serviceTime() + s.serviceLen
    nextArrivalTime = prevDeparture + sp.timeMatrix[s.custNo, e.custNo]
    earliestService = max(nextArrivalTime, e.readyTime)

    c = np.zeros(len(delta))
    c[0] = (s.custNo == 0)
    c[1] = sp.distMatrix[s.custNo, e.custNo]
    c[2] = earliestService - prevDeparture
    c[3] = e.dueDate - (prevDeparture + sp.timeMatrix[s.custNo,e.custNo])
    c[4] = r.capacity - e.demand
    #d[5] = max(0, c_from.service_window[0] - earliest_possible_service)
    #d[6] = max(0, c_from_service_time - c_from.service_window[1])

    cost = np.dot(delta, c)    
    return (s, e, cost) 

""" Ranking algorithms """
def getBestNNodes(sp, delta, routes, customers, depot, size):
    cs = sortedcontainers.SortedListWithKey(key=lambda x: x[3])
    
    # with lots of routes, this could become unreasonable
    # is there any faster way than to look at all of them?
    for r in routes:
        for c in customers:
            if(isFeasible(sp, r, c)):
                res = (r,) + heuristic(sp, delta, r, c, depot) 
                cs.add(res)

    return cs[:size]

def getBestNode(sp, delta, routes, customers, depot):
    return getBestNNodes(sp, delta, routes, customers, depot, 1)[0]

""" Route building """
def addNext(sp, routes, route, start, end):
    if(start.custNo == 0): #the depot
        routes.rList.append(Route(sp, start, end))
    else:
        route.append(end)

    return routes

def buildRoute(sp, delta, start, customers, depot):
    routes = Routes(sp, start)

    for i in range(len(customers)):
        route, start, bestNext, cost = getBestNode(sp, delta, routes, customers, depot)
        routes = addNext(sp, routes, route, start, bestNext)
        customers.remove(bestNext)
   
    # add depot to the end of each route
    
    if(len(routes[0]) == 1): # remove our place holder depot route
        routes.pop(0)

    for r in routes: # add depot to end of each route 
        r.append(depot)

    return routes

def confirmSolution(sp, routes):

    v = Validator(sp, routes).validate()
    print("There are {} vehicles with {} allowed"\
        .format(len(routes), sp.numVehicles))
   


'''
def c(routes):
    return 1

def constructRoute(sp):
    # find top n nodes,
    # compute route for each of them
    # choose next node and add to route
   
    # setup
    sp.prepare()
    depot = sp.customers[0]
    customers = sp.customers[1:]
    delta = [1]*7

    routes = Routes(depot)
    ranked = sortedcontainers.SortedListWithKey(key=lambda x: x[1])

    # find next best n
    #[route, start, bestNext, cost] = 
    bestNexts = getBestNNodes(sp, delta, routes, customers, depot, 5)
  
    print(bestNexts)
    for route, start, n, cost in bestNexts:
        best = buildRoute(sp, delta, start, customers, depot)
        ranked.append((best, c(best) + cost))

    routes.add(ranked[0])  
    return routes
'''    




@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    logger = logging.getLogger(__name__)
    logger.info("Begin auxiliary algorithm file")
    logger.info('Loading Solomon Problem file {}'.format(input_filepath))

    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)

    logger.info('Generating matrices for problem')
    
    sp.prepare()
    depot = sp.customers[0]
    customers = sp.customers[1:]
    delta = [1]*7
    delta[0] = 1 
    #constructRoute(sp)
    routes = buildRoute(sp, delta, depot, customers, depot)
    confirmSolution(sp, routes)
    #PlotRoutes(routes)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

