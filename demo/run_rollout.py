# short script to just run rollout algorithm on all problems 

import logging 
import sys 
from demo.demo_util import *

from src import RollOut 
from src.baseobjects import *

LOGGER = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

def run_rollout(ps):
    LOGGER.info("Run on {}".format(f))
    sp = open_sp(ps)
    Parameters().build(sp)

    dispatch = Dispatch(sp.customers)
    delta = [1]*5
    dispatch.set_delta(delta)
   
    solution = RollOut().run(dispatch, 5, 5)
    LOGGER.info("Solution: {}".format(Cost.of_vehicles(solution.vehicles)))
    LOGGER.debug("Solution for rollout: {}".format(solution.solutionStr()))

outfiles = setup()

for f in outfiles[:2]:
    run_rollout(f)

summarize_on_all(outfiles)


