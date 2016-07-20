
class Validator():
    def __init__(self, sp, routes):
        self.sp = sp
        self.routes = routes

    def serviceTimesWithinWindow(self):
        print("Service times are within customer time window")
        success = 1
        for r in self.routes:
            for i in r:
                assert i.readyTime <= i.serviceTime() <= i.dueDate + i.serviceLen, \
                    "{} <= {} <= {}"\
                    .format(i.readyTime, i.serviceTime(), i.dueDate + i.serviceLen)
        return success

    def serviceTimesAscendingOrder(self):
        print("Service times are ascending ordered (except depot)")
        success = 1
        for r in self.routes:
            for i in range(1,len(r)-2):
                s, e = r[i], r[i+1]
                assert s.serviceTime() <= e.serviceTime(), \
                    "t {} for {} > t {} for {}"\
                    .format(s.serviceTime(), s.custNo, e.serviceTime(), e.custNo)
        return success

    def timelineRespected(self):
        print("Confirm timeline constraints held")
        return self.serviceTimesWithinWindow() and self.serviceTimesAscendingOrder()

    def capacityRespected(self):
        success = 1
        for route in self.routes:
            s = sum(c.demand for c in route)
            assert s <= self.sp.capacity
        return success

    def validate(self):
        return self.capacityRespected() and self.timelineRespected() 

