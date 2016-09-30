import numpy as np

class Cost:
    @staticmethod
    def vehicleToCustomer(vehicle, end):
        return vehicle.travelTime(end)
    
    @staticmethod
    def distanceOnly(vehicle, end):
        return vehicle.travelDist(end)

    def totalDistance(solution):
        return sum([v.totalDist for v in solution.vehicles]) 

    @staticmethod
    def ofSolution(solution):
        return Cost.of_vehicles(solution.vehicles)

    @staticmethod
    def of_vehicles(vehicles):
        return (len(vehicles), sum([v.totalDist for v in vehicles]))

    @staticmethod
    def ofRoutes(routes):
        return len(routes) 

    @staticmethod
    def gnnh(delta, vehicle, end): #s:start, e:end customers
        # Infeasible nodes would be filtered before here -
        nextArrivalTime = vehicle.totalTime + vehicle.travelTime(end)
        earliestService = max(nextArrivalTime, end.readyTime)

        c = np.zeros(len(delta))
        isDepot     = (vehicle.last().custNo == 0)
        travelDist  = vehicle.travelDist(end)
        remaining   = earliestService - vehicle.totalTime
        timeSlack   = end.dueDate - (vehicle.totalTime + vehicle.travelTime(end))
        capSlack    = (vehicle.maxCapacity - vehicle.curCapacity) - end.demand # slack
        c[0], c[1], c[2], c[3], c[4] = isDepot, travelDist, remaining, timeSlack, capSlack
        
        cost = np.dot(delta, c)    
        return cost

