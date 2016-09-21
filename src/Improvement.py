#!/usr/bin/python3
""" Improvement algorithm complete routing solution.  """

import random
import pickle
import logging
import sys
import copy

import sortedcontainers
import numpy as np

from .baseobjects import Parameters, Dispatch, Plotter
from .RollOut import RollOut

LOGGER = logging.getLogger(__name__)

def geographic_similarity(dispatch, vehicle):
    """ Ranks vehicles in dispatch by geographic similarity to input vehicle """
    dist_f = lambda x: np.linalg.norm(np.asarray(vehicle.geographicCenter()) \
                                   - np.asarray(x.geographicCenter()))
    dist = sortedcontainers.SortedListWithKey(key=dist_f)
    dist.update(dispatch.vehicles)

    return dist

def by_vehicles_dist(vehicles):
    """ Determines how a set of vehicles should be compared """
    return (len(vehicles), sum(v.totalDist for v in vehicles))

def by_customers_dist(vehicle):
    """ Determines how vehicles should be compared """
    return (len(vehicle.customerHistory), vehicle.totalDist)

def vehicle_set_print(vehicles):
    """ Nice print function for a vehicle set """
    return "\n".join(str(v) for v in vehicles)

def should_replace_with(old_dispatch, new_dispatch):
    """ Criterion for replacing vehicle sets for improvement """
    less_vehs = len(new_dispatch.vehicles) < len(old_dispatch.vehicles)  
    if less_vehs: 
        return less_vehs
    else:
        if len(new_dispatch.vehicles) > len(old_dispatch.vehicles):
            return 0
        else:
            return new_dispatch.total_dist < old_dispatch.total_dist
    #return 1

def summarize_solution(dispatch, dispatch_backup):
    """ Helper function for printing output"""
    old_total_distance = sum(v.totalDist for v in dispatch_backup.vehicles)
    total_distance = sum(v.totalDist for v in dispatch.vehicles)
    LOGGER.debug("Before Improvement: {}: {}"\
        .format(len(dispatch_backup.vehicles), old_total_distance))

    LOGGER.debug("After Improvement: {}: {}"\
        .format(len(dispatch.vehicles), total_distance))
    #Plotter().beforeAndAfter(dispatch_backup, dispatch).show()

def chose_candidates(dispatch, worst):
    """ method for choosing the vehicles for improvement"""
    criterion = geographic_similarity
    return criterion(dispatch, worst)[:5]

def flatten_vehicles(vehicles):
    """ Get all customers from many vehicles """
    return list({c for v in vehicles for c in v.customerHistory})

def replace_vehicles(dispatch, old_vehicles, new_vehicles):
    """ Replace the old vehicles in a dispatch object with new vehicles """
    LOGGER.debug("Replace routes")
    LOGGER.debug("Are they the same? {}".format(\
        set(old_vehicles) == set(new_vehicles)))

    for v in old_vehicles:
        dispatch.vehicles.remove(v)
    for v in new_vehicles:
        dispatch.vehicles.append(v)


class Improvement:
    """ Encapslates the improvement algorithm """
    def __init__(self):
        """ Setup very simple memoization"""
        self.previous_candidates = []

    def run(self, dispatch):
        """ Master function for this class - initiates optimization """
        dispatch_backup = copy.deepcopy(dispatch) # keep for comparison purposes

        iterations = 10
        for i in range(iterations):
            if not i%5:
                LOGGER.info("Improvement phase {}/{}".format(i, iterations))
            self.improve(dispatch)

        summarize_solution(dispatch, dispatch_backup)

        return dispatch

    def improve(self, dispatch):
        """ Workhorse of Improvement. Manages the improve phase"""
        tmp_dispatch = self.setup_next_round(dispatch)
        solution = RollOut().run(tmp_dispatch)

        if should_replace_with(tmp_dispatch, solution):
            replace_vehicles(dispatch, tmp_dispatch.vehicles, solution.vehicles)
        else:
            LOGGER.debug("Wont replace because {} is worse than {}".format( \
                by_vehicles_dist(solution.vehicles),\
                by_vehicles_dist(dispatch.vehicles)))

            #Plotter().compareRouteSets(solution.vehicles, similar_vehicles).show()

    def candidate_vehicles(self, dispatch):
        """ Find next vehicles to improve """
        worst = self.worst_vehicle(dispatch)
        LOGGER.debug("Improve around {}".format(worst))
        candidate_vehicles = chose_candidates(dispatch, worst)
        return candidate_vehicles

    def worst_vehicle(self, solution):
        """ Find worst vehicle to improve around """
        criterion = by_customers_dist
        sorted_vehicles = sortedcontainers.SortedListWithKey(key=criterion)
        sorted_vehicles.update(solution.vehicles)

        rbest = sorted_vehicles.pop(0)
        if rbest in self.previous_candidates and sorted_vehicles:
            rbest = random.choice(sorted_vehicles)

        self.previous_candidates.append(rbest)
        return rbest

    def setup_next_round(self, dispatch):
        """ With the candidate vehicles, setup the rollout algorithm """
        similar_vehicles = self.candidate_vehicles(dispatch)
        customers = flatten_vehicles(similar_vehicles)
        new_dispatch = Dispatch(customers)
        new_dispatch.set_delta(dispatch.delta)
        return new_dispatch


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
