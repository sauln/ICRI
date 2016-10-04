import numpy as np

class Cost:
    @staticmethod
    def of_vehicles(vehicles):
        return (len(vehicles), sum([v.totalDist for v in vehicles]))

    @staticmethod
    def gnnh(delta, vehicle, customer): #s:start, e:customer customers
        # Infeasible nodes would be filtered before here -
        nextArrivalTime = vehicle.totalTime + vehicle.travelTime(customer)
        earliestService = max(nextArrivalTime, customer.readyTime)

        isDepot = (vehicle.last().custNo == 0)
        travelDist = vehicle.travelDist(customer)
        remaining = earliestService - vehicle.totalTime
        timeSlack = customer.dueDate - (vehicle.totalTime + vehicle.travelTime(customer))
        capSlack = (vehicle.maxCapacity - vehicle.curCapacity) - customer.demand # slack
        c = np.array( [isDepot, travelDist, remaining, timeSlack, capSlack] )
        
        cost = np.dot(delta, c)    
        return cost

