#!/usr/bin/python3
""" Improvement algorithm complete routing solution.  """

import random
import pickle
import logging
import sys
import copy
import json

import sortedcontainers
import numpy as np
from math import ceil

from .baseobjects import Dispatch, Vehicle, Cost, Solution, Utils
from .RollOut import RollOut
from .GridSearch import search, search_improvement

from db.queries import get_best_solutions
LOGGER = logging.getLogger(__name__)

def geographic_similarity(dispatch, vehicle):
    """ Ranks vehicles in dispatch by geographic similarity to input vehicle """
    dist_f = lambda x: np.linalg.norm(np.asarray(vehicle.geographic_center()) \
                                   - np.asarray(x.geographic_center()))
    dist = sortedcontainers.SortedListWithKey(key=dist_f)
    dist.update(dispatch.vehicles)

    return dist

def by_customers_dist(vehicle):
    """ Determines how vehicles should be compared """
    return (vehicle.served_customers(), vehicle.total_dist)

def log_solution(dispatch, dispatch_backup):
    new_num_veh, new_dist = Cost.of_vehicles(dispatch.vehicles)
    old_num_veh, old_dist = Cost.of_vehicles(dispatch_backup.vehicles)

    LOGGER.debug("Before Improvement: {}: {}"\
        .format(old_num_veh, old_dist))
    LOGGER.debug("After Improvement: {}: {}"\
        .format(new_num_veh, new_dist))
    LOGGER.debug("Improvement: {} vehicles, {} distance".format(\
        old_num_veh - new_num_veh,\
        old_dist - new_dist))

def build_solution_from_str(solution_obj, problem_name):
    ''' build a dispatch out of the string '''
    # load the original problem - organize solution from it
    problem_def = Utils.open_sp(problem_name + ".p")

    vehs = json.loads(solution_obj.values[0])

    cust_dict = dict(zip(map(lambda x: x.custNo, problem_def.customers),
                         problem_def.customers))

    new_dispatch = Dispatch(problem_def.customers,
                            capacity=problem_def.capacity)
    for veh in vehs:
        vehicle = Vehicle(problem_def.customers[0], problem_def.capacity)
        for c in veh[1:]:
            vehicle.serve(cust_dict[c])
        new_dispatch.vehicles.append(vehicle)

    return new_dispatch

class Improvement:
    """ Encapslates the improvement algorithm """
    def __init__(self):
        """ Setup very simple memoization"""
        self.previous_candidates = []

    def run(self, base_solution=None, search_params=None, improv_params=None):
        """ Master function for this class - initiates optimization """
        best_solutions = get_best_solutions()

        if base_solution == None:
            problem = search_params.problem
            found = best_solutions.loc[best_solutions['problem'] == problem]
            base_solution_obj = found['solution_string']
            dispatch = build_solution_from_str(base_solution_obj, problem)

        for i in range(improv_params["iterations"]):
            dispatch = self.improve(dispatch, search_params, improv_params)

        return dispatch

    def improve(self, dispatch, search_params, improv_params):
        """ Workhorse of Improvement. Manages the improve phase"""
        tmp_dispatch, old_vehicles = self.setup_next_round(dispatch)

        if(len(old_vehicles) > 2):
            solution, all_solutions = search_improvement(tmp_dispatch,
                                                         improv_params["algo"],
                                                         search_params)

            if self.should_replace_with(old_vehicles, solution.solution.vehicles):
                dispatch = self.replace_vehicles(dispatch, old_vehicles,
                                                 solution.solution.vehicles)
            else:
                LOGGER.debug("Wont replace because {} is worse than {}".format(
                    Cost.of_vehicles(solution.solution.vehicles),
                    Cost.of_vehicles(old_vehicles)))

        return dispatch

    def replace_vehicles(self, dispatch, old_vehicles, new_vehicles):
        """ Replace the old vehicles in a dispatch object with new vehicles """
        LOGGER.debug("Replace routes")
        LOGGER.debug("Are they the same? {}".format(\
            set(old_vehicles) == set(new_vehicles)))

        for v in old_vehicles:
            dispatch.vehicles.remove(v)
        for v in new_vehicles:
            dispatch.vehicles.append(v)
        return dispatch

    def should_replace_with(self, old_vehicles, new_vehicles):
        """ Criterion for replacing vehicle sets for improvement """
        new_num, new_dist = Cost.of_vehicles(new_vehicles)
        old_num, old_dist = Cost.of_vehicles(old_vehicles)

        LOGGER.debug("New solution: {}".format((new_num, new_dist)))
        LOGGER.debug("Original solution: {}".format((old_num, old_dist)))

        if new_num < old_num:
            replace = 1
        else:
            if new_num > old_num:
                replace = 0
            else:
                replace = new_dist < old_dist

        return replace

    def chose_candidates(self, dispatch, worst, count=5):
        """ method for choosing the vehicles for improvement"""
        criterion = geographic_similarity
        all_cands =  criterion(dispatch, worst)
        return all_cands[: ceil(len(all_cands)/3)]

    def candidate_vehicles(self, dispatch):
        """ Find next vehicles to improve """
        worst = self.worst_vehicle(dispatch)
        candidate_vehicles = self.chose_candidates(dispatch, worst)
        LOGGER.debug("Improvement candidates around {}: {} vehicles with distance {}"\
            .format(worst, *Cost.of_vehicles(candidate_vehicles)))
        return candidate_vehicles

    def worst_vehicle(self, solution):
        """ Find worst vehicle to improve around """
        sorted_vehicles = sortedcontainers.SortedListWithKey(key=by_customers_dist)
        sorted_vehicles.update(solution.vehicles)

        # choose the best one or a random one
        rbest = sorted_vehicles.pop(0)
        if(len(sorted_vehicles)):
            rbestR = random.choice(sorted_vehicles)
            rbest = random.choice([rbest, rbestR])

        return rbest

    def setup_next_round(self, dispatch):
        """ With the candidate vehicles, setup the rollout algorithm """
        similar_vehicles = self.candidate_vehicles(dispatch)
        customers = self.flatten_vehicles(similar_vehicles)
        new_dispatch = Dispatch(customers, capacity=dispatch.capacity)
        new_dispatch.set_delta(dispatch.delta)
        return new_dispatch, similar_vehicles

    def flatten_vehicles(self, vehicles):
        """ Get all customers from many vehicles """
        return list({c for v in vehicles for c in v.customer_history})

