import pickle
import logging
import csv
from pyDOE import *
from abc import ABCMeta, abstractmethod
import numpy as np
import time
from multiprocessing import Pool, Value
from functools import partial


from .baseobjects import Dispatch, Parameters, Solution, Plotter, Utils, Cost
from .RollOut import RollOut

LOGGER = logging.getLogger(__name__)

class Tuning:
    __metaclass__ = ABCMeta

    @abstractmethod
    def generator(self, count): pass

    def rollout(self, lam, dispatch, count, trunc, depth, width):
        Utils.increment()
        c = Utils.value()
        LOGGER.info("{}/{} run grid search on {}".format(c, count, lam))
        start = time.time()
        dispatch.set_delta(lam)
        solution = RollOut().run(dispatch, depth, width)
        num_veh, t_dist = Cost.of_vehicles(solution.vehicles)
        res = Solution(num_veh, t_dist, lam, solution)  
        end = time.time()
        LOGGER.info("{}/{}: ({}, {}) grid search took {} seconds".format(\
            c, count, num_veh, t_dist,  end-start))
        return res

    def find_costs(self, dispatch, count=5, trunc=0, depth=10, width=10):
        results = []
        lambdas = self.generator(count)
        
        rollout_partial = partial(self.rollout, 
                                  dispatch=dispatch, 
                                  count=count, trunc=trunc, 
                                  depth=depth, width=width)
      
        counter = Value('i', 0)
        
        #pool = Pool(initializer=Utils.init, initargs=(counter,))
        # results = pool.map(rollout_partial, lambdas)

        Utils.init(counter)        
        results = [rollout_partial(lam) for lam in lambdas]

        return results

class Random_search(Tuning):
    def generator(self, count):
        np.random.seed(0)
        lambdas = np.random.random_sample((count, 5))
        return lambdas

class Grid_search(Tuning):
    def generator(self, count):
        width = 5
        lambdas = lhs(width, samples=count, criterion='cm')
        return lambdas

class Shadow_search(Tuning):
    def generator(self, count):
        num_vars = 5

        for pos in range(num_vars):
            lambdas = np.ones((count, num_vars))
            lambdas[:,pos] = np.linspace(0, 1, num=count)
            yield lambdas

switch = {"grid_search": Grid_search, \
          "shadow_search":Shadow_search, \
          "random_search":Random_search}

def make_dispatch(sp, trunc=0):
    num_customers = 5 if trunc else len(sp.customers)

    dispatch = Dispatch(sp.customers[:num_customers+2])
    return dispatch 
   
def search(feed, trunc=0, count=5, search_type="random_search", width=10, depth=10):
    if type(feed) is str:
        fname = feed
        sp = Utils.open_sp(fname)
        Parameters().build(sp)
        dispatch = make_dispatch(sp, trunc)
    else:
        dispatch = feed

    costs = switch[search_type]().find_costs(\
        dispatch, trunc=trunc, count=count, depth=depth, width=width)
    
    crit = lambda x: (x.num_vehicles, x.total_distance)
    bestFound = min(costs, key=crit)
    LOGGER.debug("Found best {}".format(bestFound))

    return bestFound

if __name__ == "__main__":
    best = run_search("r101.p")
    print("Best solution: {}".format(best))
