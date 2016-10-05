import os
import pickle
import logging 
from collections import defaultdict

import numpy as np

from src import DataBuilder, Cost

LOGGER = logging.getLogger(__name__)

def build_all(data_root, files, outfiles):
    for f, of in zip(files, outfiles):
        DataBuilder(data_root + "/" + f, "data/interim/"+of)

def load_files(data_root):
    files = os.listdir(data_root)
    files = [f for f in files if 'r1' in f]

    outfiles = [f.replace(".txt", ".p") for f in files] 
    return (files, outfiles)

def setup():
    data_root = "data/raw"
    files, outfiles = load_files(data_root)
    build_all(data_root, files, outfiles)
    return sorted(outfiles)

''' This are for summarization and display '''
def group_results(results):
    problemtypes = ["rc1", "rc2", "r1", "r2", "c1", "c2"]
    problemdict = defaultdict(list)
    
    for r in results:
        for pt in problemtypes:
            if r[0].startswith( pt ):
                problemdict[pt].append(r)
    return problemdict

def load_test_results(files, root):
    results = []
    for filename in files:
        with open(root + filename, "rb") as f:
            solution = pickle.load(f)
        
        name = filename
        new_veh, new_dist = solution.num_vehicles, solution.total_distance
        old_veh, old_dist = Cost.of_vehicles(solution.pre_solution.vehicles)
        results.append( (name, new_veh, new_dist, old_veh, old_dist) )
    return results

def summarize_on_all(files):
    root = "data/solutions/"
    
    results = load_test_results(files, root)
    problemdict = group_results(results)

    for key, value in problemdict.items():
        LOGGER.info("Results of all {} problems:".format(key))
        sums = np.mean(np.array([x[1:] for x in value]), axis=0)
        LOGGER.info("({}, {}) => ({}, {})".format(*sums))
