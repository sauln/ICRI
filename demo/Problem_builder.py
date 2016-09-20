import copy
import random
import math
import logging

from src.main.BaseObjects.Customer import Customer, Point

logger = logging.getLogger(__name__)
log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)

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

