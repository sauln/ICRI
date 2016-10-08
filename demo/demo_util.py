import os
import pickle
import logging 
from collections import defaultdict

import numpy as np

from src import DataBuilder, Cost, Dispatch, Solution

LOGGER = logging.getLogger(__name__)

def build_all(data_root, files, outfiles):
    for f, of in zip(files, outfiles):
        DataBuilder(data_root + "/" + f, "data/interim/"+of)

def load_files(data_root):
    files = os.listdir(data_root)
    files = [f for f in files if 'rc101' in f]
    print(files)
    outfiles = [f.replace(".txt", ".p") for f in files] 
    return (files, outfiles)

def setup():
    data_root = "data/raw"
    files, outfiles = load_files(data_root)
    build_all(data_root, files, outfiles)
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

def load_test_result(filename, root):
    with open(root + filename, "rb") as f:
        solution = pickle.load(f)
    
    name = filename
    
    if isinstance(solution, Dispatch):
        num_veh, dist = Cost.of_vehicles(solution.vehicles)
        return (name, num_veh, dist)
    elif isinstance(solution, Solution):
        new_veh, new_dist = solution.num_vehicles, solution.total_distance
        old_veh, old_dist = Cost.of_vehicles(solution.pre_solution.vehicles)
        return (name, new_veh, new_dist, old_veh, old_dist)


def summarize_on_all(files, prefix=''):
    root = "data/solutions/"
   
    results = [load_test_result(prefix+f, root) for f in files] 
    problemdict = group_results(results, prefix)

    for key, value in problemdict.items():
        LOGGER.info("Results of all {} problems:".format(key))
        sums = np.mean(np.array([x[1:] for x in value]), axis=0)
        LOGGER.info("({})".format(sums))
