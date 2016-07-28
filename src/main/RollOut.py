import time
import sortedcontainers
from src.main.Vehicle import Vehicle
from src.main.Heuristic import Heuristic
from src.main.Routes import Routes


def rollOut(heuristic):
    
    #def setup(self, delta, start, customers, depot):
    bestNexts = heuristic.getBestNNodes(5)
    #bestNexts = routes.getBestNNodes(sp, delta, routes, customers, depot, 5)

    # these need to be objects
    ranked = sortedcontainers.SortedListWithKey(key=lambda x: x[1])
    for vehicle, bestNext, cost in bestNexts:
        heuristic.reset(bestNext)
        best = heuristic.run()
        solution = (best, best.cost() + cost, vehicle, bestNext)
        ranked.add(solution)

    b, c, r, s, e = ranked[0]
    return r, s, e

def constructRoute(sp):
    # find top n nodes,
    # compute route for each of them
    # choose next node and add to route
   
    # setup

    topNodes = 5
    searchDepth = 10
    

    sp.prepare()
    depot = sp.customers[0]
    customers = sp.customers[1:]
    delta = [1]*7

    routes = Routes(sp, depot)
    heuristic = Heuristic(sp)

    startTime = time.clock()
    for i in range(len(customers)):
        bests = routes.getBestNNodes(heuristic.costFunction, delta, customers, topNodes)

        ranked = sortedcontainers.SortedListWithKey(key=lambda x: x[1])
        for vehicle, bestNext, cost in bests:
            _t_routes = heuristic.setup(delta, bestNext, customers, depot).run(searchDepth)
            solution = (_t_routes, _t_routes.cost() + cost, vehicle, bestNext)
            ranked.add(solution)

        topRollOut = ranked[0]
        customers.remove(topRollOut[3])
        routes.addNext(topRollOut[2], topRollOut[3])

    routes.finish()

    return routes
