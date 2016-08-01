import time
import sortedcontainers
from src.main.Vehicle import Vehicle
from src.main.Heuristic import Heuristic
from src.main.Routes import Routes
from src.main.Parameters import Parameters

#def rollOut(heuristic):
#    #def setup(self, delta, start, customers, depot):
#    bestNexts = heuristic.getBestNNodes(5)
#    #bestNexts = routes.getBestNNodes(sp, delta, routes, customers, depot, 5)
#
#    # these need to be objects
#    ranked = sortedcontainers.SortedListWithKey(key=lambda x: x[1])
#    for vehicle, bestNext, cost in bestNexts:
#        heuristic.reset(bestNext)
#        best = heuristic.run()
#        solution = (best, best.cost() + cost, vehicle, bestNext)
#        ranked.add(solution)
#
#    b, c, r, s, e = ranked[0]
#    return r, s, e




def rollOut(heuristic, delta, customers, bests):
    pm = Parameters()
    ranked = sortedcontainers.SortedListWithKey(key=lambda x: x[1])
    for vehicle, bestNext, cost in bests:
        # generate a solution from this root
        _t_routes = heuristic.setup(delta, bestNext, customers, pm.depot)\
            .run(pm.searchDepth)
        # this cost function is off
        nextCost = vehicle.travelDist(bestNext)
        solution = (_t_routes, _t_routes.cost() + nextCost , vehicle, bestNext)
        ranked.add(solution)

    return ranked[0]


def constructRoute():
    pm = Parameters()

    depot = pm.depot
    customers = list(pm.customers)

    routes = Routes(depot)
    heuristic = Heuristic()
    
    delta = [1]*7
    for i in range(len(customers)):
        bests = routes.getBestNNodes(heuristic.costFunction, delta, \
                                    customers, pm.topNodes)

        topRollOut = rollOut(heuristic, delta, customers, bests)
        customers.remove(topRollOut[3])
        routes.addNext(topRollOut[2], topRollOut[3])

    routes.finish()

    return routes
