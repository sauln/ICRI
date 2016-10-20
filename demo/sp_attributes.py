''' 
Open up the Solomon Problems, generate summary statistics
about the problem definition and save as csv
'''
import pandas as pd

import src
import demo_util as DUtil

def make_line(problem):
    basic_props = (problem.problemName, problem.numVehicles, \
                   problem.capacity, len(problem.customers))
    
    total_demand = sum(c.demand for c in problem.customers)
    min_vehicles_capacity = total_demand / problem.capacity
    demand_props = (total_demand, min_vehicles_capacity)
  
    distance_props = ["minimum pairwise distance", "maximum pairwise distnace"]
    distance_props += ["Sum closest neighbor", "Sum farthest neighbor"]
    distance_props += ["Total complete graph", "Total distance from depot"]
    timewindow_props = ["Total service time"]

    return basic_props + demand_props

def summarize_problems():
    _, outfiles = DUtil.load_files("data/raw")
    problems = [src.Utils.open_sp(filename) for filename in outfiles]

    labels = ["Problem name", "Number of vehicles", "Max capacity", "Customers"]
    labels += ["total demand", "Minimum vehicles to satisfy capacity"]
    lines = [make_line(p) for p in problems]

    return (labels, lines)

def merge_results_and_summary(summaryfile, resultsfile):
    replace_p = lambda x: x.replace(".p", "")
    a = pd.read_csv(summaryfile)
    a['Problem name'] = a['Problem name'].str.lower()

    b = pd.read_csv(resultsfile)
    b['filename'] = b['filename'].map(replace_p)
    c = pd.merge(b,a, how="left", left_on="filename", right_on="Problem name")
    c = c.drop("Problem name", 1)
    
    return c

    
labels, lines = summarize_problems()
    
filename = "data/test_problem_summaries.csv"
DUtil.write_csv(labels, lines, filename)

results = merge_results_and_summary(filename, "data/heuristic_trial.csv")
mins = results.sort_values('num_veh').groupby('filename', as_index=False).first()

import matplotlib.pyplot as plt
deltas = ['d0', 'd1','d2','d3','d4']


print(results.head())
print(len(list(mins.itertuples())))


for m in mins.itertuples():
    plt.plot(m[5:10])
plt.show()


