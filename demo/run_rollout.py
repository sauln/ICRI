''' short script to run rollout algorithm on all problems '''
import logging 
import sys 
import random
from multiprocessing import Pool
from demo.demo_util import *

from src import Heuristic, RollOut, search, Improvement 
from src.baseobjects import Utils, Validator, Parameters

LOGGER = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

@Utils.timeit
def run_heuristic(ps):
    LOGGER.info("Run on {}".format(f))
    sp = Utils.open_sp(ps)
    Parameters().build(sp)

    dispatch = Dispatch(sp.customers)
    delta = [1]*5
    dispatch.set_delta(delta)
    
    solution = Heuristic().run(dispatch)
    Validator(solution, ps).validate()
    
    Utils.save_sp(solution, "heuristic/"+ps)

    LOGGER.info("Solution: {}".format(Cost.of_vehicles(solution.vehicles)))
    LOGGER.debug("Solution for heuristic: {}".format(solution.pretty_print()))


@Utils.timeit
def run_rollout(ps):
    LOGGER.info("Run on {}".format(f))
    sp = Utils.open_sp(ps)
    Parameters().build(sp)

    dispatch = Dispatch(sp.customers)
    delta = [1]*5
    dispatch.set_delta(delta)

    solution = RollOut().run(dispatch, 5, 5)
    Validator(solution, ps).validate()
    Utils.save_sp(solution, "rollout_"+ps)

    LOGGER.info("Solution: {}".format(Cost.of_vehicles(solution.vehicles)))
    LOGGER.debug("Solution for rollout: {}".format(solution.pretty_print()))

@Utils.timeit
def run_search(f):
    LOGGER.info("Run on {}".format(f))
    random.seed(0)
    solution = search(f, trunc=0, count=10, width=10, depth=10)
    Validator(solution.solution, f).validate()
    
    Utils.save_sp(solution, "search/" +f)
    LOGGER.info("Solution to {} is {}".format(f, \
        (solution.num_vehicles, solution.total_distance)))

outfiles = setup()
for key in ["heuristic", "rollout", "search"]:
    switch = {"search":run_search, "rollout":run_rollout, "heuristic":run_heuristic}
    t, src = switch[key], key+"/"

    for f in outfiles:
        t(f)

    summarize_on_all(outfiles, prefix=src)

#pool = Pool()
#pool.map(run_on_file, outfiles)

