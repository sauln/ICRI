import pickle
import logging

import numpy as np
import matplotlib.pyplot as plt

from src.visualization.visualize import Plotter
from src.main.BaseObjects.Dispatch import Dispatch
from src.main.BaseObjects.Parameters import Parameters
from src.main.Algorithms.RollOut import RollOut

logger = logging.getLogger(__name__)

def evaluate(solution):
    num_vehicles = len(solution.vehicles)
    total_distance = sum(v.totalDist for v in solution.vehicles)
    
    return [num_vehicles, total_distance]


def build_deltas(count, pos):
    #randoms = np.random.uniform(0,1, (count, num_left))
    deltas = np.ones((count, 5))
    deltas[:,pos] = np.linspace(0, 1, num=count)
    print(deltas)
    return deltas

def find_shadow_costs(sp):
    num_customers = 10
    num_diff_deltas = 10

    customers = sp.customers[1:num_customers+1]
    #customers = sp.customers[1:]
    depot = sp.customers[0]
    dispatch = Dispatch(customers, depot)
    print(dispatch.customers)

    shadow_costs = []
    num_vars = 5

    for i in range(num_vars): 
        results = []
        deltas = build_deltas(num_diff_deltas, i) 
        for delta in deltas:
            dispatch.set_delta(delta)
            solution = RollOut().run(dispatch)
            ev = evaluate(solution)
            results.append(ev)
        shadow_costs.append([results, deltas])
    
    return shadow_costs



def shadow_plot(shadow_costs):
    fig = plt.figure()

    print("Shadow costs")
    it = [(x,y,z) for (x,y),z in zip(shadow_costs, range(5))]
    for results, coords, p in it:
        distances = np.array(results)[:,1] 
        xs = coords[:,p]
        
        ax = fig.add_subplot(231+p)
        ax.scatter(xs, distances)

    plt.savefig("data/processed/shadow_costs.png")
    #with open("data/processed/shadow_costs.csv", "wb") as f:
    print(shadow_costs)    

if __name__ == "__main__":
    input_filepath = "data/interim/r101.p"
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)
    
    Parameters().build(sp, 10, 10)

    shadow_costs = find_shadow_costs(sp)
    shadow_plot(shadow_costs)

