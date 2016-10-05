import logging 
import sys 

import random
from multiprocessing import Pool

from demo.demo_util import *

from src import search, Improvement
from src.baseobjects import Utils, Validator
LOGGER = logging.getLogger(__name__)

    
def run_parallel(rfiles):
    pool = Pool()
    pool.map(run_on_file, rfiles)
   
def run_serial(rfiles):
    for f in rfiles:
        run_on_file(f)

def run_on_file(f):
    LOGGER.info("Run on {}".format(f))
    random.seed(0)
    solution = search(f, trunc=0, count=1)
    solution.pre_solution = solution.solution
    solution.solution = Improvement().run(solution.pre_solution, 5, 1)
    Validator(solution.solution).validate()
    Utils.save_sp(solution, f)
    LOGGER.info("Solution to {} is {}".format(f, \
        (solution.num_vehicles, solution.total_distance)))

def run():
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    outfiles = setup()
    #run_on_all_problems(outfiles)
    run_serial(outfiles)
    #run_parallel(rfiles)
    summarize_on_all(outfiles)

if __name__ == "__main__":
    run()

