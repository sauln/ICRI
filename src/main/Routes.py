from src.main.SolomonProblem import Customer, SolomonProblem

class Route():
    def __init__(self, parent, *seed):
        assert type(parent) == SolomonProblem, "Need to supply SolomonProblem to Route init"
        self.maxCapacity = parent.capacity
       
        
        self.capacity = 0
        self.r = []
        for s in seed:
            self.append(s)

    def __getitem__(self, index):
        return self.r[index]

    def __setitem__(self, index, value):
        #print("adding {} at {}.  capacity {} -> {}".format(value, index, self.capacity, self.capacity+value.demand))
        
        assert type(value) == Customer, "Cannot add type {} to route".format(type(value))
        a = self.r[index]
        #if(a):
        #    self.capacity -= a.demand
        self.r[index] = value
        #self.capacity += value.demand

    def append(self, item):
        #print(item)
        # needs to add the serviceTime to the customer
        assert self.capacity + item.demand <= self.maxCapacity, \
            "Not enough room for this node"
        
        if(len(self.r)>1):
            item.setArrivalTime(self.r[-1])
        
        self.capacity += item.demand
        self.r.append(item)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Cap:{} => {}".format(self.capacity, self.r)



class Routes():
    def __init__(self, start):
        r = Route(start)
        self.rList = [r] 

    def cost(self):
        # cost function of route set
        return 1

    def __getitem__(self, index):
        return self.rList[index]

    def __setitem__(self, index, value):
        assert isinstance(value, Route), "Adding route to Routes that isnt Route"
        self.route[index] = value

    def __str__(self):
        return "Number of routes: {}\n{}".format(len(self.rList), self.rList)
    
