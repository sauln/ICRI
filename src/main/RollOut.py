
def rollOut(sp, delta, routes, customers, depot):
    bestNexts = getBestNNodes(sp, delta, routes, customers, depot, 5)

    # these need to be objects
    ranked = sortedcontainers.SortedListWithKey(key=lambda x: x[1])
    for route, start, end, cost in bestNexts:
        best = buildSolution(sp, delta, start, customers, depot)
        solution = (best, best.cost() + cost, route, start, end)
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

    # find next best n
    #[route, start, bestNext, cost] =

    startTime = time.clock()

    for i in range(len(customers)):
        print("begin {} at time {}".format(i, time.clock()-startTime))
        startTime = time.clock()
        r, s, e = rollOut(sp, delta, routes, customers, depot) 
        routes = addNext(sp, routes, r, s, e)
        customers.remove(e)


        #print("Routes at end of {}th iteration: {}".format(i, routes))
    return routes
