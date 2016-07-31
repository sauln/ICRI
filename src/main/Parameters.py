
class Parameters:
    class __Parameters:
        def __init__(self):
            self.problemSet = None

        def __str__(self):
            return repr(self.problemSet)

        def __getattr__(self, name):
            return getattr(self.problemSet, name)

    instance = None
    def __new__(cls):
        if not Parameters.instance:
            Parameters.instance = Parameters.__Parameters()
        return Parameters.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr(self, name):
        return setattr(self.instance, name)

