import pickle
import logging
import csv
from pyDOE import *
from abc import ABCMeta, abstractmethod
import numpy as np

from .baseobjects import Dispatch, Parameters, Solution, Plotter
from .RollOut import RollOut

LOGGER = logging.getLogger(__name__)


''' These 3 functions can be used elsewhere '''
def open_sp(fname, root = "data/interim/"):
    input_filepath = root + fname
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)
    return sp

def save_sp(fname, root="data/solution/"):
    output_filepath = root + fname 
    with open(output_filepath, "wb") as f:
        pickle.dump(solution, f)

def save_as_csv(costs, filename, root="data/processed/"):
    print("Saving grid search results as {}".format(root+filename))
    with open(root + filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Num Vehicles", "Distance"] + ["lam"]*5)
        for row in costs:
            writer.writerow([row.num_vehicles, row.total_distance] + list(row.params))

class Tuning:
    __metaclass__ = ABCMeta

    @abstractmethod
    def generator(self, count): pass

    def find_costs_from_sp(self, sp, count=5, trunc=0, fname=None):
        if trunc:
            num_customers = 5 
        else:
            num_customers = len(sp.customers)
        
        dispatch = Dispatch(sp.customers[:num_customers+2])
        
        return self.find_costs(dispatch, count=count, trunc=trunc, fname=fname) 

    def find_costs(self, dispatch, count=5, trunc=0, fname=None):
        num_diff_lambdas = count
        
        results = []
        for lambdas in self.generator(num_diff_lambdas): 
            for lam in lambdas:
                dispatch.set_delta(lam)
                solution = RollOut().run(dispatch)
                num_veh, t_dist = self.evaluate(solution)
                res = Solution(num_veh, t_dist, lam, solution, fname)  
                results.append(res)

        return results

    def evaluate(self, solution):
        num_vehicles = len(solution.vehicles)
        total_distance = sum(v.totalDist for v in solution.vehicles)
        return [num_vehicles, total_distance]

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
    costs = switch[search_type]().find_costs(dispatch, trunc=trunc, fname=fname, count=count)
    crit = lambda x: (x.num_vehicles, x.total_distance)
    bestFound = min(costs, key=crit)
    return bestFound, costs


def run_search(fname, search_type="random_search", save=0, trunc=0, count=5):
    sp = open_sp(fname)
    Parameters().build(sp, 10, 10)


    costs = switch[search_type]().find_costs_from_sp(sp, trunc=trunc, fname=fname, count=count)
    crit = lambda x: (x.num_vehicles, x.total_distance)
    bestFound = min(costs, key=crit)




    #costs = switch[search_type]().find_costs(sp, trunc=trunc, fname=fname, count=count)
    #crit = lambda x: (x.num_vehicles, x.total_distance)
    #bestFound = min(costs, key=crit)
    if(save):
        save_as_csv(costs, search_type+"_"+ fname.replace(".p","") + ".csv")
    
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

