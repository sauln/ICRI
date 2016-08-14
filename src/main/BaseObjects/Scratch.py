''' 
main layers:
dispatch - controller for everything, asserts business rules
vehicle - state machine, only concerned with tracking current states
        


'''


def plotNextOptions(key, value):
    pts = [[key, v] for v in value]
    for path in pts:
        Plotter().plotRoute(path)
    Plotter().plotCenter(key).plotCustomers(customers).show()


def buildRandomCustomers(num=25):
    maxTime = 100
    minTime = 10
    maxCoord = 20

    random.seed(0)

    depot = Customer(0,Point(0,0), 0, 0, maxTime, 0) 
    customers = []

    for i in range(25):
        p = Point(random.randint(-maxCoord, maxCoord),\
                  random.randint(-maxCoord, maxCoord))
        start = random.randint( minTime, maxTime)
        end = start + 10

        customers.append(Customer(i+1, p, 10, start, end, 10))
    return depot, customers


import random
from src.visualization.visualize import Plotter
from collections import defaultdict
import numpy as np

from src.main.BaseObjects.Customer import Customer, Point
from src.main.BaseObjects.Routes import Dispatch


depot, customers = buildRandomCustomers()
dispatch = Dispatch(customers, depot)


# get best next
# move from available customers to vehicle






#start = depot
#for i in range(3):
#    distL = lambda x: cost(start,x)
#    nextC = min(graph[start], key = distL)
#    plotNextOptions(start, graph[start])
#    start = nextC

#for key, value in graph.items():
#    plotNextOptions(key, value)



