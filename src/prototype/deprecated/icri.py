
from src.prototype.generalizedCost import g
from src.model.SolomonProblem import Customer


import numpy as np
import pickle



class Route():
    service_time_min = 0
    service_time_max = 0
    def __init__(self):
        pass

class Vehicle():
    capacity_max = 0
    capacity_curr = 0
    def __init__(self):
        pass

class Service():
    customer = 0
    arrival_time = 0
    departure_time = 0
    service_time = 0    
    
    def __init__(self):
        pass

    def find_service_time(self, arrival_time):
        service_time = max(self.arrival_time, self.service_time[0])


def vehicleRoutingAlgorithm():
    pass

def main():
    print("Start using TDD")

if __name__ == "__main__":
    main()

