# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv

import pickle
import sortedcontainers

from src.model.CostFunction import CostFunction
from src.visualization.visualize import PlotRoutes 

class Route():
    def __init__(self):
        self.route = []
        self.edges = []

    def append(self, item, cost):
        self.edges.append( ((self.route if len(self.route) > 0 else None, item), cost) )
        self.route.append(item)

    def cost(self):
        return sum( cost for edge, cost in self.edges )

    def __str__(self):
        s = self.cost()
        a = ' => '.join(str(i) for i in self.route)
        #a = '-'.join(str(i.start.custNo) for i in self.route)
        return "Distance: {0:.4g} {1}".format(s, a)

    def __repr__(self):
        return "{:.4g}:({}, {})".format( \
            self.cost(), self.route[0].custNo, self.route[-1].custNo) 

    def __getitem__(self, index):
        return self.route[index]

    def __setitem__(self,index,value):
        self.route[index] = value


class Routes():
    def __init__(self):
        self.rList = [[]] 

    def cost(self):
        # cost function of route set
        return 1

    def setFirstNode(self, item):
        self.rList[0] = [item]

    def getBestNodes(self, delta, customers, depot, width):
        # used in Hc
        cs = sortedcontainers.SortedListWithKey(key=lambda x: x[2])
        
        for r in self.routes:
            feasible, _ = self.partitionFeasible(r[-1], customers)
            for c in feasible:
                cs.append((r, c, self.g(delta, r[-1])))

        return cs[:width]


    # in H_g, we need to consider the infeasible nodes also
    #
    def getBestNode(self, delta, customers, depot):
        cs = sortedcontainers.SortedListWithKey(key=lambda x: x[2])

        for r in self.routes:
            feasible, infeasible = self.partitionFeasible(r[-1], customers)
            for c in feasible:
                cs.append((r,c,self.g(delta, r[-1])))
            for c in infeasible:
                cs.append((r,depot,self.g(delta, depot)))

        return cs[0]

    def __str__(self):
        return "{}".format(self.rList)



def isFeasible(cf, start, end):
    return start.serviceTime() + cf.timeMatrix[start.custNo, end.custNo] <= \
           end.dueDate + end.serviceLen

def heuristic(cf, delta: [float], custStart, custEnd, depot):
    # Infeasible nodes would be filtered before here - 

    start = custStart
    #if(isFeasible(cf, custStart, custEnd)):
    #    start = custStart
    #else:
    #    start = depot

    
    cost = delta[0] * (start.custNo == 0) +\
           delta[1] * cf.distMatrix[start.custNo, custEnd.custNo] +\
           delta[2] * cf.timeMatrix[start.custNo, custEnd.custNo]

    return (start, custEnd, cost) 

def getBestNode(cf, delta, routes, customers, depot):
    cs = sortedcontainers.SortedListWithKey(key=lambda x: x[3])


    # with lots of routes, this could become unreasonable
    for r in routes:
        for c in customers:
            res = (r,) + heuristic(cf, delta, r[-1], c, depot) 
            cs.add(res)

    return cs[0]



def buildRoute(costFunction, delta, start, customers, depot):
    routes = Routes()

    routes.setFirstNode(start)
    nextNode = start        
    
    for i in range(len(customers)):
        route, start, bestNext, cost = \
            getBestNode(costFunction, delta, routes.rList, customers, depot)
        print("{}, {} => {}, {}".format(route,start.custNo,bestNext.custNo,cost))

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
    cf = CostFunction(sp.customers) 
    
    depot = sp.customers[0]
    cs    = sp.customers[1:]
    delta = [1]*7
    
    routes = buildRoute(cf, delta, depot, cs, depot)    
    print(routes)
    #visualizeRoutes(routes)
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





