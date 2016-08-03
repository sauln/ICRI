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
        #print("Roll out {} from {}.".format(bestNext, vehicle))
        _t_routes = heuristic.setup(delta, bestNext, customers, pm.depot)\
            .run(pm.searchDepth)
        nextCost = vehicle.travelDist(bestNext)
        solution = (_t_routes, _t_routes.cost() + nextCost , vehicle, bestNext)
        ranked.add(solution)

    return ranked[0]

def c(routes, end=None):
    return 1


def combineRoutes(frontSequence, endSequence):
    # shallow copy might not copy the routes objects?!
    print("In combine routes:") 
    
    #print("Combining {} with {}".format(frontSequence, endSequence))
    #for r in frontSequence:
    #    print("Details of frontsequence: {}".format(r))
    routes = deepcopy(frontSequence)
    if(endSequence[0][0].custNo != 0):
        lastVehicle = routes[-1]
        restOfVehicle = endSequence.pop(0) 
        print("joining two half complete vehicles together, {}+{}".format(lastVehicle, restOfVehicle))
        for cust in restOfVehicle:
            #print("adding {} to {}".format(cust, lastVehicle))
            
            lastVehicle.append(cust)
            #print("now routes looks like: {}".format(routes))
    

        assert lastVehicle != frontSequence[-1], "Need to make deeper copy"
        # last or first is depot - should be separate vehicles
    for route in endSequence:
        routes.objList.append(route)
    return routes



def H_c():
    pm = Parameters()

    depot = pm.depot
    customers = list(pm.customers)

    print("Construct routes")
    print("depot: {}, {}".format(depot, customers))

    # need to maintain two routes objects
    routes = Routes(depot)
    bestSequence = Routes(depot)
    heuristic = Heuristic()

    # don't need 'start' because we can grab off end of list
    start = depot
    numVehicles = minNumVeh = lowestCost = float("inf") 
    lowerLimit = 12
    W = 100

    Delta = [[1,1,1,1,1,1,1]]
    lowestVehicle = bestSequence[-1]
    custCopy = list(customers)

    for d in Delta:

        print("Best sequence: {}".format(bestSequence))

        while len(custCopy) > 0 and lowerLimit < numVehicles and numVehicles <= minNumVeh:
            width = min(W, len(custCopy))
            print("Width: {}".format(width))
            # like getbestNNodes, but not from any vehicle
            # move this into the CostFunction object?
            topCusts = routes.lowestCostNext(heuristic.costFunction, lowestVehicle,\
                                             d, custCopy, 5)

            print("Top  5 customers: {}".format(topCusts))
            lowestCost = float('inf')
            for vehicle, cust, cost in topCusts:
                #   for cust in topCusts:
                # need to be able to see cost w/o actually appnding
                # H_r can stop at the end of the vehicle, or keep going
               
                print("checking out adding {} to {}".format(cust, vehicle))
                 

                projectedRoute = heuristic.setup(d, cust, custCopy, depot).run(width) 
        
                tCost = c(bestSequence) + c(vehicle, cust) + c(projectedRoute)
                if tCost < lowestCost:
                    lowestCost = tCost
                    lowestNext = cust
                    lowestVehicle = vehicle
                    lowestProjectedRoute = projectedRoute

            print("Adding best customer {} onto best vehicle: {}".format(lowestNext, lowestVehicle))


            custCopy.remove(lowestNext)


            print("Bestsequence before combined: {}".format(bestSequence))
            print("type bestsequence : {}".format(type(bestSequence)))
            routes = combineRoutes(bestSequence,  lowestProjectedRoute)
            bestSequence.addNext(lowestVehicle, lowestNext)
            
            print("Bestsequence after combined: {}".format(bestSequence))
            print("best routes so far: {}".format(routes))
            numVehicles = len(routes)
       
            print("stoping conditions: custs left:  {}, numvehicles {} \
                lowerlimit {}, minnumveh: {}"\
                .format(len(custCopy),numVehicles, lowerLimit ,minNumVeh))
            print("min<inf {}".format(numVehicles < minNumVeh))
            print("lowerlimit< numvehicles {}".format(lowerLimit < numVehicles))
            
        custCopy = list(customers)
        if minNumVeh > numVehicles:
            minNumVeh = numVehicles
    return bestSequence


def constructRoute():
    routes = H_c() 
    '''
    pm = Parameters()

    depot = pm.depot
    customers = list(pm.customers)

    print("Construct routes")
    print("depot: {}, {}".format(depot, customers))

    routes = Routes(depot)
    heuristic = Heuristic()

    #print("Routes in the very beginning {}".format(routes))
    delta = [10, 1, 1, 1, 1, 1, 1]
    
    for i in range(len(customers)):
        bests = routes.getBestNNodes(heuristic.costFunction, delta, \
                                    customers, pm.topNodes)

        #print("best next nodes: {}".format("\n".join(repr(b) for b in bests)))
        
        solution, cost, seedVehicle, seedCustomer \
            = rollOut(heuristic, delta, customers, bests)
        
        customers.remove(seedCustomer)
        routes.addNext(seedVehicle, seedCustomer)



    routes.finish()
    print("Routes:{}\n{}\n".format(len(routes),routes))
    '''
    return routes
