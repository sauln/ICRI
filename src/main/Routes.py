import numpy as np

from src.main.SolomonProblem import Customer, SolomonProblem

class Route():
    def __init__(self, parent, *seed):
        assert type(parent) == SolomonProblem, "Need to supply SolomonProblem to Route init"
        self.maxCapacity = parent.capacity
       
        self.capacity = 0
        self.r = []
        for s in seed:
            self.append(s)

    def travelDistance(self):
        total = 0
        for i in range(len(self.r)-1):
            s, e = self.r[i], self.r[i+1]
            total += np.sqrt( (s.xcoord - e.xcoord)**2 + (s.ycoord - e.ycoord)**2)
        return total

    def __getitem__(self, index):
        return self.r[index]

    def __setitem__(self, index, value):
        assert type(value) == Customer, "Cannot add type {} to route".format(type(value))
       
        # if we are replacing, then fix the capacity
        a = self.r[index]
        if(a):
            self.capacity -= a.demand
        
        self.r[index] = value
        self.capacity += value.demand
    
    def __len__(self):
        return len(self.r)

    def append(self, item):
        prev =  self.r[-1] if len(self.r) >= 1 else item
        item.setArrivalTime(prev)
        
        # ensure we're not adding a bad node
        assert self.capacity + item.demand <= self.maxCapacity, \
            "Not enough room for this node"
       
        # ensure serviceTime is within the correct window, except for depot
        #if(item.custNo != 0):
        assert item.readyTime <= item.serviceTime() <= item.dueDate + item.serviceLen,\
            "{} <= {} <= {}"\
            .format(item.readyTime, item.serviceTime(), item.dueDate + item.serviceLen)


        self.capacity += item.demand
        self.r.append(item)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "len:{} => {}".format(len(self.r), self.r)

class Routes():
    def __init__(self, sp, depot, start = None):
        r = Route(sp, depot)
        self.rList = [r] 
        
        if start:
            self.rList.append(Route(sp, depot, start))

    def cost(self):
        total = sum(r.travelDistance() for r in self.rList)
        return total

    def pop(self, index = -1):
        return self.rList.pop(index) 

    def __getitem__(self, index):
        return self.rList[index]

    def __setitem__(self, index, value):
        assert isinstance(value, Route), "Adding route to Routes that isnt Route"
        self.route[index] = value

    def __str__(self):
        return "Number of routes: {}\n{}".format(len(self.rList), self.rList)
    
    def __repr__(self):
        return self.__str__()


    def __len__(self):
        return len(self.rList)
