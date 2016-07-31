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

    def __str__(self):
        return "ID: {}({}) d.({:3},{:3}) t.({:3},{:3})+{}".\
            format(self.custNo, self.demand, \
                   self.xcoord, self.ycoord, \
                   self.readyTime, self.dueDate, self.serviceLen)

    def __hash__(self):
        return self.custNo

    def __repr__(self):
        return "c{}".format(self.custNo)

    def __eq__(self, other):
        return other is not None and self.custNo == other.custNo and \
                       self.xcoord  == other.xcoord  and \
                       self.ycoord  == other.ycoord  and \
                       self.demand  == other.demand  and \
                       self.readyTime == other.readyTime and \
                       self.dueDate == other.dueDate and \
                       self.serviceLen == other.serviceLen

