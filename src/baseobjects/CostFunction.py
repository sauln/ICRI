import numpy as np
from .Parameters import Parameters

class Cost:
    @staticmethod
    def of_vehicles(vehicles):
        return (len(vehicles), sum([v.total_dist for v in vehicles]))

    @staticmethod
    def euclidean_cust(c1, c2):
        # this function is way too much of computation time.
        # precompute for the entire customer set
        dist = lambda c1, c2: np.sqrt((c1.x - c2.x)**2 + (c1.y - c2.y)**2)
        return dist(c1,c2)

    @staticmethod
    def gnnh(delta, vehicle, customer): #s:start, e:customer customers
        # vehicle.travel_time, vehicle.travel_dist, 
        nextArrivalTime = vehicle.total_time + vehicle.travel_time(customer)
        earliestService = max(nextArrivalTime, customer.readyTime)

        isDepot = (vehicle.last().custNo == 0)
        travel_dist = vehicle.travel_dist(customer)
        remaining = earliestService - vehicle.total_time
        timeSlack = customer.dueDate - (vehicle.total_time + vehicle.travel_time(customer))
        capSlack = vehicle.remaining_slack() - customer.demand # slack
        c = np.array( [isDepot, travel_dist, remaining, timeSlack, capSlack] )
        cost = np.dot(delta, c)
        return cost

