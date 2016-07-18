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


def isNotFull(sp, route, end):
    curCapacity = route.capacity
    capacity = sp.capacity >= end.demand + curCapacity
    return capacity

def isValidTime(sp, route, end):
    start = route[-1]
    earliest = start.serviceTime() + sp.distMatrix[start.custNo, end.custNo]  
    latest = end.dueDate + end.serviceLen

    print("Earliest: {}\t\t Latest: {}".format(earliest, latest))
    validTime = earliest <= latest
    return validTime


def isFeasible(sp, route, end):
    print(route, end)
    capacity  = isNotFull(sp, route, end)
    validTime = isValidTime(sp, route, end)
    return (validTime and capacity)

def heuristic(sp, delta, s, e, depot, capacity): #s:start, e:end customers
    # Infeasible nodes would be filtered before here - 
    prevDeparture = s.serviceTime() + s.serviceLen
    nextArrivalTime = prevDeparture + sp.timeMatrix[s.custNo, e.custNo]
    earliestService = max(nextArrivalTime, e.readyTime)

    c = np.zeros(len(delta))
    c[0] = (s.custNo == 0)
    c[1] = sp.distMatrix[s.custNo, e.custNo]
    c[2] = earliestService - prevDeparture
    c[3] = e.dueDate - (prevDeparture + sp.timeMatrix[s.custNo,e.custNo])
    c[4] = capacity - e.demand
    #d[5] = max(0, c_from.service_window[0] - earliest_possible_service)
    #d[6] = max(0, c_from_service_time - c_from.service_window[1])

    cost = np.dot(delta, c)    
    return (s, e, cost) 

def getBestNNodes(sp, delta, routes, customers, depot, size):
    cs = sortedcontainers.SortedListWithKey(key=lambda x: x[3])
    # with lots of routes, this could become unreasonable
    # is there any faster way than to look at all of them?

    for r in routes:
        for c in customers:
            if(isFeasible(sp, r, c)):
                res = (r,) + heuristic(sp, delta, r[-1], c, depot, r.capacity) 
                cs.add(res)

    return cs[:size]

def getBestNode(sp, delta, routes, customers, depot):
    return getBestNNodes(sp, delta, routes, customers, depot, 1)[0]

def addNext(routes, route, start, end):
    #print("To {}, adding {} => {}".format(routes, end, start))

    if(start.custNo == 0): #the depot
        routes.rList.append(Route(start, end))
    else:
        route.append(end)

    return routes

def buildRoute(sp, delta, start, customers, depot):
    #print("Begin build route")    
    routes = Routes(start)
    #print(routes)

    for i in range(len(customers)):
    #for i in range(3):
        route, start, bestNext, cost = getBestNode(sp, delta, routes, customers, depot)
        routes = addNext(routes, route, start, bestNext)
        #print("Customers: {}".format(customers) )
        customers.remove(bestNext)
    
    return routes




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
   
    #constructRoute(sp)
    routes = buildRoute(sp, delta, depot, customers, depot)

    print(routes)
    #routes = buildRoute(sp, delta, depot, cs, depot)    
    #print("Look here, the routes: \n{}".format(routes))
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

