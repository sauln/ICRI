class Routes():
    def __init__(self):
        self.rList = [[]] 

    def cost(self):
        # cost function of route set
        return 1

    def setFirstNode(self, item):
        self.rList[0] = [item]

    def getBestNodes(self, delta, customers, depot, width):
        # used in Hc
        cs = sortedcontainers.SortedListWithKey(key=lambda x: x[2])
        
        for r in self.routes:
            feasible, _ = self.partitionFeasible(r[-1], customers)
            for c in feasible:
                cs.append((r, c, self.g(delta, r[-1])))

        return cs[:width]

    # in H_g, we need to consider the infeasible nodes also
    #
    def getBestNode(self, delta, customers, depot):
        cs = sortedcontainers.SortedListWithKey(key=lambda x: x[2])

        for r in self.routes:
            feasible, infeasible = self.partitionFeasible(r[-1], customers)
            for c in feasible:
                cs.append((r,c,self.g(delta, r[-1])))
            for c in infeasible:
                cs.append((r,depot,self.g(delta, depot)))

        return cs[0]

    def __str__(self):
        return "Number of routes: {}\n".format(len(self.rList)) +\
            "\n".join("{}".format(r) for r in self.rList)
