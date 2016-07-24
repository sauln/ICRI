class Vehicle():
    maxCapacity = 0
    curCapacity = 0
    distTravel = 0
    customers = []

    def __init__(self, sp, *seed):

        print("Init vehicle: seed: {}".format(seed))
        for s in seed:
            self.customers.append(s)
        self.depot = seed[0]
        self.maxCapacity = sp.capacity
        self.timeMatrix = sp.timeMatrix

    def lastCustomer(self):
        return self.customers[-1] 

    def lastServiceTime(self):
        return self.customers[-1].serviceTime()

    def isNotFull(self, end):
        return self.maxCapacity >= end.demand + self.curCapacity

    def isValidTime(self, end):
        # does the entire operation need to be done before the due date?
        travelTime = self.timeMatrix[self.lastCustomer().custNo, end.custNo]
        earliest = self.lastServiceTime() + travelTime #+ end.serviceLen 
        latest = end.dueDate
        return earliest <= latest

    def isFeasible(self, end):
        return (self.isValidTime(end) and self.isNotFull(end))

    def __getitem__(self, index):
        return self.customers[index]

    def __setitem__(self, index, value):
        assert type(value) == Customer, "Cannot add type {} to route".format(type(value))
       
        # if we are replacing, then fix the capacity
        a = self.customers[index]
        if(a):
            self.curCapacity -= a.demand
        
        self.customers[index] = value
        self.curCapacity += value.demand
    
    def __len__(self):
        return len(self.customers)


    #def lastServiceTime(self, customer):
    #    #the actual time a customer was serviced if not depot
    #    return (max(self._arrivalTime, self.readyTime), 0)[self.custNo == 0]


    def nextServiceTime(self, customer)
        return 

    def setLastServiceTime(self, customer):
        self._lastServiceTime = max(self._lastArrivalTime, customer.readyTime)

    def setArrivalTime(self, customer):
        # use the actual timeTravel matrix
        last = self.customers[-1]

        travelTime = self.timeMatrix(last.custNo, customer.custNo)
        
        self._lastArrivalTime = self._lastServiceTime + last.serviceLen + travelTime


    # want to move away from having the customers keep track of their service time
    # imagine the vehicle keeps a ledger
    def append(self, item):
        #if len(self.customers) >= 1:
        #    item.setArrivalTime(self.customers[-1] )
        #else:
        #    item._arrivalTime = 0
        
        # ensure we're not adding a bad node
        assert self.capacity + item.demand <= self.maxCapacity, \
            "Not enough room for this node"
       
        # ensure serviceTime is within the correct window, except for depot
        #if(item.custNo != 0):
        #  correct time window is 
        #       nextServiceTime in [item.readyTime, item.dueDate] AND
        #       
        
        #assert item.readyTime <= self.nextServiceTime() <= item.dueDate + item.serviceLen,\
        #    "{} <= {} <= {}"\
        #    .format(item.readyTime, item.serviceTime(), item.dueDate + item.serviceLen)

        self.setLastArrivalTime(item) # order of these matters
        self.setLastServiceTime(item)

        self.curCapacity += item.demand
        self.customers.append(item)


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


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "len:{} => {}".format(len(self.r), self.r)
