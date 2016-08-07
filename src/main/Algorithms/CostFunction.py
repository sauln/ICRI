import numpy as np

class Cost:
    @staticmethod
    def vehicleToCustomer(vehicle, end):
        return vehicle.travelTime(end)
    
    @staticmethod
    def distanceOnly(vehicle, end):
        return vehicle.travelDist(end)
    
    @staticmethod
    def ofRoutes(routes):
        return len(routes)*10 

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

