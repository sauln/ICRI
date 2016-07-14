



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


'''
objects:
Routes - an object of routes
 - this will keep our stack of routes
 - it will return a set of potentially free nodes
 - assume that when the next best addition is to not continue, we will
   attempt to continue on with this path in the future.

Routes::freeNodes() -> [Customers] 
    - all 
'''


class Routes():
    def __init__(self):
        self.rlist = []

    def freeNodes(self):#could be called `looseEnds` because they are still viable
        pass # return set of viable nodes


class Route():
    def __init__(self):
        self.route = []
        self.edges = []


    def append(self, item, cost):
        self.edges.append( ((self.route if len(self.route) > 0 else None, item), cost) )
        self.route.append(item)



    #def append(self, item):
    #    assert isinstance(item, Edge), "item is type {}:\n{}".format(type(item), item)
    #    self.route.append(item)

    def cost(self):
        return sum( cost for edge, cost in self.edges )
        #return sum(self.matrices.distMatrix(i,j) \
        #    for i, j in zip(self.route[:-1], self.route[1:]))
            
        #return sum( for i in self.route)

    def __str__(self):
        s = self.cost()
        a = ' => '.join(str(i) for i in self.route)
        #a = '-'.join(str(i.start.custNo) for i in self.route)
        return "Distance: {0:.4g} {1}".format(s, a)

    def __repr__(self):
        return "{:.4g}:({}, {})".format(self.cost(), self.route[0].custNo, self.route[-1].custNo) 

    def __getitem__(self, index):
        return self.route[index]

    def __setitem__(self,index,value):
        self.route[index] = value
