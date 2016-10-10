# load the pickled solution files and create a csv results file




import pickle

import demo_util as util
from src.baseobjects import Validator


def confirm(f, solution):
    customers = sorted(list(set([c for vehicle in solution.solution.vehicles \
        for c in vehicle.customer_history])), key=lambda c: c.custNo)



if __name__ == "__main__":
    root = "data/solutions/search/"
    files, _ = util.load_files(root)
    solutions = [util.load_solution(filename, root) for filename in files]

    for f,s in zip(files,solutions): 
        confirm(f, s)
        Validator(s.solution, f).validate()
    print(files)













