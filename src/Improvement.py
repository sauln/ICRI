#!/usr/bin/python3
""" Improvement algorithm complete routing solution.  """

import random
import pickle
import logging
import sys
import copy

import sortedcontainers
import numpy as np
from math import ceil

from .baseobjects import Parameters, Dispatch, Plotter, Cost
from .RollOut import RollOut
from .GridSearch import search

LOGGER = logging.getLogger(__name__)


def geographic_similarity(dispatch, vehicle):
    """ Ranks vehicles in dispatch by geographic similarity to input vehicle """
    dist_f = lambda x: np.linalg.norm(np.asarray(vehicle.geographicCenter()) \
                                   - np.asarray(x.geographicCenter()))
    dist = sortedcontainers.SortedListWithKey(key=dist_f)
    dist.update(dispatch.vehicles)

    return dist

def by_customers_dist(vehicle):
    """ Determines how vehicles should be compared """
    return (len(vehicle.customerHistory), vehicle.totalDist)

def summarize_solution(dispatch, dispatch_backup):
    new_num_veh, new_dist = Cost.of_vehicles(dispatch.vehicles)
    old_num_veh, old_dist = Cost.of_vehicles(dispatch_backup.vehicles)
    LOGGER.info("Before Improvement: {}: {}"\
        .format(old_num_veh, old_dist))
    LOGGER.info("After Improvement: {}: {}"\
        .format(new_num_veh, new_dist))
    LOGGER.info("Improvement: {} vehicles, {} distance".format(\
        old_num_veh - new_num_veh,\
        old_dist - new_dist))


class Improvement:
    """ Encapslates the improvement algorithm """
    def __init__(self):
        """ Setup very simple memoization"""
        self.previous_candidates = []

    def replace_vehicles(self, dispatch, old_vehicles, new_vehicles):
        """ Replace the old vehicles in a dispatch object with new vehicles """
        LOGGER.debug("Replace routes")
        LOGGER.debug("Are they the same? {}".format(\
            set(old_vehicles) == set(new_vehicles)))

        for v in old_vehicles:
            dispatch.vehicles.remove(v)
        for v in new_vehicles:
            dispatch.vehicles.append(v)
    
    def should_replace_with(self, old_vehicles, new_vehicles):
        """ Criterion for replacing vehicle sets for improvement """
        less_vehs = len(new_vehicles) < len(old_vehicles)  
        new_num, new_dist = Cost.of_vehicles(new_vehicles)
        old_num, old_dist = Cost.of_vehicles(old_vehicles)

        LOGGER.debug("New solution: {}".format((new_num, new_dist)))
        LOGGER.debug("Original solution: {}".format((old_num, old_dist)))
        if less_vehs: 
            return less_vehs
        else:
            if new_num > old_num:
                return 0
            else:
                return new_dist < old_dist
        #return 1

    def run(self, dispatch):
        """ Master function for this class - initiates optimization """
        dispatch_backup = copy.deepcopy(dispatch) # keep for comparison purposes

        iterations = 5
        for i in range(iterations):
            if not i%5: LOGGER.debug("Improvement phase {}/{}".format(i, iterations))
            self.improve(dispatch)

        summarize_solution(dispatch, dispatch_backup)

        return dispatch

    def chose_candidates(self, dispatch, worst, count=5):
        """ method for choosing the vehicles for improvement"""
        criterion = geographic_similarity
        all_cands =  criterion(dispatch, worst)
        return all_cands[: ceil(len(all_cands)/3)]


    def improve(self, dispatch):
        """ Workhorse of Improvement. Manages the improve phase"""
        tmp_dispatch, old_vehicles = self.setup_next_round(dispatch)
        #import pdb
        #pdb.set_trace()
        #solution = RollOut().run(tmp_dispatch)
        #solution = run_search(f, trunc=0, count=10)
        solution, costs = search(tmp_dispatch, count=20)

        if self.should_replace_with(old_vehicles, solution.solution.vehicles):
            self.replace_vehicles(dispatch, old_vehicles, solution.solution.vehicles)
        else:
            LOGGER.debug("Wont replace because {} is worse than {}".format( \
                Cost.of_vehicles(solution.solution.vehicles),\
                Cost.of_vehicles(old_vehicles)))

            #Plotter().compareRouteSets(solution.vehicles, similar_vehicles).show()

    def candidate_vehicles(self, dispatch):
        """ Find next vehicles to improve """
        worst = self.worst_vehicle(dispatch)
        candidate_vehicles = self.chose_candidates(dispatch, worst)
        LOGGER.debug("Improvement candidates around {}: {} vehicles with distance {}"\
            .format(worst, *Cost.of_vehicles(candidate_vehicles)))
        return candidate_vehicles

    def worst_vehicle(self, solution):
        """ Find worst vehicle to improve around """
        criterion = by_customers_dist
        sorted_vehicles = sortedcontainers.SortedListWithKey(key=criterion)
        sorted_vehicles.update(solution.vehicles)

        
        rbest = sorted_vehicles.pop(0)
        if(len(sorted_vehicles)):
            rbestR = random.choice(sorted_vehicles)
            rbest = random.choice([rbest, rbestR])

        self.previous_candidates.append(rbest)
        return rbest

    def setup_next_round(self, dispatch):
        """ With the candidate vehicles, setup the rollout algorithm """
        similar_vehicles = self.candidate_vehicles(dispatch)
        customers = self.flatten_vehicles(similar_vehicles)
        new_dispatch = Dispatch(customers)
        new_dispatch.set_delta(dispatch.delta)
        return new_dispatch, similar_vehicles

    def flatten_vehicles(self, vehicles):
        """ Get all customers from many vehicles """
        return list({c for v in vehicles for c in v.customerHistory})




if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    with open("data/interim/SolutionR101.p", "rb") as f:
        routes = pickle.load(f)
    with open("data/interim/r101.p", "rb") as f:
        sp = pickle.load(f)

    parameters = Parameters()
    parameters.build(sp, 10, 20)

    newRoutes = Improvement().run(routes)
    # Plotter().beforeAndAfter(routes, newRoutes).show()
