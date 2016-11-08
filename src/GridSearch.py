import pickle
import logging
import csv
from pyDOE import *
from abc import ABCMeta, abstractmethod
import numpy as np
import time
from multiprocessing import Pool, Value
from functools import partial
import sys


from .baseobjects import Dispatch, Parameters, Solution, Utils
from .baseobjects import Cost, Validator, Heuristic
from .RollOut import RollOut

from db import add_data

LOGGER = logging.getLogger(__name__)

class Tuning:
    __metaclass__ = ABCMeta

    @abstractmethod
    def generator(self, count): pass

    def run_algo(self, lam, algo, dispatch, count, trunc, depth, width, params=None):
        Utils.increment()
        c = Utils.value()
        print("Start search for {} using {}".format(algo, params.problem))
        
        sys.stdout.flush()
        dispatch.set_delta(lam)
        solution = algo().run(dispatch, depth, width) 
        num_veh, t_dist = Cost.of_vehicles(solution.vehicles)
        res = Solution(num_veh, t_dist, lam, solution)  
        # Validator(solution, filename).validate()
       

        add_data.save_result_to_db(params, res)


        print("{}/{}: ({}, {}) grid search on {}".format(\
            c, count, num_veh, t_dist, lam))
        sys.stdout.flush()
        return res

    def find_costs(self, algo, dispatch, \
                         count=5, trunc=0, depth=10, width=10, params=None):
        results = []
        counter = Value('i', 0)
        Utils.init(counter)        
       
        algo_partial = partial(self.run_algo, algo=algo, 
                                  dispatch=dispatch, 
                                  count=count,  trunc=trunc, 
                                  depth=depth,  width=width, params=params)
        lambdas = self.generator(count)
        results = [algo_partial(lam) for lam in lambdas]
        return results

class RandomSearch(Tuning):
    def generator(self, count):
        # np.random.seed(0)
        lambdas = np.random.random_sample((count, 5))
        return lambdas

class GridSearch(Tuning):
    def generator(self, count):
        width = 5
        lambdas = lhs(width, samples=count, criterion='cm')
        return lambdas

class ShadowSearch(Tuning):
    def generator(self, count):
        num_vars = 5

        for pos in range(num_vars):
            lambdas = np.ones((count, num_vars))
            lambdas[:,pos] = np.linspace(0, 1, num=count)
            yield lambdas

class Search(RandomSearch):
    pass

#switch_search = {   "grid_search":Grid_search, \
#                  "shadow_search":Shadow_search, \
#                  "random_search":Random_search}

def search(algo_type, filename, trunc=0, \
           count=5, \
           width=10, depth=10, params=None):
    
    sp = Utils.open_sp(filename)
    Parameters().build(sp)
    
    num_customers = 5 if trunc else len(sp.customers)
    dispatch = Dispatch(sp.customers[:num_customers+1])
    
    costs = Search().find_costs(\
        algo_type, dispatch, trunc=trunc, count=count, depth=depth, width=width, params=params)
    
    crit = lambda x: (x.num_vehicles, x.total_distance)
    bestFound = min(costs, key=crit)
    print("Found best {}".format(bestFound))

    return bestFound, costs

def search_improvement(algo_type, dispatch, trunc=0, \
                       count=5, \
                       width=10, depth=10):

    costs = Search().find_costs(\
        algo_type, dispatch, trunc=trunc, count=count, depth=depth, width=width)
    
    crit = lambda x: (x.num_vehicles, x.total_distance)
    bestFound = min(costs, key=crit)
    LOGGER.debug("Found best {}".format(bestFound))

    return bestFound, costs

if __name__ == "__main__":
    best = run_search("r101.p")
    print("Best solution: {}".format(best))
