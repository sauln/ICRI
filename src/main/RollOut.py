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
    sp.prepare()
    depot = sp.customers[0]
    customers = sp.customers[1:]
    delta = [1]*7

    routes = Routes(sp, depot)

    # take routes - find top 5 from routes
    # compute complete path using these 5 as start
    # choose best and add that node to route 
    heuristic = Heuristic(sp)

    startTime = time.clock()
    startTime = time.clock()

    #for i in range(len(customers)):
    for i in range(91):

        #print("customers left: {}".format(len(customers)))
        #heuristic.setup(delta, depot, customers, depot)
        #heuristic.routes = routes
        bests = routes.getBestNNodes(heuristic.costFunction, delta, customers, 5)
        #print("Bests: {}".format(bests))

        ranked = sortedcontainers.SortedListWithKey(key=lambda x: x[1])
        for vehicle, bestNext, cost in bests:
            _t_routes = heuristic.setup(delta, bestNext, customers, depot).run(3)
            solution = (_t_routes, _t_routes.cost() + cost, vehicle, bestNext)
            ranked.add(solution)

        topRollOut = ranked[0]
        customers.remove(topRollOut[3])
        routes.addNext(topRollOut[2], topRollOut[3])

    return routes
