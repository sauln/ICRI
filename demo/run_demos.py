''' short script to run rollout algorithm on all problems '''
import logging 
import sys 
import random
from multiprocessing import Pool
from functools import partial

import demo_util as DUtil
from src import Heuristic, RollOut, search, Improvement, Dispatch, Cost 
from src.baseobjects import Utils, Validator, Parameters, Solution

LOGGER = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

switch_algo = {"rollout":RollOut, "heuristic":Heuristic}

def write_solution(search_type, solutions):
    filename = "data/" + search_type + "_trial.csv"
    sol_lines = [write_line(search_type, sol, fil) for sol, fil in solutions]
    lines = [line for solution in sol_lines for line in solution]
    labels = ["search_type", "filename", "num_veh", "dist", "d0", "d1", "d2", "d3", "d4"]

    DUtil.write_csv(labels, lines, filename)

def write_line(search_type, solutions, filename):
    lines = []
    for solution in solutions:
        lines.append([search_type, filename, solution.num_vehicles, \
            solution.total_distance] + list(solution.params))
    return lines

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
    print(filename)

    solution = Utils.open_sp(filename, root="data/solutions/search/rollout_")
    
    Parameters().build(Utils.open_sp(filename))
    new_solution = Improvement().run(algo, solution.solution, filename, 50, 5)
    
    LOGGER.info("Original solution to {} is {}".format(filename, \
        (solution.num_vehicles, solution.total_distance)))
    
    LOGGER.info("Solution to {} is {}".format(filename, \
        (len(new_solution.solution.vehicles), new_solution.total_distance)))

    Utils.save_sp(new_solution, filename, root="data/solutions/improve/rollout_")

    LOGGER.info("Finished {}".format(filename))
    return [new_solution], filename

def run_search(algo_type=None, filename=None):
    LOGGER.info("Run on {}".format(filename))
    random.seed(0)

    # run many iterations over either rollout, heuristic
    best_solution, all_solutions = search(algo_type, filename, trunc=0, count=25, \
                                          width=5, depth=5)
    
    Utils.save_sp(best_solution, "search/" +algo_type.__name__.lower()+ "_" +filename)
    LOGGER.info("Solution to {} is {}".format(filename, \
        (best_solution.num_vehicles, best_solution.total_distance)))

    return all_solutions, filename

def profile():
    outfiles = DUtil.setup()[:1]
    algo, src= switch_algo["heuristic"], "search/heuristic_" 
    results = [run_search(algo, filename) for filename in outfiles]            
    
def main(argv):
    outfiles = DUtil.setup()
    # tmps = ['r207.p', 'r210.p', 'r211.p', 'rc103.p', 'rc104.p', 'rc107.p', 'rc108.p']
    # outfiles = [f for f in outfiles if "r1" in f]
    print(outfiles)
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
            argv.pop(0)
            run_type = run_search
            src_lambda = lambda key: "search/" + key + "_"
        elif argv[0] == "improve":
            argv.pop(0)
            run_type = run_improvement
            src_lambda = lambda key: "improve/" + key + "_"
        else:
            run_type = run_single
            src_lambda = lambda key: key + "/"
    
        for key in argv:
            algo, src = switch_algo[key], src_lambda(key)
            
            runner = partial(run_type, algo)
            results = Pool().map(runner, outfiles)
            #results = [run_type(algo, filename) for filename in outfiles]            
            #results = [runner(filename) for filename in outfiles]

            write_solution(key, results)
            DUtil.summarize_on_all(outfiles, prefix=src)




if __name__ == "__main__":
    main(sys.argv[1:])

