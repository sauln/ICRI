import numpy as np

class Cost:
    @staticmethod
    def of_vehicles(vehicles):
        return (len(vehicles), sum([v.totalDist for v in vehicles]))

    @staticmethod
    def gnnh(delta, vehicle, end): #s:start, e:end customers
        # Infeasible nodes would be filtered before here -
        nextArrivalTime = vehicle.totalTime + vehicle.travelTime(end)
        earliestService = max(nextArrivalTime, end.readyTime)

        isDepot     = (vehicle.last().custNo == 0)
        travelDist  = vehicle.travelDist(end)
        remaining   = earliestService - vehicle.totalTime
        timeSlack   = end.dueDate - (vehicle.totalTime + vehicle.travelTime(end))
        capSlack    = (vehicle.maxCapacity - vehicle.curCapacity) - end.demand # slack
        c = np.array( [isDepot, travelDist, remaining, timeSlack, capSlack] )
        
        cost = np.dot(delta, c)    
        return cost

