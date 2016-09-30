import pickle

''' These 3 functions can be used elsewhere '''
def open_sp(fname, root = "data/interim/"):
    input_filepath = root + fname
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)
    return sp

def save_sp(solution, fname, root="data/solutions/"):
    output_filepath = root + fname 
    with open(output_filepath, "wb") as f:
        pickle.dump(solution, f)

def save_as_csv(costs, filename, root="data/processed/"):
    print("Saving grid search results as {}".format(root+filename))
    with open(root + filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Num Vehicles", "Distance"] + ["lam"]*5)
        for row in costs:
            writer.writerow([row.num_vehicles, row.total_distance] + list(row.params))

