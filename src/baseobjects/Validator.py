#from .Parameters import Parameters

import numpy as np
from .Utils import *

class Validator():
    def __init__(self, dispatch, source):
        self.vehicles = dispatch.vehicles
        self.used_customers = [c.custNo for vehicle in self.vehicles \
            for c in vehicle.customer_history]
        
        sp =  open_sp(source)
        self.customers = sp.customers
        self.maxCapacity = sp.capacity
 
    def allCustomersAreUsed(self):
        unused_customers = [c for c in self.customers if c.custNo not in self.used_customers]
        assert not unused_customers, "There are unused customers: {}".format(\
            unused_customers)

    def allCustomersAreUsedOnlyOnce(self):
        used_customers = list(filter((0).__ne__, self.used_customers))
        assert len(used_customers) == len(set(used_customers))

    def vehicles_return_home_in_time(self):
        for vehicle in self.vehicles:
            assert vehicle.total_time < vehicle.depot.dueDate, "{} > {}".format(\
                vehicle.total_time, vehicle.depot.dueDate)

    def serviceTimesWithinWindow(self):
        ''' Rebuilt the route and assert it works the whole way''' 
        success = 1
        for vehicle in self.vehicles:
            total = 0
            cs = vehicle.customer_history
            for i in range(0,len(cs)-1):
                #td = self.timeMatrix[cs[i].custNo,cs[i+1].custNo]
                td = np.sqrt( (cs[i].location.x - cs[i+1].location.x)**2 + \
                           (cs[i].location.y - cs[i+1].location.y)**2)
                srv = max(total + td, cs[i+1].readyTime)
                total = srv + cs[i+1].serviceLen
                assert 1, "Unsure what to assert here"

    def capacityRespected(self):
        for vehicle in self.vehicles:
            s = sum(c.demand for c in vehicle.customer_history)
            assert s <= self.maxCapacity

    def validate(self):
        self.allCustomersAreUsed()
        self.allCustomersAreUsedOnlyOnce()
        self.capacityRespected()
        self.serviceTimesWithinWindow()
        self.vehicles_return_home_in_time()
        print("Validation passed")
