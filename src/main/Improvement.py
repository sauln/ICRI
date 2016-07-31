import pickle

import sortedcontainers
import numpy as np
from src.visualization.visualize import PlotRoutes 

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

def geographicSimilarity(routes, seedRoute, closeCount):
    base = seedRoute.geographicCenter() 
    
    distL = lambda x: diff(base, x.geographicCenter())
    dist = sortedcontainers.SortedListWithKey(key = distL)
    for r in routes:
        dist.add(r)

    return dist[:closeCount]

def flattenRoutes(routes):
    return list({c for route in routes for c in route})

def Improvement(routes):
    r1 = shortestRoute(routes)
    simRoutes = geographicSimilarity(routes, r1, 5)
    print("Most {} similar routes {}".format(len(simRoutes), simRoutes))

    customers = flattenRoutes(simRoutes)
    print("All the customers: {}".format(customers))

    PlotRoutes(simRoutes)       
    
if __name__ == "__main__":
    with open("data/interim/tmpr101.p", "rb") as f:
        routes = pickle.load(f)

    Improvement(routes)

