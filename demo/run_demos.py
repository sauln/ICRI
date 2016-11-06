''' short script to run rollout algorithm on all problems '''
import logging 
import sys 
import random
from multiprocessing import Pool
from functools import partial

sys.path.append('.')

import demo_util as DUtil
from src import Heuristic, RollOut, search, Search, Improvement, Dispatch, Cost 
from src.baseobjects import Utils, Validator, Parameters, Solution, Heuristic

from db import add_data, queries

LOGGER = logging.getLogger(__name__)
#logging.basicConfig(stream=sys.stderr, level=logging.INFO)

switch_algo = {"rollout":RollOut, "heuristic":Heuristic}

class Params:
    def __init__(self, width, depth, count, algo_type, run_type, problem):
        self.width=width
        self.depth=depth
        self.count=count
        self.algo_type=algo_type
        self.run_type=run_type
        self.problem=problem

    def __repr__(self):
        return "{} {} {} {} {} {}".format(\
            self.problem, self.run_type, self.algo_type, 
            self.width, self.depth, self.count)

def run_search(algo_type, filename):
    LOGGER.info("Run {}".format(filename))
    random.seed(0)
    problem_name=filename.replace(".p", "")
    params = Params(5,5,5, algo_type.__name__.lower(), "search", problem_name)

    if not queries.params_in(params):
        best_solution, all_solutions = search(algo_type, filename, trunc=0, \
                                              count=params.count, \
                                              width=params.width, depth=params.depth)
        
        for sol in all_solutions: 
            add_data.save_result_to_db(params, sol)
    else:
        all_solutions = queries.get_solutions(params)

    return all_solutions, filename

def profile():
    outfiles = DUtil.setup()[:1]
    algo, src= switch_algo["heuristic"], "search/heuristic_" 
    results = [run_search(algo, filename) for filename in outfiles]            

def execute_algorithms(f, t, files):
    runner = partial(f, t)
    #results = Pool().map(runner, files)
    results = [runner(filename) for filename in files]
    return results

def main(argv):
    outfiles = DUtil.setup()
    # tmps = ['r207.p', 'r210.p', 'r211.p', 'rc103.p', 'rc104.p', 'rc107.p', 'rc108.p']
    # outfiles = [f for f in outfiles if "r1" in f]
    print(outfiles)
    if(len(argv) == 0):
        argv.append("profile")

    if argv[0] == "summarize":
        argv.pop(0)
        for key in argv: DUtil.summarize_on_all(outfiles, prefix=key)

    elif argv[0] == "profile":
        profile()
    
    else:
        if argv[0] == "search":
            argv.pop(0), 
            algo= switch_algo[argv[0]]
            results = execute_algorithms(run_search, algo, outfiles)
        elif argv[0] == "improve":
            argv.pop(0)
            algo= switch_algo[argv[0]]
            results = execute_algorithms(run_improvement, algo, outfiles)
        else:
            algo= switch_algo[argv[0]]
            results = execute_algorithms(run_single, algo, outfiles)
             
        #queries.print_results()

def run_single(algo_type, filename):
    LOGGER.info("Run on {}".format(filename))
    sp = Utils.open_sp(filename)
    Parameters().build(sp)

    dispatch = Dispatch(sp.customers)
    delta = [1]*5
    dispatch.set_delta(delta)

    solution = algo_type().run(dispatch, 10, 10)
    num_veh, t_dist = Cost.of_vehicles(solution.vehicles)
    res = Solution(num_veh, t_dist, delta, solution)  
    Validator(solution, filename).validate()
    
    Utils.save_sp(solution, "rollout/"+filename)
    LOGGER.info("Solution: {}".format(Cost.of_vehicles(solution.vehicles)))
    LOGGER.debug("Solution for rollout: {}".format(solution.pretty_print()))
    return [res], filename 

def run_improvement(algo, filename):
    LOGGER.info("Run improvement on {}".format(filename))

    solution = Utils.open_sp(filename, root="data/solutions/search/rollout_")
    
    Parameters().build(Utils.open_sp(filename))
    new_solution = Improvement().run(algo, solution.solution, iterations=50, count=5)
    #Utils.save_sp(new_solution, filename, root="data/solutions/improve/rollout_")
    
    problem_name=filename.replace(".p", "")
    for sol in all_solutions: 
        add_data.save_result_to_db(params, sol)

    #LOGGER.info("Finished {}".format(filename))
    return [new_solution], filename

if __name__ == "__main__":
    main(sys.argv[1:])

