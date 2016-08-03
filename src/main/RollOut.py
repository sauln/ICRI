import time
import sortedcontainers
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

'''
def H_c():
    start = depot
    bestSequence = depot
    numVehicles = minNumVeh = lowestCost = MAXINT
    custCopy = list(customers)

    lowerLimit = 25

    for d in Delta:
        while len(custCopy) > 0 and lowerLimit < numVehicles and numVehicles <= minNumVeh:
            width = min(W, len(custCopy))
            topCusts = w(start, custCopy, g, width)
            for cust in topCusts:
                tCost = c(bestSequence.append(cust) + c(builtRoute(d, cust, custCopy, depot)
                if tCost < lowestCost:
                    lowestCost = tCost
                    lowestNext = cust
            start = lowestNext
            custCopy.remove(lowestNext)
            bestSequence.append(lowestNext)
            routes = bestSequence + builtRoute(d, lowestNext, custCopy, depot)
            numVehicles = routes.size()
        custCopy = list(customers)
        if minNumVeh > numVehicles
            minNumVeh = numVehicles
    
'''





def constructRoute():
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

    return routes
