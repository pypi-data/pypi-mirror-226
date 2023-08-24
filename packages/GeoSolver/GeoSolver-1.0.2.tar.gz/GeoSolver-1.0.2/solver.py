import sympy as sp


class Solver:
    def __init__(self, constraint):
        self.constraint = constraint

    def solve(self):
        AllEquestions = []
        AllVariables = []

        for idx, point in self.constraint.points.items():
            AllEquestions += point.OnLine
            AllVariables.append(point.x)
            AllVariables.append(point.y)
            AllVariables.append(point.z)

        #result = []
        #out = []
        result = sp.solve(AllEquestions, AllVariables)
        if result == []:
            raise Exception("No solution found!")
        else:
            return result

        #for i in sp.solve(AllEquestions, AllVariables):
        #    result.append(i)
        #for idx, point in self.constraint.points.items():
        #    out.append({idx: result[i] for i in range(3 * (idx - 1), idx * 3)})
        #return out
        #return result
