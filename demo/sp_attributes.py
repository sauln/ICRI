''' 
Open up the Solomon Problems, generate summary statistics
about the problem definition and save as csv
'''

import src
import demo_util as DUtil
_, outfiles = DUtil.load_files("data/raw")
problems = [src.Utils.open_sp(filename) for filename in outfiles]


def make_line(problem):
    basic_props = (problem.problemName, problem.numVehicles, \
                   problem.capacity, len(problem.customers))
    
    total_demand = sum(c.demand for c in problem.customers)
    min_vehicles_capacity = total_demand / problem.capacity
    demand_props = (total_demand, min_vehicles_capacity)
  
    distance_props = ["minimum pairwise distance", "maximum pairwise distnace"]
    distance_props += ["Sum closest neighbor", "Sum farthest neighbor"]
    distance_props += ["Total complete graph"]
    distance_props += ["Total distance from depot"]

    timewindow_props = ["Total service time"]


    return basic_props + demand_props


filename = "data/test_problem_summaries.csv"
labels = ["Problem name", "Number of vehicles", "Max capacity", "Customers"]
labels += ["total demand", "Minimum vehicles to satisfy capacity"]
lines = [make_line(p) for p in problems]

DUtil.write_csv(labels, lines, filename)


'''
    Base attributes to derive values from
        self.problemName     = name
        self.numVehicles     = numVeh
        self.capacity        = capacity
        self.customers       = customers
'''


print(problems)




