''' 
Open up the Solomon Problems, generate summary statistics
about the problem definition and save as csv
'''
import matplotlib.pyplot as plt

import src
import demo_util as DUtil

heuristics = DUtil.aggregate_results("heuristic")
mins_heur = heuristics.sort_values('num_veh').groupby('filename', as_index=False).first()

deltas = ['d0', 'd1','d2','d3','d4']

print(mins_heur.head())

rollouts = DUtil.aggregate_results("rollout")
mins_roll = rollouts.sort_values('num_veh').groupby('filename', as_index=False).first()

print(mins_roll.head())


def matching_deltas(row_a, row_b):
    return row_a[4:9].equals(row_b[4:9])

res = []
for (_, row_a), (_, row_b) in zip(mins_roll.iterrows(), mins_heur.iterrows()):
    res.append(matching_deltas(row_a, row_b))

#print(list(mins.itertuples()))

#for m in mins.itertuples():
#    plt.plot(m[5:10])
#plt.show()


