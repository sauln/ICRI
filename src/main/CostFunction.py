import numpy as np
from src.main.Parameters import Parameters

class CostFunction():
    def __init__(self, heuristicType):
        self.switch = {"gnnh":self.gnnh, "distanceOnly":self.distanceOnly}
        self.heuristicType = heuristicType

    def run(self, *args):
        return self.switch[self.heuristicType](*args)

    def distanceOnly(self, delta, vehicle, end):
        return vehicle.travelDist(end)

    def gnnh(self, delta, vehicle, end): #s:start, e:end customers
        # Infeasible nodes would be filtered before here -
        nextArrivalTime = vehicle.totalTime + vehicle.travelTime(end)
        earliestService = max(nextArrivalTime, end.readyTime)

        c = np.zeros(len(delta))
        isDepot     = (vehicle.last().custNo == 0)
        travelDist  = vehicle.travelDist(end)
        remaining   = earliestService - vehicle.totalTime
        timeSlack   = end.dueDate - (vehicle.totalTime + vehicle.travelTime(end))
        capSlack    = (vehicle.maxCapacity - vehicle.curCapacity) - end.demand # slack
        #d[5] = max(0, c_from.service_window[0] - earliest_possible_service)
        #d[6] = max(0, c_from_service_time - c_from.service_window[1])

        c[0], c[1], c[2], c[3], c[4] = isDepot, travelDist, remaining, timeSlack, capSlack
        #print("Depot {}, travelDist {:3g}, remaining {},\ntimeSlack {:3g}, capSlack {}\n"\
        #    .format(isDepot, travelDist, remaining, timeSlack, capSlack))
        
        
        cost = np.dot(delta, c)    
        return cost 

