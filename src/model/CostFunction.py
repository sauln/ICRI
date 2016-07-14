import sortedcontainers
import src.model.Matrices as mat
from src.model.SolomonProblem import Customer
from src.model.Route import Edge


class CostFunction():
    def __init__(self, customers):
        m = mat.Matrices(customers)
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
    
    # need to take a list of routes and return [(route, next)]
    def bestNodes(self, delta, routes, customers, depot, width):
        cs = []
        
        print(routes)

        for r in routes:
            print("Last node: {}".format(r[-1]))
            print("number of custs: {}".format(len(customers)))
            feasible, _ = self.partitionFeasible(r[-1], customers)
            print(len(feasible))
            for c in feasible:
                cs.append((r, c, self.g(delta, r[-1], c)))

        return cs[:width]


    def w(self, delta, custStart, customers, depot, lim) -> [Edge]:
        feasible, infeasible = self.partitionFeasible(custStart, customers)

        #implements fast insertion sort, sorting on last element in key
        cs = sortedcontainers.SortedListWithKey(key=lambda x: x.cost)

        for c in feasible:
            cs.add( (custStart, c, self.g(delta, custStart, c)) )
        for c in infeasible:
            cs.add( (custStart, depot, c, self.g(delta, depot, c)) )

        #ns = [(self.g(delta, custStart, c), c) for c in customers] 
        #return sorted(ns, key=lambda c: c[0])[:lim] 
        return cs[:lim] 


    def g(self, delta: [float], custStart: Customer, custEnd: Customer) -> float:
        # Infeasible nodes would be filtered before here - 
        if(custStart == custEnd):
            return 0

        return delta[0] * 5 * (custStart.custNo == 0) +\
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

