class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Customer():
    #todo: change these to camel case
    def __init__(self, custNo, location, demand, readyTime, dueDate, serviceLen):
        self.custNo       = custNo
        self.location     = location
        self.demand       = demand
        self.readyTime    = readyTime
        self.dueDate      = dueDate
        self.serviceLen   = serviceLen

    def __str__(self):
        return "ID: {} t.({:3},{:3})".\
            format(self.custNo, self.readyTime, self.dueDate)

    def __hash__(self):
        return self.custNo

    def __repr__(self):
        return "c{}".format(self.custNo)

    def __eq__(self, other):
        return other is not None and self.custNo == other.custNo and \
                       self.location  == other.location  and \
                       self.demand  == other.demand  and \
                       self.readyTime == other.readyTime and \
                       self.dueDate == other.dueDate and \
                       self.serviceLen == other.serviceLen

