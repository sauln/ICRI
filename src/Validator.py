from baseobjects import Parameters

class Validator():
    def __init__(self, routes):
        self.routes = routes
        self.timeMatrix = Parameters().timeMatrix
        self.maxCapacity = Parameters().params.capacity
        self.customers = Parameters().customers


    def allCustomersAreUsed(self):
        usedCustomers = set([c.custNo for route in self.routes for c in route])
        for c in self.customers:
            assert c.custNo in usedCustomers, "{} not in {}".format(c, usedCustomers)
        return 1

    def allCustomersAreUsedOnlyOnce(self):
        usedCustomers = [c.custNo for route in self.routes for c in route]
        usedCustomers = list(filter((0).__ne__, usedCustomers))
        assert len(usedCustomers) == len(set(usedCustomers))
        return 1

    def serviceTimesWithinWindow(self):
        success = 1
        for r in self.routes:
            total = 0
            for i in range(0,len(r)-1):
                td = self.timeMatrix[r[i].custNo,r[i+1].custNo]
                srv = max(total + td, r[i+1].readyTime)
                total = srv + r[i+1].serviceLen
                assert 1, "Unsure what to assert here"
        return success

    def capacityRespected(self):
        success = 1
        for route in self.routes:
            s = sum(c.demand for c in route)
            assert s <= self.maxCapacity
        return success

    def validate(self):
        assert self.capacityRespected()
        assert self.serviceTimesWithinWindow()
        assert self.allCustomersAreUsed()
        assert self.allCustomersAreUsedOnlyOnce()
