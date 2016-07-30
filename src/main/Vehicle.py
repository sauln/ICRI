from src.main.Customer import Customer
from src.main.Matrices import Matrices

class ListBase():
    ''' I just wanted to get these functions out of the way  '''
    def __init__(self):
        self.customers = []
        self.curCapacity = 0
    
    def __getitem__(self, index):
        return self.customers[index]

    def __setitem__(self, index, value):
        assert type(value) == Customer, "Cannot add type {} to route".format(type(value))
        assert self.customers[index] == None, \
            "the customer at {} is {}".format(index, self.customers[index])
        self.customers[index] = value
        self.curCapacity += value.demand
    
    def __len__(self):
        return len(self.customers)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Len:{}:{}".format(len(self.customers), self.customers)

class Vehicle(ListBase):
    def __init__(self, sp, *seed):
        super(Vehicle, self).__init__()
        self.curCapacity, self.distTravel, self.totalSlack, self.totalTime = 0,0,0,0
        self.depot = seed[0]
        self.maxCapacity = sp.capacity
        for s in seed:
            self.append(s)

    def travelDistance(self):
        tot = 0
        for i in range(len(self.customers)-1):
            tot += Matrices().timeMatrix[self.customers[i].custNo, \
                                         self.customers[i+1].custNo]
        return tot

    def isNotFull(self, end):
        return self.maxCapacity >= end.demand + self.curCapacity

    def isValidTime(self, end):
        # does the entire operation need to be done before the due date?
        travelTime = Matrices().timeMatrix[self.lastCustomer().custNo, end.custNo]
        return self.totalTime + travelTime <= end.dueDate

    def isFeasible(self, end):
        return (self.isValidTime(end) and self.isNotFull(end))

    def lastCustomer(self):
        # should this be a better method of try/catch?
        if(len(self.customers) > 0):
            return self.customers[-1] 

    def update(self, item):
        travelTime = Matrices().timeMatrix[self.customers[-1].custNo, item.custNo]
        arrivalTime = self.totalTime + travelTime
        srv = max(arrivalTime, item.readyTime)
        slackTime = srv - arrivalTime
        self.totalSlack += slackTime
        self.totalTime = srv + item.serviceLen
        self.curCapacity += item.demand

    def append(self, item):
        assert type(item) == Customer, "Cannot add type {} to route".format(type(value))
        if(item.custNo is not 0 and self.__len__() != 0): #not depot and not first item
            assert self.isFeasible(item), "Item {} is not feasible".format(item)
            self.update(item)
        self.customers.append(item)

