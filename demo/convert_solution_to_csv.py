# load the pickled solution files and create a csv results file

import pickle

import demo_util as util
from src.baseobjects import Validator


def visual_confirmation(f, s):
    print(f)
    print(s.pretty_print())


if __name__ == "__main__":
    root = "data/solutions/search/"
    files, _ = util.load_files(root)
    files = [f for f in files if "c1" in f and "rc" not in f]    
    
    solutions = [util.load_solution(filename, root) for filename in files]

    for f,s in zip(files,solutions): 
        visual_confirmation(f, s.solution)
        Validator(s.solution, f).validate()

