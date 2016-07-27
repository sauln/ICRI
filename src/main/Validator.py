
class Validator():
    def __init__(self, sp, routes):
        self.sp = sp
        self.routes = routes

    def serviceTimesWithinWindow(self):
        print("\nService times are within customer time window")
        success = 1
        for r in self.routes:
            #print("Start route {}".format(r))
            total = 0
            for i in range(0,len(r)-1):
                td = self.routes.sp.timeMatrix[r[i].custNo,r[i+1].custNo]
                #print("Travel between {}({},{}) and {}({},{}) is {}".format(\
                #    r[i].custNo, r[i].readyTime, r[i].dueDate, \
                #    r[i+1].custNo, r[i+1].readyTime, r[i+1].dueDate, td)) 
                #total += td
                srv = max(total + td, r[i+1].readyTime)
                #print("  arrive {}".format(total + td))
                #print("  service {} -> {}".format(srv, srv + r[i+1].serviceLen))
                total = srv + r[i+1].serviceLen
                 
                
                #assert i.readyTime <= i.serviceTime() <= i.dueDate + i.serviceLen, \
                #    "{} <= {} <= {}"\
                #    .format(i.readyTime, i.serviceTime(), i.dueDate + i.serviceLen)
            #print("End route")

        #print(self.routes.sp.timeMatrix[0,:])
        return success

    def timelineRespected(self):
        print("Confirm timeline constraints held")
        return self.serviceTimesWithinWindow() 

    def capacityRespected(self):
        success = 1
        for route in self.routes:
            s = sum(c.demand for c in route)
            assert s <= self.sp.capacity
        return success

    def validate(self):
        return self.capacityRespected() and self.timelineRespected() 

