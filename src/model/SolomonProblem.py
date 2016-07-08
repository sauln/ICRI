

class SolomonProblem():
    def __init__(self, name, num_veh, capacity, customers):
        self.problem_name    = name
        self.number_vehicles = num_veh
        self.capacity        = capacity
        self.customers       = customers

    def __str__(self):
        return "{} Num Vehicles: {}  Capacity: {}  Num Customers: {}".\
            format(self.problem_name,self.number_vehicles,self.capacity,len(self.customers))

    def __repr__(self):
        return self.__str__()


class Customer():
    def __init__(self, cust_no, xcoord, ycoord, demand, ready_time, due_date, service_time):
        self.cust_no      = cust_no
        self.xcoord       = xcoord
        self.ycoord       = ycoord
        self.demand       = demand
        self.ready_time   = ready_time
        self.due_date     = due_date
        self.service_time = service_time
   
    def __str__(self):
        return "ID: {:3}  x.({:3},{:3}) t.({:3},{:3})".\
            format(self.cust_no, self.xcoord, self.ycoord, self.ready_time, self.due_date)

    def __repr__(self):
        return self.__str__()


