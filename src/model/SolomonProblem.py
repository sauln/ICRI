
class SolomonProblem():
    def __init__(self, name, numVeh, capacity, customers):
        self.problemName     = name
        self.numVehicles     = numVeh
        self.capacity        = capacity
        self.customers       = customers

    def __str__(self):
        return "{} Num Vehicles: {}  Capacity: {}  Num Customers: {}".\
            format(self.problemName,self.numVehicles,self.capacity,len(self.customers))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (self.problemName == other.problemName) and \
               (self.numVehicles == other.numVehicles) and \
               (self.capacity == other.capacity) and \
               (self.customers == other.customers)


class Customer():
    #todo: change these to camel case
    def __init__(self, custNo, xcoord, ycoord, demand, readyTime, dueDate, serviceLen):
        self.custNo       = custNo
        self.xcoord       = xcoord
        self.ycoord       = ycoord
        self.demand       = demand
        self.readyTime    = readyTime
        self.dueDate      = dueDate
        self.serviceLen   = serviceLen

        self.serviceTime = 0 # will the be actual time this customer was serviced



    def __str__(self):
        return "ID: {:3}  x.({:3},{:3}) Service: {}".\
            format(self.custNo, self.xcoord, self.ycoord, self.serviceTime)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.custNo == other.custNo and \
               self.xcoord  == other.xcoord  and \
               self.ycoord  == other.ycoord  and \
               self.demand  == other.demand  and \
               self.readyTime == other.readyTime and \
               self.dueDate == other.dueDate and \
               self.serviceLen == other.serviceLen
