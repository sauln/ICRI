from .Parameters import Parameters

class Validator():
    def __init__(self, dispatch):
        self.vehicles = dispatch.vehicles
        self.timeMatrix = Parameters().timeMatrix
        self.maxCapacity = Parameters().params.capacity
        self.customers = Parameters().customers
        self.used_customers = [c.custNo for vehicle in self.vehicles \
            for c in vehicle.customerHistory]
 
    def allCustomersAreUsed(self):
        for c in self.customers:
            assert c.custNo in self.used_customers, "{} not in {}".format(\
                c, self.used_customers)

    def allCustomersAreUsedOnlyOnce(self):
        used_customers = list(filter((0).__ne__, self.used_customers))
        assert len(used_customers) == len(set(used_customers))

    def vehicles_return_home_in_time(self):
        for vehicle in self.vehicles:
            assert vehicle.totalTime < vehicle.depot.dueDate, "{} > {}".format(\
                vehicle.totalTime, vehicle.depot.dueDate)

    def serviceTimesWithinWindow(self):
        success = 1
        for vehicle in self.vehicles:
            total = 0
            cs = vehicle.customerHistory
            for i in range(0,len(cs)-1):
                td = self.timeMatrix[cs[i].custNo,cs[i+1].custNo]
                srv = max(total + td, cs[i+1].readyTime)
                total = srv + cs[i+1].serviceLen
                assert 1, "Unsure what to assert here"

    def capacityRespected(self):
        for vehicle in self.vehicles:
            s = sum(c.demand for c in vehicle.customerHistory)
            assert s <= self.maxCapacity

    def validate(self):
        self.capacityRespected()
        self.serviceTimesWithinWindow()
        self.vehicles_return_home_in_time()
        self.allCustomersAreUsedOnlyOnce()
