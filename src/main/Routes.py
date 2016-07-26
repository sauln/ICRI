import numpy as np

from src.main.SolomonProblem import SolomonProblem
from src.main.Customer import Customer
from src.main.Vehicle import Vehicle


class Routes():
    def __init__(self, sp, start, depot):
        self.sp = sp
        v = Vehicle(sp, start)
        self.depot = depot
        #r = Route(sp, depot)
        self.vList = [v]
        
    def cost(self):
        total = sum(r.travelDistance() for r in self.vList)
        return total

    def pop(self, index = -1):
        return self.vList.pop(index) 

    def __getitem__(self, index):
        return self.vList[index]

    #def __setitem__(self, index, value):
    #    assert isinstance(value, Route), "Adding route to Routes that isnt Route"
    #    self.route[index] = value

    def __str__(self):
        return "Number of routes: {}\n{}".format(len(self.vList), self.vList)
    
    def __repr__(self):
        return self.__str__()

    """ Route building """
    def addNext(self, vehicle, end):
        if(vehicle[-1].custNo == 0): #the depot
            nv = Vehicle(self.sp, self.depot, end)
            self.vList.append(nv)
        else:
            vehicle.append(end)

    def __len__(self):
        return len(self.vList)

    def finish(self):
        if(len(self.vList[0]) == 1): # remove our place holder depot route
            self.vList.pop(0)

        for v in self.vList: # add depot to end of each route 
            v.append(self.depot)



