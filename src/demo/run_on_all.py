import os
import pickle

from collections import defaultdict

from src.main.Algorithms.GridSearch import run_search
from src.main.Algorithms.RollOut import run_roll_out 
from src.data.make_dataset import DataBuilder

def load_files(data_root):
    files = os.listdir(data_root)
    outfiles = [f.replace(".txt", ".p") for f in files] 
    return (files, outfiles)

def save_sp(solution, fname, root="data/solutions/"):
    output_filepath = root + fname 
    with open(output_filepath, "wb") as f:
        pickle.dump(solution, f)

def run_on_all_problems():
    data_root = "data/raw"
    
    files, outfiles = load_files(data_root)
    for f, of in zip(files, outfiles):
        DataBuilder(data_root + "/" + f, "data/interim/"+of)

    rfiles = list(filter(lambda x: "c" not in x, outfiles))
    print("Run for r type files: {}".format(rfiles))

    for f in rfiles:
        print("Run on {}".format(f))
        solution = run_search(f) 
        #solution = run_roll_out(f)
        save_sp(solution, f)

def summarize(xs):
    avg_veh = sum([x[1] for x in xs])/len(xs)
    avg_dist = sum([x[2] for x in xs])/len(xs)

    return (avg_veh, avg_dist)

def summarize_on_all():
    root = "data/solutions/"
    _, files = load_files(root)
    
    results = []

    for filename in files:
        with open(root + filename, "rb") as f:
            solution = pickle.load(f)
        
        totalDist = solution.total_distance
        num_veh = solution.num_vehicles
        name = filename
        results.append( (name, num_veh, totalDist) )

    problemtypes = ["rc1", "rc2", "r1", "r2", "c1", "c2"]
    problemdict = defaultdict(list)

    for r in results:
        for pt in problemtypes:
            if r[0].startswith( pt ):
                problemdict[pt].append(r)

    for key, value in problemdict.items():
        print("Results of all {} problems:".format(key))
        print(summarize(value))


if __name__ == "__main__":
    print("STARTING THE GRID SEARCH ON ALL FILES!!")
    # run_on_all_problems()
    print("SUMMARIZING THE  GRID SEARCH ON ALL FILES!!!!")
    summarize_on_all()
    print("WOOOOOOHOOOO WE FINISHED!!!!!")


