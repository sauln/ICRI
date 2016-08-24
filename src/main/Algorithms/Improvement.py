import pickle
import copy
import sortedcontainers
import numpy as np
import random
import logging, sys

from src.visualization.visualize import Plotter
from src.main.BaseObjects.Parameters import Parameters
from src.main.Algorithms.RollOut import RollOut 
from src.main.BaseObjects.Dispatch import Dispatch

logger = logging.getLogger(__name__)

def geographicSimilarity(dispatch, vehicle):
    distL = lambda x: np.linalg.norm(np.asarray(vehicle.geographicCenter()) \
                                   - np.asarray(x.geographicCenter()))
    dist = sortedcontainers.SortedListWithKey(key = distL)
    dist.update(dispatch.vehicles)

    return dist

def rankByVehiclesAndTotalDistance(vehicleSet):
    return (len(vehicleSet), sum(v.totalDist for v in vehicleSet))

def rankByNumCustomersAndDist(vehicle):
    return (len(vehicle.customerHistory), vehicle.totalDist)

def vehicleSetPrint(vehicleSet):
    return "\n".join(str(v) for v in vehicleSet)

class Improvement:
    def __init__(self):
        self.previousCandidates = []

    def run(self, dispatch):
        dispatchBackup = copy.deepcopy(dispatch) # keep for comparison purposes

        iterations = 100
        for i in range(iterations):
            if(not i%10):
                logger.info("Improvement phase {}/{}".format(i, iterations))
            self.improve(dispatch)

        self.summarizeSolution(dispatch, dispatchBackup)

        return dispatch

    def summarizeSolution(self, dispatch, dispatchBackup):
        logger.info("Before improvement: {}".format(dispatchBackup.solutionStr()))
        logger.info("After improvement: {}".format(dispatch.solutionStr()))

        Plotter().beforeAndAfter(dispatchBackup, dispatch).show() 

    def improve(self, dispatch):
        simVehicles = self.candidateVehicles(dispatch)

        tmpDispatch = self.setupNextRound(simVehicles)
        solution = RollOut().run(tmpDispatch)
      
        if(self.shouldReplaceWith(simVehicles, solution.vehicles)):
            self.replaceRoutes(dispatch, simVehicles, solution.vehicles) 
        else:
            logger.debug("Wont replace because {} is worse than {}".format( \
                rankByVehiclesAndTotalDistance(solution.vehicles),\
                rankByVehiclesAndTotalDistance(simVehicles)))

            #Plotter().compareRouteSets(solution.vehicles, simVehicles).show()


    def shouldReplaceWith(self, oldVehicles, newVehicles):
        #set(oldVehicles) != set(newVehicles) and \
        #            self.bestOf(newVehicles, oldVehicles) == newVehicles
        return len(newVehicles) <= len(oldVehicles)
        #return 1

    def candidateVehicles(self, dispatch):
        worst = self.worstVehicle(dispatch)
        logger.debug("Improve around {}".format(worst))
        candidateVehicles = self.choseCandidates(dispatch, worst)
        return candidateVehicles
    
    def choseCandidates(self, dispatch, worst):
        criterion = geographicSimilarity
        return criterion(dispatch, worst)[:5]

    def worstVehicle(self, solution):
        criterion = rankByNumCustomersAndDist 
        sortedRoutes = sortedcontainers.SortedListWithKey(key = criterion)
        sortedRoutes.update(solution.vehicles)
        
        rbest = sortedRoutes.pop(0)
        if(rbest in self.previousCandidates):
            rbest = random.choice(sortedRoutes)
        
        self.previousCandidates.append(rbest)
        return rbest 

    def setupNextRound(self, simRoutes):
        customers = self.flattenRoutes(simRoutes)
        customers.remove(Parameters().depot) 
        dispatch = Dispatch(customers, Parameters().depot)
        return dispatch

    def flattenRoutes(self, vehicles):
        return list({c for vehicle in vehicles for c in vehicle.customerHistory})

    def replaceRoutes(self, dispatch, oldVehicles, newVehicles):
        logging.debug("Replace routes")
        logging.debug("Are they the same? {}".format(set(oldVehicles) == set(newVehicles)))
        
        for r in oldVehicles:
            dispatch.vehicles.remove(r)
        for r in newVehicles:
            dispatch.vehicles.append(r)

    def bestOf(self, *allVehicleSets):
        if(allVehicleSets[0] == allVehicleSets[1]):
            return 0
        criterion = rankByVehiclesAndTotalDistance 

        rankedVehicleSets = sortedcontainers.SortedListWithKey(key = criterion)
        rankedVehicleSets.update(allVehicleSets)

        
        return rankedVehicleSets[0] 

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    with open("data/interim/SolutionR101.p", "rb") as f:
        routes = pickle.load(f)
    with open("data/interim/r101.p", "rb") as f:
        sp = pickle.load(f)

    parameters = Parameters()
    parameters.build(sp, 10, 20)
    
    newRoutes = Improvement().run(routes)
    # Plotter().beforeAndAfter(routes, newRoutes).show()


