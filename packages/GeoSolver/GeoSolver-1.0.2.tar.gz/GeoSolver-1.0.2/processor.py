import math
from .vector import Vec
from .surface import Surface


class Processor:
    def __init__(self, constraints):
        self.constraints = constraints
        self.Line_Solver(constraints.line_constraints)
        self.Angle_Solver(constraints.angle_constraints)
        self.Parallel_Solver(constraints.parallel_constraints)

    def Line_Solver(self, line_constraints):
        for line_constraint in line_constraints:  # 线长度约束，格式为 [{(点编号1, 点编号2): 长度}]
            for point_pair, len in line_constraint.items():
                self.constraints.points[point_pair[0]].OnLine.append(
                    Vec(self.constraints.points[point_pair[0]], self.constraints.points[point_pair[1]]).length() - len)
                self.constraints.points[point_pair[1]].OnLine.append(
                    Vec(self.constraints.points[point_pair[0]], self.constraints.points[point_pair[1]]).length() - len)

    def Angle_Solver(self, angle_constraints):
        for angle_constraint in angle_constraints:  # 角约束，格式为 [{(点编号1, 点编号2, 点编号3): 角度}]
            for point_pair, angle in angle_constraint.items():
                COS = math.cos(angle)
                V1 = Vec(self.constraints.points[point_pair[1]], self.constraints.points[point_pair[0]])
                V2 = Vec(self.constraints.points[point_pair[1]], self.constraints.points[point_pair[2]])
                # 计算夹角的余弦值
                cosine_angle = V1.dot(V2) / (V1.length() * V2.length())
                for point in point_pair:
                    self.constraints.points[point].OnLine.append(cosine_angle - COS)

    def Parallel_Solver(self, parallel_constraints):
        for parallel_constraint in parallel_constraints:  # 线平行约束，格式为 [{(点编号1, 点编号2, 点编号3, 点编号4)}]
            V1 = Vec(self.constraints.points[parallel_constraint[0]], self.constraints.points[parallel_constraint[1]])
            V2 = Vec(self.constraints.points[parallel_constraint[2]], self.constraints.points[parallel_constraint[3]])
            # 计算夹角的余弦值
            cosine_angle = V1.dot(V2) / (V1.length() * V2.length())
            for point in parallel_constraint:
                self.constraints.points[point].OnLine.append(cosine_angle ** 2 - 1)

    def Line_Surface_Solver(self, surface_constraints):  # 线面角约束，格式为 {((线点编号1, 线点编号2), (面点编号1, 面点编号2, 面点编号3)): 目标角度}
        for surface_constraint in surface_constraints:
            for point_pair, angle in surface_constraint.items():
                Line = Vec(self.constraints.points[point_pair[0][0]], self.constraints.points[point_pair[0][1]])
                V1 = Vec(self.constraints.points[point_pair[1][1]], self.constraints.points[point_pair[1][0]])
                V2 = Vec(self.constraints.points[point_pair[1][1]], self.constraints.points[point_pair[1][2]])
                surface = Surface(V1, V2)
                COS = math.cos(angle)
                cosine_angle = surface.line_surface_angle(Line)
                for point in point_pair[1]:
                    self.constraints.points[point].OnLine.append(cosine_angle - COS)
                for point in point_pair[0]:
                    self.constraints.points[point].OnLine.append(cosine_angle - COS)

    def Surface_Surface_Solver(self, surface_constraints):  # 面面角
        for surface_constraint in surface_constraints:
            for point_pair, angle in surface_constraint.items():
                V11 = Vec(self.constraints.points[point_pair[0][1]], self.constraints.points[point_pair[0][0]])
                V12 = Vec(self.constraints.points[point_pair[0][1]], self.constraints.points[point_pair[0][2]])
                surface1 = Surface(V11, V12)
                V21 = Vec(self.constraints.points[point_pair[1][1]], self.constraints.points[point_pair[1][0]])
                V22 = Vec(self.constraints.points[point_pair[1][1]], self.constraints.points[point_pair[1][2]])
                surface2 = Surface(V21, V22)
                COS = math.cos(angle)
                cosine_angle = surface1.surface_surface_angle(surface2)
                for point in point_pair[0]:
                    self.constraints.points[point].OnLine.append(cosine_angle - COS)
                for point in point_pair[1]:
                    self.constraints.points[point].OnLine.append(cosine_angle - COS)

    def Area_Solver(self, area_constraints):  # 面积
        for area_constraint in area_constraints:
            for point_pair, area in area_constraint.items():
                AREA = 0
                for i in range(1,len(point_pair)-1):
                    V1 = Vec(self.constraints.points[0], self.constraints.points[i])
                    V2 = Vec(self.constraints.points[0], self.constraints.points[i+1])
                    AREA += V1.cross(V2).length()/2
                for point in point_pair:
                    self.constraints.points[point].OnLine.append(AREA - area)

    def Symmetric_Solver(self,  symmetric_constraints):  # 对称性
        for symmetric_constraint in symmetric_constraints:
            for point_pair, symmetric_line in symmetric_constraint.items():
                V1 = self.constraints.points[point_pair[0]].get_perpendicular_vector(Vec(symmetric_line[0], symmetric_line[1]))
                V1 = V1.coordinate()
                self.constraints.points[point_pair[1]].OnLine.append(self.constraints.points[point_pair[1]].x - self.constraints.points[point_pair[0]].x - V1[0]*2)
                self.constraints.points[point_pair[1]].OnLine.append(self.constraints.points[point_pair[1]].y - self.constraints.points[point_pair[0]].y - V1[1]*2)
                self.constraints.points[point_pair[1]].OnLine.append(self.constraints.points[point_pair[1]].z - self.constraints.points[point_pair[0]].z - V1[2]*2)
                V2 = self.constraints.points[point_pair[1]].get_perpendicular_vector(Vec(symmetric_line[0], symmetric_line[1]))
                V2 = V2.coordinate()
                self.constraints.points[point_pair[0]].OnLine.append(self.constraints.points[point_pair[0]].x - self.constraints.points[point_pair[1]].x - V2[0]*2)
                self.constraints.points[point_pair[0]].OnLine.append(self.constraints.points[point_pair[0]].y - self.constraints.points[point_pair[1]].y - V2[1]*2)
                self.constraints.points[point_pair[0]].OnLine.append(self.constraints.points[point_pair[0]].z - self.constraints.points[point_pair[1]].z - V2[2]*2)