
class Route():
    service_time_min = 0
    service_time_max = 0
    def __init__(self):
        pass

class Vehicle():
    capacity_max = 0
    capacity_curr = 0
    def __init__(self):
        pass

class Service():
    customer = 0
    arrival_time = 0
    departure_time = 0
    service_time = 0    
    
    def __init__(self):
        pass

    def find_service_time(self, arrival_time):
        service_time = max(self.arrival_time, self.service_time[0])


## these will be matrices - indexed by customer ids
def distance(cid1, cid2):
    return 0
def travel_time(cid1, cid2):
    return 0

def g(c_from, c_to, vehicle):
    next_arrival_time = c_from.service_time + c_from.service_len + travel_time(c_from, c_to)
    earliest_possible_service = max(next_arrival_time, c_to.service_window[0])
    prev_departure = c_from.service_time + c_from.service_len

    d0 = 1 if (not c_from.depot) else 0
    d1 = distance(c_from.cid, c_to.cid)
    d2 = earliest_possible_service - prev_departure
    d3 = c_to.service_window[1] - (prev_departure + travel_time(c_from, c_to))
    d4 = vehicle.capacity_curr - c_to.demand
    d5 = max(0, c_from.service_window[0] - earliest_possible_service)
    d6 = max(0, c_from_service_time - c_from.service_window[1])
    return (d0, d1, d2, d3, d4, d5, d6)

def vehicleRoutingAlgorithm():
    pass

def main():
    #need distance matrix between all customers
    vehicle_max = 0
    vehicle_cost = 0 

    c1 = Customer()
    c2 = Customer()
    v  = Vehicle()

    Delta = (1,)*6

    print("Define classes")
    print("Do TDD?!")
    weights = g(c1,c2, v)
    gdij    = sum(a*b for (a,b) in zip(weights,Delta))
    print(weights)
    print(gdij)

if __name__ == "main":
    main()


