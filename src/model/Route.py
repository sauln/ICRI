class Node():
    def __init__(self, start, end, cost):
        self.start = start
        self.end   = end
        self.cost  = cost

    def __str__(self):
        return "Node: ({}, {})+{}".format(self.start, self.end, self.cost)



class Route():
    def __init__(self):
        self.route = []

    def append(self, item):
        assert isinstance(item, Node), "item is type {}:\n{}".format(type(item), item)
        self.route.append(item)

    def cost(self):
        return sum(i.cost for i in self.route)

    def __str__(self):
        s = self.cost() 
        a = '-'.join(str(i.start.custNo) for i in self.route)
        return "Distance: {0:.4g} {1}".format(s, a)

    def __repr__(self):
        return self.__str__() 

    def __getitem__(self, index):
        return self.route[index]

    def __setitem__(self,index,value):
        self.route[index] = value
