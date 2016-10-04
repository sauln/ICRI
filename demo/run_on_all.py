import os
import pickle
import logging 
import sys 
from collections import defaultdict

import numpy as np

import random
from multiprocessing import Pool

from src import DataBuilder, search, Improvement
from src.baseobjects import Utils, Cost, Validator
LOGGER = logging.getLogger(__name__)

def run_on_all_problems(files):
    #rfiles = sorted(list(filter(lambda x: "r1" in x, files)))
    rfiles = sorted(files)

    LOGGER.info("Run for r type files: {}".format(rfiles))
   
    #run_serial(rfiles)
    run_parallel(rfiles)
    
def run_parallel(rfiles):
    pool = Pool()
    pool.map(run_on_file, rfiles)
   
def run_serial(rfiles):
    for f in rfiles:
        run_on_file(f)

def load_files(data_root):
    files = os.listdir(data_root)
    files = [f for f in files if 'r1' in f]

    outfiles = [f.replace(".txt", ".p") for f in files] 
    return (files, outfiles)

def run_on_file(f):
    LOGGER.info("Run on {}".format(f))
    random.seed(0)
    solution = search(f, trunc=0, count=1)
    solution.pre_solution = solution.solution
    solution.solution = Improvement().run(solution.pre_solution, 5, 20)
    Validator(solution.solution).validate()
    Utils.save_sp(solution, f)
    LOGGER.info("Solution to {} is {}".format(f, \
        (solution.num_vehicles, solution.total_distance)))

def build_all(data_root, files, outfiles):
    for f, of in zip(files, outfiles):
        DataBuilder(data_root + "/" + f, "data/interim/"+of)


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

def run():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    data_root = "data/raw"
    files, outfiles = load_files(data_root)
    build_all(data_root, files, outfiles)
    run_on_all_problems(outfiles)
    summarize_on_all(outfiles)


if __name__ == "__main__":
    run()

