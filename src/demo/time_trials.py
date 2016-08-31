#  run the rollout algorithm on 25, 50, 75, 100, 125, 150, 175, 200

#  load r101, randomly choose 25 customers x10 times - run rollout
# -*- coding: utf-8 -*-
import logging
import time
import random 

import copy

import math

from collections import defaultdict

from src.data.make_dataset import DataBuilder
from src.main.BaseObjects.Dispatch import Dispatch
from src.main.BaseObjects.Parameters import Parameters
from src.main.Algorithms.RollOut   import RollOut 
from src.main.BaseObjects.Customer import Customer, Point


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

def tweak(customer, index):
    demand = customer.demand + random.randrange(-10, 10)
    x = customer.location.x + random.randrange(-10, 10)
    y = customer.location.y + random.randrange(-10, 10)

    ## insure that we can get to this customer
    diff = math.sqrt(x*x + y*y)
    c_time = random.randrange(-30, 30)
    if c_time < 0:
        readyTime = max(diff, customer.readyTime + c_time)
        dueDate = max(diff+10, customer.dueDate + c_time)
    else:
        readyTime = min(220, customer.readyTime + c_time)
        dueDate = min(230, customer.readyTime + c_time)
    
    return Customer(index, Point(x,y), demand, readyTime, dueDate, 10)

def build_random_customers(base_customers, n):
    base = copy.deepcopy(base_customers)
    base2 = copy.deepcopy(base_customers)
    new_bases = random.sample(base, n - len(base))
    modded_new = [tweak(c, i + len(base) + 1) for i, c in enumerate(new_bases)]
    
    return base2 + modded_new

def get_customers(customers, n):
    if len(customers) > n:
        logger.debug("Randomly sample {} customers".format(n))
        cs = copy.deepcopy(random.sample(customers, n))
        for i, c in enumerate(cs):
            c.custNo = i+1
        return cs
    elif len(customers) == n:
        logger.debug("Return list of {} customers".format(n))
        return copy.deepcopy(customers)
    else:
        logger.debug("Generate {} new customers to make {}".format(n - len(customers), n))
        return copy.deepcopy(build_random_customers(customers, n))


def configure_test(base_sp):
    base_customers = list(base_sp.customers[1:])
    depot = base_sp.customers[0]

    base_len = len(base_customers)
    num_each = 3

    for n in [25, 50, 75, 100, 150, 200]:
        for i in range(num_each):
            customers = get_customers(base_customers, n)
            logger.info("Run for {} customers".format(len(customers)))
            base_sp.customers = [depot] + customers
            yield base_sp


for sp in configure_test(base_sp):
    num_custs, len_time = run_test(sp)
    results[num_custs].append(len_time)

    print(results)

