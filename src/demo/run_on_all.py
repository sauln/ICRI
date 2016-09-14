import os
import pickle
 
from src.main.Algorithms.RollOut import run_roll_out 
from src.data.make_dataset import DataBuilder


def load_files():
    data_root = "data/raw"
    files = os.listdir(data_root)

    outfiles = [f.replace(".txt", ".p") for f in files] 

    return (files, outfiles)


def run_on_all_problems():
    
    files, outfiles = load_files()
    for f, of in zip(files, outfiles):
        DataBuilder(data_root + "/" + f, "data/interim/"+of)

    for f in outfiles:
        print("Run on {}".format(f))
        run_roll_out(f)

def summarize(xs):
    avg_veh = sum([x[1] for x in xs])/len(xs)
    avg_dist = sum([x[2] for x in xs])/len(xs)

    return (avg_veh, avg_dist)
        

def summarize_on_all():
    _, files = load_files()
    
    root = "data/solutions/"

    # unpickle each file in files,
    # check get name, vehicle #, and total distance
    # group them

    results = []

    for filename in files:
        with open(root + filename, "rb") as f:
            solution = pickle.load(f)
        
        totalDist = sum( [v.totalDist for v in solution.vehicles] )
        num_veh = len(solution.vehicles)
        name = filename
        results.append( (name, num_veh, totalDist) )

    rc1s = []
    rc2s = []
    c1s = []
    c2s = []
    r1s = []
    r2s = []
    for r in results:
        if r[0][:3] == "rc1":
            rc1s.append(r)
        elif r[0][:3] == "rc2":
            rc2s.append(r)
        elif r[0][:2] == "r1":
            r1s.append(r)
        elif r[0][:2] == "r2":
            r2s.append(r)
        elif r[0][:2] == "c1":
            c1s.append(r)
        elif r[0][:2] == "c2":
            c2s.append(r)
    print("Results of all R1 problems:")
    print(summarize(r1s))
    print("Results of all R2 problems:")
    print(summarize(r2s))
    
    print("Results of all C1 problems:")
    print(summarize(c1s))
    print("Results of all C2 problems:")
    print(summarize(c2s))

    print("Results of all RC1 problems:")
    print(summarize(rc1s))
    print("Results of all RC2 problems:")
    print(summarize(rc2s))


if __name__ == "__main__":
    #run_on_all_problems()

    summarize_on_all()

