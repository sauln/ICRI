
class Solution:
    def __init__(self, num_vehicles, total_distance, params, solution, name=None):
        self.num_vehicles = num_vehicles
        self.total_distance = total_distance
        self.params = params
        self.solution = solution
        self.name = name
        self.pre_solution = None


    def __repr__(self):
        return "{}({}, {}): {}".format(self.name, self.num_vehicles, self.total_distance, self.params)

