#this is actual an edge... wtf
class Edge():
    def __init__(self, start, end, cost):
        self.start = start
        self.end   = end
        self.cost  = cost

    def __str__(self):
        return "({}, {}+{:.3g})".format(self.start.custNo, self.end.custNo, self.cost)

    def __repr__(self):
        return self.__str__()


class Route():
    def __init__(self):
        self.route = []

    def append(self, item):
        assert isinstance(item, Edge), "item is type {}:\n{}".format(type(item), item)
        self.route.append(item)

    def cost(self):
        return sum(i.cost for i in self.route)

    def __str__(self):
        s = self.cost()
        a = ' => '.join(str(i) for i in self.route)
        #a = '-'.join(str(i.start.custNo) for i in self.route)
        return "Distance: {0:.4g} {1}".format(s, a)

    def __repr__(self):
        return "{:.4g}:({}, {})".format(self.cost(), self.route[0].start.custNo, self.route[-1].end.custNo) 

    def __getitem__(self, index):
        return self.route[index]

    def __setitem__(self,index,value):
        self.route[index] = value
