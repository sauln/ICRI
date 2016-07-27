import numpy as np


class CostFunction():
    def __init__(self, heuristicType, timeMatrix, distMatrix):
        self.switch = {"gnnh":self.gnnh}
        self.heuristicType = heuristicType
        self.timeMatrix = timeMatrix
        self.distMatrix = distMatrix

    def run(self, *args):
        return self.switch[self.heuristicType](*args)

    def gnnh(self, delta, vehicle, end): #s:start, e:end customers
        s = vehicle.lastCustomer()
        e = end

        # Infeasible nodes would be filtered before here -
        prevDeparture = vehicle.totalTime
        nextArrivalTime = prevDeparture + self.timeMatrix[s.custNo, e.custNo]
        earliestService = max(nextArrivalTime, e.readyTime)

        c = np.zeros(len(delta))
        c[0] = (s.custNo == 0)
        c[1] = self.distMatrix[s.custNo, e.custNo]
        c[2] = earliestService - prevDeparture
        c[3] = e.dueDate - (prevDeparture + self.timeMatrix[s.custNo,e.custNo])
        c[4] = (vehicle.maxCapacity - vehicle.curCapacity) - e.demand # slack
        #d[5] = max(0, c_from.service_window[0] - earliest_possible_service)
        #d[6] = max(0, c_from_service_time - c_from.service_window[1])

        cost = np.dot(delta, c)    
        return cost 

