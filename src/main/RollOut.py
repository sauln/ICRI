import time
import sys
import sortedcontainers
from copy import copy, deepcopy

from src.main.Vehicle import Vehicle
from src.main.Heuristic import Heuristic
from src.main.Routes import Routes
from src.main.Parameters import Parameters

def rollOut(heuristic, delta, customers, bests):
    pm = Parameters()
    ranked = sortedcontainers.SortedListWithKey(key=lambda x: x[1])
    for vehicle, bestNext, cost in bests:
        _t_routes = heuristic.run(delta, bestNext, customers, pm.depot, pm.searchDepth)
        nextCost = vehicle.travelDist(bestNext)
        solution = (_t_routes, _t_routes.cost() + nextCost , vehicle, bestNext)
        ranked.add(solution)

    return ranked[0]

# these costs need to be better developed
def c(routes, end=None):
    return 1

def combineRoutes(frontSequence, endSequence):
    # shallow copy might not copy the routes objects?!
    routes = deepcopy(frontSequence)
    if(endSequence[0][0].custNo != 0):
        lastVehicle = routes[-1]
        restOfVehicle = endSequence.pop(0) 
        for cust in restOfVehicle[1:]:
            lastVehicle.append(cust)
    
        assert lastVehicle != frontSequence[-1], "Need to make deeper copy"
        # last or first is depot - should be separate vehicles
    for route in endSequence:
        routes.objList.append(route)
    
    return routes

def H_c():
    pm = Parameters()
    depot = pm.depot
    customers = list(pm.customers)

    # need to maintain two routes objects
    routes = Routes(depot)
    bestSequence = Routes(depot)
    heuristic = Heuristic()

    # don't need 'start' because we can grab off end of list
    start = depot
    numVehicles = minNumVeh = lowestCost = float("inf") 
    lowerLimit = 12
    W = 100

    Delta = [[10,1,1,1,1,1,1]]
    lowestVehicle = bestSequence[-1]
    custCopy = list(customers)

    for d in Delta:
        while len(custCopy) > 0 and lowerLimit < numVehicles and numVehicles <= minNumVeh:
            width = min(W, len(custCopy))

            # there are multiple ways we can structure this
            topCusts = heuristic.costFunction.lowestCostNext(lowestVehicle,  d, \
                                                             custCopy,  5)

            lowestCost = float('inf')
            for vehicle, cust, cost in topCusts:
                projectedRoute = heuristic.run(d, cust, custCopy, depot, width) 
        
                tCost = c(bestSequence) + c(vehicle, cust) + c(projectedRoute)
                if tCost < lowestCost:
                    lowestCost = tCost
                    lowestNext = cust
                    lowestVehicle = vehicle
                    lowestProjectedRoute = projectedRoute

            custCopy.remove(lowestNext)
            bestSequence.addNext(lowestVehicle, lowestNext)
            routes = combineRoutes(bestSequence,  lowestProjectedRoute)
            numVehicles = len(routes)
            
        custCopy = list(customers)
        if minNumVeh > numVehicles:
            minNumVeh = numVehicles
    return bestSequence


def constructRoute():
    routes = H_c() 
    routes.finish()
    return routes
