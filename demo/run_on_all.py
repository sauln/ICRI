import os
import pickle
import logging 
import sys 
from collections import defaultdict

import random

from src import DataBuilder, run_search, Improvement
LOGGER = logging.getLogger(__name__)

def load_files(data_root):
    files = os.listdir(data_root)
    outfiles = [f.replace(".txt", ".p") for f in files] 
    return (files, outfiles)

def save_sp(solution, fname, root="data/solutions/"):
    output_filepath = root + fname 
    with open(output_filepath, "wb") as f:
        pickle.dump(solution, f)

def run_on_file(f):
    LOGGER.info("Run on {}".format(f))
    random.seed(0)
    solution = run_search(f, trunc=0, count=100)
    solution.pre_solution = solution.solution
    solution.solution = Improvement().run(solution.pre_solution)
    save_sp(solution, f)

def build_all(data_root, files, outfiles):
    for f, of in zip(files, outfiles):
        DataBuilder(data_root + "/" + f, "data/interim/"+of)
    
def run_on_all_problems(files):
    rfiles = sorted(list(filter(lambda x: "r1" in x, files)))
    
    LOGGER.info("Run for r type files: {}".format(rfiles))
    from multiprocessing import Pool
    pool = Pool()
    pool.map(run_on_file, rfiles)
    #for f in rfiles:
    #    pool.apply_async(run_on_file(f)


def summarize(xs):
    avg_veh = sum([x[1] for x in xs])/len(xs)
    avg_dist = sum([x[2] for x in xs])/len(xs)
    pre_av = sum([x[3] for x in xs])/len(xs)
    pre_ad = sum([x[4] for x in xs])/len(xs)
    return (avg_veh, avg_dist, pre_av, pre_ad)

def summarize_on_all():
    root = "data/solutions/"
    _, files = load_files(root)
    
    results = []

    for filename in files:
        with open(root + filename, "rb") as f:
            solution = pickle.load(f)
        
        totalDist = solution.total_distance
        num_veh = solution.num_vehicles
        name = filename
       
        pre_dist = sum([v.totalDist for v in solution.pre_solution.vehicles])
        pre_veh = len(solution.pre_solution.vehicles)
        
        results.append( (name, num_veh, totalDist, pre_veh, pre_dist) )

    problemtypes = ["rc1", "rc2", "r1", "r2", "c1", "c2"]
    problemdict = defaultdict(list)

    for r in results:
        for pt in problemtypes:
            if r[0].startswith( pt ):
                LOGGER.info(r)
                problemdict[pt].append(r)

    for key, value in problemdict.items():
        LOGGER.info("Results of all {} problems:".format(key))
        sums = summarize(value)
        LOGGER.info("({}, {}) => ({}, {})".format(sums[0], sums[1], sums[2], sums[3]))


if __name__ == "__main__":
    data_root = "data/raw"
   
    # this is just DataBuilder.convert_all w/ diff args
    files, outfiles = load_files(data_root)
    build_all(data_root, files, outfiles)
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    LOGGER.info("STARTING THE GRID SEARCH ON ALL FILES!!")
    run_on_all_problems(outfiles)
    LOGGER.info("SUMMARIZING THE  GRID SEARCH ON ALL FILES!!!!")
    summarize_on_all()
    LOGGER.info("WOOOOOOHOOOO WE FINISHED!!!!!")


