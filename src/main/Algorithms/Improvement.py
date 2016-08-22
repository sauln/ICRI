import pickle
import copy
import sortedcontainers
import numpy as np
import random

from src.visualization.visualize import Plotter
from src.main.BaseObjects.Parameters import Parameters
from src.main.Algorithms.RollOut import RollOut 


class Improvement():
    def __init__(self):
        pass

def shortestRoute(solution):
    # this can go in routes class
    sortedRoutes = sortedcontainers.SortedListWithKey(\
        key = lambda x: (len(x.customerHistory), x.totalDist))
    sortedRoutes.update(solution.vehicles)
    r = random.randint(0,5)
    rbest = sortedRoutes[0] 
    return rbest 

def geographicSimilarity(dispatch, vehicle):
    base = vehicle.geographicCenter() 

    distL = lambda x: np.linalg.norm(np.asarray(vehicle.geographicCenter()) \
                                   - np.asarray(x.geographicCenter()))
    dist = sortedcontainers.SortedListWithKey(key = distL)
    dist.update(dispatch.vehicles)

    return dist[:5]

def flattenRoutes(routes):
    return list({c for route in routes for c in route})

def replaceRoutes(base, oldRoutes, newRoutes):
    for r in oldRoutes:
        base.objList.remove(r)

    for r in newRoutes:
        base.objList.append(r)

def betterThan(firstRoutes, secondRoutes):
    if(len(firstRoutes) != len(secondRoutes)):
        return len(secondRoutes) < len(firstRoutes)
    else:
        c1 = sum(r.totalDist for r in firstRoutes)
        c2 = sum(r.totalDist for r in secondRoutes)
        print("Compare close solutions: {}<{}".format(c1,c2))
        return c2 < c1

def setupNextRound(simRoutes):
    customers = flattenRoutes(simRoutes)
    customers.remove(Parameters().depot) 
    Parameters().customers = customers 

def candidateRoutes(dispatch):
    r1 = shortestRoute(dispatch)
    simRoutes = geographicSimilarity(dispatch, r1)
    return simRoutes

def Improvement(dispatch):
    dispatchTmp = copy.deepcopy(dispatch) 
    custBk = copy.deepcopy(Parameters().customers)
  

    simRoutes = candidateRoutes(dispatchTmp)
    print(simRoutes) 
    setupNextRound(simRoutes)
    
    
    '''
    for i in range(5):
        newRoutes = RollOut().constructRoute()

        Plotter().beforeAndAfter(simRoutes, newRoutes).show()
        
        if(betterThan(simRoutes, newRoutes)):
            print("This solution better {} >= {}".format(len(simRoutes), len(newRoutes)))
            replaceRoutes(routesWork, simRoutes, newRoutes)
    '''

    # Parameters().customers = custBk

    return dispatchTmp

if __name__ == "__main__":
    with open("data/interim/SolutionR101.p", "rb") as f:
        routes = pickle.load(f)
    with open("data/interim/r101.p", "rb") as f:
        sp = pickle.load(f)

    parameters = Parameters()
    parameters.build(sp, 10, 20)
    
    newRoutes = Improvement(routes)
    # Plotter().beforeAndAfter(routes, newRoutes).show()


