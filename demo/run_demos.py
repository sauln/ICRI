''' short script to run rollout algorithm on all problems '''
import logging
import sys
import random
from multiprocessing import Pool
from functools import partial

sys.path.append('.')

import demo_util as DUtil
from src import Heuristic, RollOut, search, Improvement, Dispatch, Cost
from src.baseobjects import Utils, Validator, Parameters, Solution, Heuristic, Params



from db import add_data, queries

LOGGER = logging.getLogger(__name__)




def run_search(algo_type, filename):
    print("Run {}".format(filename))
    random.seed(999)
    problem_name=filename.replace(".p", "")
    params = Params(10,10,20, algo_type.__name__.lower(),
                           "search", problem_name)

    best_solution, all_solutions = search(algo_type, params)
    return all_solutions, filename

def run_improvement(algo_type, filename):
    LOGGER.info("Run improvement on {}".format(filename))
    # need some initial solution:
    problem_name=filename.replace(".p", "")
    search_params = Params(10,10,20, algo_type.__name__.lower(),
                           "search", problem_name)
    improv_params = {"iterations":5, "count":5, "algo":algo_type}

    improved_solution = Improvement().run(base_solution=None, search_params=search_params,
                                          improv_params=improv_params)

    add_data.save_improvement_result(improved_solution, search_params, improv_params)
    return improved_solution, filename

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
    outfiles = [f for f in outfiles if 'r1' in f and 'c' not in f]
    print(outfiles)
    switch_algo = {"rollout":RollOut, "heuristic":Heuristic}
    if(len(argv) == 0):
        argv.append("profile")

    if argv[0] == "summarize":
        argv.pop(0)
        for key in argv:
            DUtil.summarize_on_all(outfiles, prefix=key)
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

if __name__ == "__main__":
    main(sys.argv[1:])

