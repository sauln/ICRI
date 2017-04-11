import pickle
import random
import logging
import csv
# from pyDOE import *
# import pyDOE
from abc import ABCMeta, abstractmethod
import numpy as np
import time
from multiprocessing import Pool, Value
from functools import partial
import sys

sys.path.append('.')


from .baseobjects import Dispatch, Parameters, Solution, Utils, Params
from .baseobjects import Cost, Validator, Heuristic
from .RollOut import RollOut

from db import add_data

LOGGER = logging.getLogger(__name__)

class Tuning:
    __metaclass__ = ABCMeta

    @abstractmethod
    def generator(self, count): pass

    def run_algo(self, lam, dispatch, algo, params):
        print("Start search for {} using {}".format(params.run_type,
                                                    params.problem))
        sys.stdout.flush()

        dispatch.set_delta(lam)
        solution = algo().run(dispatch, params.depth, params.width)
        num_veh, t_dist = Cost.of_vehicles(solution.vehicles)
        res = Solution(num_veh, t_dist, lam, solution)
        add_data.save_result_to_db(params, res)

        print("n/{}: ({}, {}) grid search on {}".format(\
            params.count, num_veh, t_dist, lam))
        sys.stdout.flush()

        return res

    def find_costs(self, dispatch, algo, params):
        algo_partial = partial(self.run_algo,
                               dispatch=dispatch,
                               algo=algo,
                               params=params)
        lambdas = self.generator(params.count)
        results = [algo_partial(lam) for lam in lambdas]
        return results

class RandomSearch(Tuning):
    def generator(self, count):
        # np.random.seed(0)
        lambdas = np.random.random_sample((count, 5))
        return lambdas

# pyDOE needs scipy
# class GridSearch(Tuning):
#     def generator(self, count):
#         width = 5
#         lambdas = pyDOE.lhs(width, samples=count, criterion='cm')
#         return lambdas

class ShadowSearch(Tuning):
    def generator(self, count):
        num_vars = 5

        for pos in range(num_vars):
            lambdas = np.ones((count, num_vars))
            lambdas[:,pos] = np.linspace(0, 1, num=count)
            yield lambdas


# switch to decide which to expose
class Search(RandomSearch):
    pass

def search_core(dispatch, algo_type, search_params):
    costs = Search().find_costs(dispatch, algo_type, search_params)

    crit = lambda x: (x.num_vehicles, x.total_distance)
    bestFound = min(costs, key=crit)
    LOGGER.debug("Found best {}".format(bestFound))
    return bestFound, costs

def search(algo_type, search_params):
    sp = Utils.open_sp(search_params.problem+".p")
    Parameters().build(sp)
    dispatch = Dispatch(sp.customers)

    return search_core(dispatch, algo_type, search_params)

def search_improvement(dispatch, algo_type, search_params):
    return search_core(dispatch, algo_type, search_params)

def run_search(filename):
    print("Run {}".format(filename))
    random.seed(999)
    problem_name=filename.replace(".p", "")
    params = Params(3,3,3, RollOut.__name__.lower(),
                           "search", problem_name)

    best_solution, all_solutions = search(RollOut, params)
    return all_solutions, filename

if __name__ == "__main__":
    best = run_search("r101.p")
    print("Best solution: {}".format(best))
