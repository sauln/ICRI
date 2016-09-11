import pickle
import logging
import csv

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

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
            line = np.concatenate((ev, delta))
            results.append(line)
        shadow_costs.append(np.array(results))

    return shadow_costs


def save_as_csv(shadow_costs):
    flattened = np.concatenate(shadow_costs)

    with open("data/processed/shadow_costs.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Num Vehicles", "Distance"] + ["Delta"]*5)
        for row in flattened:
            writer.writerow(row)


def shadow_plot(shadow_costs):
    fig = plt.figure()

    print("Plot and save shadow costs")

    for p, var in enumerate(shadow_costs):
        num_vehicles = var[:,0]
        distances = var[:,1]
        deltas = var[:,p+2]
       

        ax = fig.add_subplot(len(shadow_costs), 2, 2*p)
        ax.scatter(deltas, distances)
        ax.set_title("Total distance of parameter {}".format(p))
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.0f"))

        ax = fig.add_subplot(len(shadow_costs), 2, 2*p + 1)
        ax.scatter(deltas, num_vehicles)
        ax.set_title("Total vehicles of parameter {}".format(p))

    plt.savefig("data/processed/shadow_costs.png")
    #    plt.show()


if __name__ == "__main__":
    input_filepath = "data/interim/r101.p"
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)
    
    Parameters().build(sp, 10, 10)

    shadow_costs = find_shadow_costs(sp)
    shadow_plot(shadow_costs)
    save_as_csv(shadow_costs)
