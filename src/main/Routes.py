class Routes():
    def __init__(self, start):
        self.rList = [[start]] 

    def cost(self):
        # cost function of route set
        return 1

    def __str__(self):
        return "Number of routes: {}\n".format(len(self.rList)) +\
            "\n".join("{}".format(r) for r in self.rList)
    
