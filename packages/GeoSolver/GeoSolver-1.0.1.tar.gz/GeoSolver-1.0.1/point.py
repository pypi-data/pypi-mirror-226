import sympy as sp


class Point:
    count = 0

    def __init__(self, x=None, y=None, z=None):
        Point.count += 1
        self.local_var = Point.count
        self.x = sp.Symbol('x' + str(self.local_var))
        self.y = sp.Symbol('y' + str(self.local_var))
        self.z = sp.Symbol('z' + str(self.local_var))
        self.OnLine = []  # 点所在的直线（求解用）
        if x is not None:
            self.OnLine.append("x" + str(self.local_var) + "- " + str(x))
        if y is not None:
            self.OnLine.append("y" + str(self.local_var) + "- " + str(y))
        if z is not None:
            self.OnLine.append("z" + str(self.local_var) + "- " + str(z))

    def fit(self):
        out = []
        for i in sp.solve(self.OnLine, [self.x, self.y, self.z]).values():
            out.append(i)
        return out

    def get_perpendicular_vector(self, vector):
        # 计算向量的法向量方向
        normal_direction = vector.cross(Vec(Point(0, 0, 0), Point(1, 0, 0)))

        # 创建垂直向量的终点坐标
        perpendicular_end_x = self.x + normal_direction.coordinate()[0]
        perpendicular_end_y = self.y + normal_direction.coordinate()[1]
        perpendicular_end_z = self.z + normal_direction.coordinate()[2]

        # 创建垂直向量的终点
        perpendicular_end = Point(perpendicular_end_x, perpendicular_end_y, perpendicular_end_z)

        # 创建垂直向量对象并返回
        perpendicular_vector = Vec(self, perpendicular_end)
        return perpendicular_vector

