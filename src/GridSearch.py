import pickle
import logging
import csv
from pyDOE import *
from abc import ABCMeta, abstractmethod
import numpy as np

from .baseobjects import Dispatch, Parameters, Solution, Plotter, Utils, Cost
from .RollOut import RollOut

LOGGER = logging.getLogger(__name__)

class Tuning:
    __metaclass__ = ABCMeta

    @abstractmethod
    def generator(self, count): pass

    def make_dispatch(self, sp, trunc=0):
        if trunc:
            num_customers = 5 
        else:
            num_customers = len(sp.customers)
        
        dispatch = Dispatch(sp.customers[:num_customers+2])
        
        return dispatch 

    def find_costs(self, dispatch, count=5, trunc=0, fname=None):
        if type(dispatch) is not Dispatch:
            dispatch = self.make_dispatch(dispatch, trunc)

        num_diff_lambdas = count
        
        results = []
        for lambdas in self.generator(num_diff_lambdas): 
            for lam in lambdas:
                dispatch.set_delta(lam)
                solution = RollOut().run(dispatch)
                num_veh, t_dist = Cost.of_vehicles(solution.vehicles)
                res = Solution(num_veh, t_dist, lam, solution, fname)  
                results.append(res)

        return results

class Random_search(Tuning):
    def generator(self, count):
        np.random.seed(0)
        lambdas = np.random.random_sample((count, 5))
        return [lambdas]

class Grid_search(Tuning):
    def generator(self, count):
        width = 5
        lambdas = lhs(width, samples=count, criterion='cm')
        return [lambdas]

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
   
def search(dispatch, trunc=0, count=5, fname=None, search_type="random_search"):
    costs = switch[search_type]().find_costs(\
        dispatch, trunc=trunc, fname=fname, count=count)
    crit = lambda x: (x.num_vehicles, x.total_distance)
    bestFound = min(costs, key=crit)
    return bestFound, costs

def run_search(fname, search_type="random_search", save=0, trunc=0, count=5):
    sp = Utils.open_sp(fname)
    Parameters().build(sp, 10, 10)

    bestFound, costs = search(sp, fname=fname, trunc=trunc, count=count)
    if(save):
        self.save_as_csv(costs, search_type+"_"+ fname.replace(".p","") + ".csv")
    
    LOGGER.info("Found best for {}: {}".format(fname, bestFound))
    return bestFound 

if __name__ == "__main__":
    best = run_search("r101.p")
    print("Best solution: {}".format(best))

    #grid_search_costs = Grid_search().find_costs(sp)
    #random_costs = Random_search().find_costs(sp)
    #random_costs = find_random_costs(sp)
    # save_as_csv(random_costs, "data/processed/random_costs.csv")
    #gs_costs = find_gs_costs(sp)
    #save_as_csv(gs_costs, "data/processed/gs_costs.csv")
    #shadow_costs = find_shadow_costs(sp)
    #shadow_plot(shadow_costs)
    #end = time.gmtime()
    #print("Ending at {}".format(end))

