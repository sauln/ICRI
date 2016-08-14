''' 
main layers:
dispatch - controller for everything, asserts business rules
vehicle - state machine, only concerned with tracking current states
        


'''








class Dispatch():
    ''' This organizes the customers, visited customers, and vehicles''' 
    ''' Will be similar to the parameters - and should be the only interface
        to the parameters
    '''
    
    def __init__(self):
        pass

class Customer():
    def __init__(self, x, y, start, end):
        self.x = x
        self.y = y
        self.start = start
        self.end = end
    def __str__(self):
        return "({},{})+({},{})".format(self.x,self.y,self.start,self.end)
    def __repr__(self):
        return self.__str__() 

class VisitedCustomer():
    def __init__(self, customer):
        self.customer = customer
        
class Vehicle():
    ''' Vehicle will just keep track of state '''
    def __init__(self):
        self.edges = []

class Dispatch():
    def __init__(self):
        pass

def dist(a,b):
    # make this into a dynamic programming shiz!
    return np.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

def isFeasible(a, b):
    # print("{} + {} <= {}".format(a.start, dist(a,b), b.end))
    return a.start + dist(a,b) <= b.end

def build_feasible_graph(customers):
    graph = {}
    for customer in customers:
        graph[customer] = [c for c in customers 
            if isFeasible(customer, c) and c is not customer]
    return graph

def cost(start, c):
    # travel dist, measure of how much time remaining.
    return dist(start,c) + (c.end)

def plotNextOptions(key, value):
    pts = [[key, v] for v in value]
    for path in pts:
        Plotter().plotRoute(path)
    Plotter().plotCenter(key).plotCustomers(customers).show()

import random
#from src.visualization.visualize import Plotter
from src.visualization.visualize import Plotter

maxTime = 100
minTime = 10
maxCoord = 20

random.seed(0)

depot = Customer(0,0,0, maxTime) 
customers = [depot]


for i in range(25):
    start = random.randint( minTime, maxTime)
    end = start + 10
    customers.append(Customer(random.randint(-maxCoord, maxCoord),\
                              random.randint(-maxCoord, maxCoord),\
                              start, end))

from collections import defaultdict
import numpy as np

graph = build_feasible_graph(customers)

start = depot
for i in range(3):
    distL = lambda x: cost(start,x)
    nextC = min(graph[start], key = distL)
    plotNextOptions(start, graph[start])
    start = nextC

#for key, value in graph.items():
#    plotNextOptions(key, value)



