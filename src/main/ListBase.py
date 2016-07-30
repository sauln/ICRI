
class ListBase():
    def __init__(self):
        self.objList = []
    
    def __getitem__(self, index):
        return self.objList[index]

    def __setitem__(self, index, value):
        #assert type(value) == Customer, "Cannot add type {} to route".format(type(value))
        assert self.objList[index] == None, \
            "the customer at {} is {}".format(index, self.objList[index])
        self.objList[index] = value
        #self.curCapacity += value.demand

    def pop(self, index = -1):
        return self.objList.pop(index) 
    
    def __len__(self):
        return len(self.objList)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Len:{}:{}".format(len(self.objList), self.objList)

    def last(self):
        if (len(self.objList) > 0):
            return self.objList[-1]

