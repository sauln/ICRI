class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and \
               self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))
    def __str__(self):
        return "({},{})".format(self.x, self.y)
    def __repr__(self):
        return self.__str__()

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
        return "ID: {} t.({:3},{:3}) d.({:3}, {:3})".format(\
            self.custNo, self.readyTime, self.dueDate, self.location.x, self.location.y)

    def __hash__(self):
        return self.custNo

    def __repr__(self):
        return "c{}".format(self.custNo)

    def __eq__(self, other):
        # There are a lot of these calls.  why so much?
        return self.custNo == other.custNo and \
               self.location  == other.location  and \
               self.demand  == other.demand  and \
               self.readyTime == other.readyTime and \
               self.dueDate == other.dueDate and \
               self.serviceLen == other.serviceLen

