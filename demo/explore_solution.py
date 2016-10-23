from src import Cost, Utils

solution = Utils.open_sp("c109.p", root = "data/solutions/search/").solution

v0 = solution.vehicles[0]


num_cs = 0
cs = set()
for v in solution.vehicles:
    time = 0
    capacity = 0
    print("Next vehicle:")
    num_cs += len(v.customer_history)
    for ca,cb in zip(v.customer_history[:-1], v.customer_history[1:]):
        travel_time = Cost.euclidean_cust(ca.location, cb.location)
        time = max(cb.readyTime, time+travel_time)
        capacity += cb.demand
        print("({:03}->{:03}) t:{:06.2f}, cap:{:03} + {}.\
[{:03}, {:04}], -> {:05.2f}".format(\
            ca.custNo, cb.custNo, time, capacity, cb.demand, \
            cb.readyTime, cb.dueDate, travel_time))

        assert(time < cb.dueDate)
        cs.add(cb)
       
       
print(len(solution.vehicles))
print(num_cs)
print(cs)

