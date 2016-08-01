import pickle
import copy
import sortedcontainers
import numpy as np


from src.visualization.visualize import Plotter
from src.main.Parameters import Parameters
from src.main.RollOut import constructRoute

# improvement algorithm
# 
# take a solution set 
# 

def shortestRoute(routes):
    # this can go in routes class
    smallest = routes[0]
    for route in routes:
        if (len(route) < len(smallest)):
            smallest = route

    print("Shortest route: {}".format(smallest))
    return smallest

def diff(st, en):
    return np.linalg.norm(np.asarray(st) - np.asarray(en))

def geographicSimilarity(routes, seedRoute):
    base = seedRoute.geographicCenter() 
    
    distL = lambda x: diff(base, x.geographicCenter())
    dist = sortedcontainers.SortedListWithKey(key = distL)
    for r in routes:
        dist.add(r)

    return dist[:Parameters().topNodes]

def flattenRoutes(routes):
    return list({c for route in routes for c in route})

def replaceRoutes(base, oldRoutes, newRoutes):
    for r in oldRoutes:
        base.objList.remove(r)

    for r in newRoutes:
        base.objList.append(r)

def Improvement(routes):
    routesbk = copy.deepcopy(routes) 
    
    for i in range(5):
        r1 = shortestRoute(routes)
        simRoutes = geographicSimilarity(routes, r1)
        customers = flattenRoutes(simRoutes)
        
        customers.remove(Parameters().depot) 
        Parameters().customers = customers 
        
        newRoutes = constructRoute()
       
        replaceRoutes(routes, simRoutes, newRoutes)
    
    Plotter().beforeAndAfter(routesbk, routes).show()

    print("Most {} similar routes {}".format(len(simRoutes), simRoutes))
    print("All the customers: {}".format(customers))

if __name__ == "__main__":
    with open("data/interim/tmpr101.p", "rb") as f:
        routes = pickle.load(f)
    with open("data/interim/r101.p", "rb") as f:
        sp = pickle.load(f)

    parameters = Parameters()
    parameters.build(sp, 10, 20)
    
    Improvement(routes)

