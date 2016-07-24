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

        self._serviceTime = 0 # time this customer was serviced
        self._arrivalTime = 0 # time route arrived at this customer

    def __str__(self):
        return "ID: {:3}({}) t.({:3},{:3})+{}".\
            format(self.custNo, self.demand, \
                   self.readyTime, self.dueDate, self.serviceLen)

    def __repr__(self):
        return "c{}".format(self.custNo)

    def __eq__(self, other):
        return self.custNo == other.custNo and \
               self.xcoord  == other.xcoord  and \
               self.ycoord  == other.ycoord  and \
               self.demand  == other.demand  and \
               self.readyTime == other.readyTime and \
               self.dueDate == other.dueDate and \
               self.serviceLen == other.serviceLen

