

class CostFunction():
    def __init__(self, matrix):
        self.distMatrix = matrix.distMatrix
        self.timeMatrix = matrix.timeMatrix

    def w(self, delta, custStart, customers, depot, lim): 
        ns = [(self.g(delta, custStart, c), c) for c in customers] 
        return sorted(ns, key=lambda c: c[0])[:lim] 

    def g(self, delta, custStart, custEnd):
        #need to know if it is infeasible beforehand

        # need to 

        #if infeasible, return -1
        #need to start the all infeasible nodes at depot
        return delta[0] * (custStart.custNo == 0) +\
               delta[1] * self.distMatrix[custStart.custNo, custEnd.custNo] +\
               delta[2] * self.timeMatrix[custStart.custNo, custEnd.custNo]

        #return self.distMatrix[custStart.custNo, custEnd.custNo]

    #next_arrival_time = c_from.service_time + c_from.service_len + travel_time(c_from, c_to)
    #earliest_possible_service = max(next_arrival_time, c_to.service_window[0])
    #prev_departure = c_from.service_time + c_from.service_len

    #d = []
    #d[0] = 1 if (not c_from.depot) else 0
    #d[1] = distance(c_from.cid, c_to.cid)
    #d[2] = earliest_possible_service - prev_departure
    #d[3] = c_to.service_window[1] - (prev_departure + travel_time(c_from, c_to))
    #d[4] = 0# vehicle.capacity_curr - c_to.demand
    #d[5] = max(0, c_from.service_window[0] - earliest_possible_service)
    #d[6] = max(0, c_from_service_time - c_from.service_window[1])
    
    #return sum(a*b for (a,b) in zip(d,delta))

