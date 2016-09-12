import pickle
import logging
import csv

from pyDOE import *

from abc import ABCMeta, abstractmethod


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

from src.visualization.visualize import Plotter
from src.main.BaseObjects.Dispatch import Dispatch
from src.main.BaseObjects.Parameters import Parameters
from src.main.Algorithms.RollOut import RollOut

logger = logging.getLogger(__name__)


def save_as_csv(shadow_costs, filename):
    flattened = np.concatenate(shadow_costs)

    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Num Vehicles", "Distance"] + ["lam"]*5)
        for row in flattened:
            writer.writerow(row)

def shadow_plot(shadow_costs):
    fig = plt.figure()

    print("Plot and save shadow costs")

    for p, var in enumerate(shadow_costs):
        num_vehicles = var[:,0]
        distances = var[:,1]
        lambdas = var[:,p+2]
       
        ax = fig.add_subplot(len(shadow_costs), 2, 2*p)
        ax.scatter(lambdas, distances)
        ax.set_title("Total distance of parameter {}".format(p))
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.0f"))

        ax = fig.add_subplot(len(shadow_costs), 2, 2*p + 1)
        ax.scatter(lambdas, num_vehicles)
        ax.set_title("Total vehicles of parameter {}".format(p))

    plt.savefig("data/processed/shadow_costs.png")
    #    plt.show()

class Tuning:
    __metaclass__ = ABCMeta

    @abstractmethod
    def generator(self, count): pass

    def find_costs(self, sp):
        num_customers = 5 #len(sp.customers)
        num_diff_lambdas = 10

        customers = sp.customers[1:num_customers+1]
        depot = sp.customers[0]
        dispatch = Dispatch(customers, depot)

        shadow_costs = []
        for lambdas in self.generator(num_diff_lambdas): 
            results = []
            for lam in lambdas:
                dispatch.set_delta(lam)
                solution = RollOut().run(dispatch)
                ev = self.evaluate(solution)
                line = np.concatenate((ev, lam))
                print(line)
                results.append(line)
            shadow_costs.append(np.array(results))

        return shadow_costs

    def evaluate(self, solution):
        num_vehicles = len(solution.vehicles)
        total_distance = sum(v.totalDist for v in solution.vehicles)
        
        return [num_vehicles, total_distance]

class Random_search(Tuning):
    def generator(self, count):
        ''' according to Bergstra/Bengio, random search is better than grid search for 
         many dimensions'''
        window = (0, 1)
        seed = 0
        dimensions = 5 

        np.random.seed(seed)
        lambdas = np.random.random_sample((25, 5))
        return [lambdas]

class Grid_search(Tuning):
    def generator(self, count):
        # let count be a proxy metric for density
        # okay to return just 1 list 
        width = 5
        lambdas = lhs(5, samples=100, criterion='cm')
        return [lambdas]

class Shadow_search(Tuning):
    def generator(self, count):
        num_vars = 5

        for pos in range(num_vars):
            #randoms = np.random.uniform(0,1, (count, num_left))
            lambdas = np.ones((count, num_vars))
            lambdas[:,pos] = np.linspace(0, 1, num=count)
            yield lambdas


if __name__ == "__main__":
    input_filepath = "data/interim/r101.p"
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)
    
    Parameters().build(sp, 10, 10)
   
    shadow_costs = Shadow_search().find_costs(sp)
    grid_search_costs = Grid_search().find_costs(sp)
    random_costs = Random_search().find_costs(sp)

    #random_costs = find_random_costs(sp)
    # save_as_csv(random_costs, "data/processed/random_costs.csv")

    #gs_costs = find_gs_costs(sp)
    #save_as_csv(gs_costs, "data/processed/gs_costs.csv")
   

    #shadow_costs = find_shadow_costs(sp)
    #shadow_plot(shadow_costs)
    #save_as_csv(shadow_costs, "data/processed/shadow_costs.csv")
   
    #end = time.gmtime()
    #print("Ending at {}".format(end))

