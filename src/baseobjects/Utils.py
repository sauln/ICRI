import pickle
import time
import logging

LOGGER = logging.getLogger(__name__)

''' timing decorator '''
def timeit(f):
    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        LOGGER.info('func:%r args:[%r, %r] took: %2.4f sec' % \
            (f.__name__, args, kw, te-ts))
        return result
    return timed

''' Counter for logging grid search information that is multiprocessing safe '''
counter = None
def increment():
    global counter
    with counter.get_lock():
        counter.value += 1

def value():
    global counter
    with counter.get_lock():
        return counter.value

def init(args):
    global counter
    counter = args

''' Slightly generalized IO functions '''
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

