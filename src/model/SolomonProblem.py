
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

    def __eq__(self, other):
        return (self.problem_name == other.problem_name) and \
               (self.number_vehicles == other.number_vehicles) and \
               (self.capacity == other.capacity) and \
               (self.customers == other.customers)


class Customer():
    def __init__(self, cust_no, xcoord, ycoord, demand, ready_time, due_date, service_len):
        self.cust_no      = cust_no
        self.xcoord       = xcoord
        self.ycoord       = ycoord
        self.demand       = demand
        self.ready_time   = ready_time
        self.due_date     = due_date
        self.service_len  = service_len
   
    def __str__(self):
        return "ID: {:3}  x.({:3},{:3}) t.({:3},{:3})".\
            format(self.cust_no, self.xcoord, self.ycoord, self.ready_time, self.due_date)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.cust_no == other.cust_no and \
               self.xcoord  == other.xcoord  and \
               self.ycoord  == other.ycoord  and \
               self.demand  == other.demand  and \
               self.ready_time == other.ready_time and \
               self.due_date == other.due_date and \
               self.service_len == other.service_len
