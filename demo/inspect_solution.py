import pickle

if __name__ == "__main__":
    filename = "data/solutions/r101.p"
    with open(filename, "rb") as f:
        solution = pickle.load(f)

    import pdb
    pdb.set_trace()



