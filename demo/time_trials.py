#  run the rollout algorithm on 25, 50, 75, 100, 125, 150, 175, 200

#  load r101, randomly choose 25 customers x10 times - run rollout
# -*- coding: utf-8 -*-
import logging
import time

from collections import defaultdict

from src.data.make_dataset import DataBuilder
from src.main.BaseObjects.Dispatch import Dispatch
from src.main.BaseObjects.Parameters import Parameters
from src.main.Algorithms.RollOut   import RollOut 

from src.demo.Problem_builder import get_customers 

logger = logging.getLogger(__name__)
log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)

logger.info("Running time tests")
problem_number = "r101"
input_filepath = "data/raw/{}.txt".format(problem_number)
output_filepath = "data/interim/{}.p".format(problem_number)
intermediate_filepath = "data/interim/solution_{}.p".format(problem_number)


base_sp = DataBuilder(input_filepath, output_filepath).problem
Parameters().build(base_sp, 10, 10)

logger.info('Setup Parameters and Dispatch')

def run_test(sp):
    Parameters().build(sp, 10, 10)
    customers = list(sp.customers[1:])
    depot = sp.customers[0]
    num_customers = len(customers)
    
    t0 = time.clock()
    dispatch = Dispatch(customers, depot)
    solution = RollOut().run(dispatch)
    t1 = time.clock()
    total_t = t1 - t0
    return (num_customers, total_t)

results = defaultdict(list)

def configure_test(base_sp):
    base_customers = list(base_sp.customers[1:])
    depot = base_sp.customers[0]

    base_len = len(base_customers)
    num_each = 3

    for n in [150, 200]:
        for i in range(num_each):
            customers = get_customers(base_customers, n)
            logger.info("Run for {} customers".format(len(customers)))
            base_sp.customers = [depot] + customers
            yield base_sp

for sp in configure_test(base_sp):
    num_custs, len_time = run_test(sp)
    results[num_custs].append(len_time)

    print(results)

