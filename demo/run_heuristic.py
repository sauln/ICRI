# short script to just run heuristic algorithm on all problems 

import logging 
import sys 
from demo.demo_util import *

from src import Heuristic 
from src.baseobjects import *

LOGGER = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

def run_heuristic(ps):
    LOGGER.info("Run on {}".format(f))
    sp = open_sp(ps)
    Parameters().build(sp)

    dispatch = Dispatch(sp.customers)
    delta = [1]*5
    dispatch.set_delta(delta)
    
    solution = Heuristic().run(dispatch)
    Validator(solution, ps).validate()
    
    save_sp(solution, "heuristic/"+ps)

    LOGGER.info("Solution: {}".format(Cost.of_vehicles(solution.vehicles)))
    LOGGER.debug("Solution for heuristic: {}".format(solution.pretty_print()))

outfiles = setup()

for f in outfiles:
    run_heuristic(f)

summarize_on_all(outfiles, prefix="heuristic/")



