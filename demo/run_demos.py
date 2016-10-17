''' short script to run rollout algorithm on all problems '''
import logging 
import sys 
import random
from multiprocessing import Pool
import demo_util as DUtil

import csv

from src import Heuristic, RollOut, search, Improvement, Dispatch, Cost 
from src.baseobjects import Utils, Validator, Parameters, Solution

LOGGER = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

switch_algo = {"rollout":RollOut, "heuristic":Heuristic}

def write_solution(search_type, solutions):
    labels = ["search_type", "filename", "num_veh", "dist", "d0", "d1", "d2", "d3", "d4"]
    with open("data/"+search_type+"_trial.csv", 'w', newline='') as f:
        solution_writer = csv.writer(f)
        solution_writer.writerow(labels)
        
        sol_lines = [write_line(search_type, sol, fil) for sol, fil in solutions]
        for lines in sol_lines:
            for line in lines:
                solution_writer.writerow(line)

def write_line(search_type, solutions, filename):
    lines = []
    for solution in solutions:
        if(solution.solution.delta is solution.params):
            print("EQUAL:{}".format(solution.params))
            
        # why does solution.params != solution.solution.delta
        lines.append([search_type, filename, solution.num_vehicles, solution.total_distance] \
            + list(solution.params))
    return lines

def run_single(algo_type, filename):
    LOGGER.info("Run on {}".format(filename))
    sp = Utils.open_sp(filename)
    Parameters().build(sp)

    dispatch = Dispatch(sp.customers)
    delta = [1]*5
    dispatch.set_delta(delta)

    solution = algo_type().run(dispatch, 5, 5)
    num_veh, t_dist = Cost.of_vehicles(solution.vehicles)
    res = Solution(num_veh, t_dist, delta, solution)  
    Validator(solution, filename).validate()
    
    Utils.save_sp(solution, "rollout/"+filename)
    LOGGER.info("Solution: {}".format(Cost.of_vehicles(solution.vehicles)))
    LOGGER.debug("Solution for rollout: {}".format(solution.pretty_print()))
    return [res], filename 

def run_search(algo_type, filename):
    LOGGER.info("Run on {}".format(filename))
    random.seed(0)

    # run many iterations over either rollout, heuristic
    best_solution, all_solutions = search(algo_type, filename, trunc=0, count=10, \
                                          width=10, depth=10)
    
    Utils.save_sp(best_solution, algo_type.__name__.lower()+"/" +filename)
    LOGGER.info("Solution to {} is {}".format(filename, \
        (best_solution.num_vehicles, best_solution.total_distance)))

    return all_solutions, filename

def main(argv):
    outfiles = DUtil.setup()

    if argv[0] == "summarize":
        argv.pop(0)
        for key in argv:
            DUtil.summarize_on_all(outfiles, prefix=key+"/")
    else:
        if argv[0] == "search":
            argv.pop(0)
            run_type = run_search
        else:
            run_type = run_single
        
        for key in argv:
            algo, src = switch_algo[key], key + "/" 
            results = [run_type(algo, filename) for filename in outfiles]            
            
            write_solution(key, results)
            DUtil.summarize_on_all(outfiles, prefix=src)

if __name__ == "__main__":
    main(sys.argv[1:])

