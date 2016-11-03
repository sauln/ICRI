import os
import pickle
import logging 
from collections import defaultdict
import csv

import pandas as pd
import numpy as np

from src import DataBuilder, Cost, Dispatch, Solution, Utils

LOGGER = logging.getLogger(__name__)

def write_csv(labels, data_list, filename):
    with open(filename, 'w', newline='') as f:
        solution_writer = csv.writer(f)
        solution_writer.writerow(labels)
        
        for line in data_list:
            solution_writer.writerow(line)


def build_all(data_root, files, outfiles):
    for f, of in zip(files, outfiles):
        DataBuilder(data_root + "/" + f, "data/interim/"+of)

def load_files(data_root):
    files = sorted(os.listdir(data_root))
    #files = [f for f in files if 'rc' in f]
    LOGGER.debug("Loaded files {}".format(files))
    outfiles = [f.replace(".txt", ".p") for f in files] 
    return (files, outfiles)

def setup():
    data_root = "data/raw"
    files, outfiles = load_files(data_root)
    build_all(data_root, files, outfiles)

    #outfiles = [o for o in outfiles if "r20" in o]
    return sorted(outfiles)

''' This are for summarization and display '''
def group_results(results, prefix=''):
    problemtypes = ["rc1", "rc2", "r1", "r2", "c1", "c2"]
    problemtypes = list(map(lambda x: prefix+x, problemtypes))
    problemdict = defaultdict(list)
  
    for res in results:
        for pt in problemtypes:
            if res[0].startswith( pt ):
                problemdict[pt].append(res)

    return problemdict

def load_solution(filename, root):
    with open(root + filename, "rb") as f:
        solution = pickle.load(f)
    return solution 

def load_test_result(filename, root):
    try:
        solution = load_solution(filename, root)
        name = filename
        
        if isinstance(solution, Dispatch):
            num_veh, dist = Cost.of_vehicles(solution.vehicles)
            return (name, num_veh, dist)
        elif isinstance(solution, Solution):
            new_veh, new_dist = solution.num_vehicles, solution.total_distance

            if solution.pre_solution is not None:
                old_veh, old_dist = Cost.of_vehicles(solution.pre_solution.vehicles)
                return (name, new_veh, new_dist, old_veh, old_dist)
            else:
                return (name, new_veh, new_dist) 
    except:
        return 0

def summarize_on_all(files, prefix=''):
    root = "data/solutions/"
    
    loaded_results = [load_test_result(prefix+f, root) for f in files] 
    results = [res for res in loaded_results if res is not 0]
    if(len(results) is not len(loaded_results)):
        LOGGER.info("Some files not loaded properly. Summarizing incomplete fileset")
   
    problemdict = group_results(results, prefix)

    for key, value in problemdict.items():
        print("{}".format(key))
        sums = np.mean(np.array([x[1:] for x in value]), axis=0)
        print("{} {}".format(*sums))

def write_solution(solutions):
    sol_lines = [write_line(sol, fil) for sol, fil in solutions]
    lines = [line for solution in sol_lines for line in solution]
    labels = ["filename", "num_veh", "dist", "d0", "d1", "d2", "d3", "d4"]
    
    filename = "data/" + "random_search" + "_trial.csv"
    DUtil.write_csv(labels, lines, filename)

def write_line(solutions, filename):
    lines = []
    for solution in solutions:
        lines.append([filename, solution.num_vehicles, \
            solution.total_distance] + list(solution.params))
    return lines

def make_line(problem):
    basic_props = (problem.problemName, problem.numVehicles, \
                   problem.capacity, len(problem.customers))
    
    total_demand = sum(c.demand for c in problem.customers)
    min_vehicles_capacity = total_demand / problem.capacity
    demand_props = (total_demand, min_vehicles_capacity)
  
    distance_props = ["minimum pairwise distance", "maximum pairwise distnace"]
    distance_props += ["Sum closest neighbor", "Sum farthest neighbor"]
    distance_props += ["Total complete graph", "Total distance from depot"]
    timewindow_props = ["Total service time"]

    return basic_props + demand_props

def summarize_problems():
    _, outfiles = load_files("data/raw")
    problems = [Utils.open_sp(filename) for filename in outfiles]

    labels = ["Problem name", "Number of vehicles", "Max capacity", "Customers"]
    labels += ["total demand", "Minimum vehicles to satisfy capacity"]
    lines = [make_line(p) for p in problems]

    return (labels, lines)

def merge_results_and_summary(summaryfile, resultsfile):
    replace_p = lambda x: x.replace(".p", "")
    a = pd.read_csv(summaryfile)
    a['Problem name'] = a['Problem name'].str.lower()

    b = pd.read_csv(resultsfile)
    b['filename'] = b['filename'].map(replace_p)
    c = pd.merge(b,a, how="left", left_on="filename", right_on="Problem name")
    c = c.drop("Problem name", 1)
    
    return c

def aggregate_results(result_type): 
    labels, lines = summarize_problems()
    summary_filename = "data/results/test_problem_summaries.csv"
    
    write_csv(labels, lines, summary_filename)
    
    results_filename = "data/results/" + result_type + "_trial.csv" 
    out_filename = "data/results/" + result_type + "_w_summaries.csv"
    
    results = merge_results_and_summary(summary_filename, results_filename)
    #results.to_csv(out_filename, index=False)


    return results










