
class Route():
    def __init__(self):
        self.route = []

    def append(self, item):
        self.route.append(item)

    def cost(self):
        return sum(i[0] for i in self.route)

    def __str__(self):
        s = self.cost() 
        a = '-'.join(str(i[1].custNo) for i in self.route)
        return "Distance: {0:.4g} {1}".format(s, a)

    def __repr__(self):
        return self.__str__() 

    def __getitem__(self, index):
        return self.route[index]

    def __setitem__(self,index,value):
        self.route[index] = value
