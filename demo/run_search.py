import logging 
import sys 
import time
import random
from multiprocessing import Pool

from demo.demo_util import *

from src import search, Improvement
from src.baseobjects import Utils, Validator

LOGGER = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    
def run_on_file(f):
    LOGGER.info("Run on {}".format(f))
    random.seed(0)
    
    start = time.time()
    solution = search(f, trunc=0, count=20)
    Validator(solution.solution).validate()
    end = time.time()
    
    Utils.save_sp(solution, f)
    LOGGER.info("Solution to {} is {}".format(f, \
        (solution.num_vehicles, solution.total_distance)))
    print("Time elapsed for {}: {}".format(f, end-start))

outfiles = setup()

#for f in outfiles:
#    run_on_file(f)

pool = Pool()
pool.map(run_on_file, outfiles)

summarize_on_all(outfiles)

