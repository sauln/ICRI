# short script to just run heuristic algorithm on all problems 

import logging 
import sys 
from demo.demo_util import *

from src import Heuristic 
from src.baseobjects import *


def run_heuristic(ps):
    LOGGER.info("Run on {}".format(f))
    sp = open_sp(ps)
    Parameters().build(sp)

    dispatch = Dispatch(sp.customers)
    delta = [1]*5
    dispatch.set_delta(delta)
    
    solution = Heuristic().run(dispatch)
   
    LOGGER.info("Solution: {}".format(Cost.of_vehicles(solution.vehicles)))
    LOGGER.debug("Solution for heuristic: {}".format(solution.solutionStr()))

LOGGER = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
outfiles = setup()

for f in outfiles[:2]:
    run_heuristic(f)

summarize_on_all(outfiles)



