class Vehicle():
    def __init__(self, sp, *seed):
        self.depot = seed[0]
        self.maxCapacity = sp.capacity
        self.timeMatrix = sp.timeMatrix
        self.curCapacity = 0
        self.distTravel = 0
        self.customers = []
        self._lastServiceTime = 0
        self._lastArrivalTime = 0
        
        for s in seed:
            self.append(s)

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
        assert self.customers[index] == None

        self.customers[index] = value
        self.curCapacity += value.demand
    
    def __len__(self):
        return len(self.customers)


    #def lastServiceTime(self, customer):
    #    #the actual time a customer was serviced if not depot
    #    return (max(self._arrivalTime, self.readyTime), 0)[self.custNo == 0]

    def lastCustomer(self):
        return self.customers[-1] 

    def lastServiceTime(self):
        return self._lastServiceTime 

    def departureTime(self):
        return self._lastServiceTime + self.lastCustomer().serviceLen

    def nextServiceTime(self, customer):
        return 0 

    def setLastServiceTime(self, customer):
        self._lastServiceTime = max(self._lastArrivalTime, customer.readyTime)

    def setLastArrivalTime(self, customer):
        # use the actual timeTravel matrix
        
        if(len(self.customers) > 0):
            last = self.customers[-1]
        else:
            last = self.depot

        travelTime = self.timeMatrix[last.custNo, customer.custNo]
        
        self._lastArrivalTime = self._lastServiceTime + last.serviceLen + travelTime


    # want to move away from having the customers keep track of their service time
    # imagine the vehicle keeps a ledger
    def append(self, item):
        #if len(self.customers) >= 1:
        #    item.setArrivalTime(self.customers[-1] )
        #else:
        #    item._arrivalTime = 0
        
        # ensure we're not adding a bad node
        assert self.curCapacity + item.demand <= self.maxCapacity, \
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

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Serviced:{} => {}".format(len(self.customers), self.customers)

