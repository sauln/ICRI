import sortedcontainers
from src.main.Matrices import Matrices
from src.main.SolomonProblem import Customer

class CostFunction():
    def __init__(self, customers):
        m = Matrices(customers)
        self.distMatrix = m.distMatrix
        self.timeMatrix = m.timeMatrix

    def feasible(self, start: Customer, end: Customer) -> bool:
        return start.serviceTime() + self.timeMatrix[start.custNo, end.custNo] <= \
               end.dueDate + end.serviceLen
    
    def partitionFeasible(self, start, customers) -> ([Customer], [Customer]):
        # a feasible customer is one whose last time is greater than start.time + travel_time
        fs = dict()
        fs[0], fs[1] = [], []

        for c in customers:
            fs[self.feasible(start, c)].append(c)
        
        infeasible, feasible = fs[0], fs[1]
        
        return (feasible, infeasible)

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

