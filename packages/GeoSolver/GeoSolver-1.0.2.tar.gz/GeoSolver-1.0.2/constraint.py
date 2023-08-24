from .point import Point


class Constraint:
    def __init__(self):
        self.points = {}  # 存储点的坐标，格式为 {点编号: (x, y, z)}
        self.line_constraints = []  # 存储线长度约束，格式为 [{(点编号1, 点编号2): 长度}]
        self.angle_constraints = []  # 存储角度约束，格式为 [{(点编号1, 点编号2, 点编号3): 角度}]
        self.parallel_constraints = []  # 存储线平行约束，格式为 [{(点编号1, 点编号2, 点编号3, 点编号4)}]
        self.line_surface_angle_constraints = {}  # 存储线面角约束，格式为 {((线点编号1, 线点编号2), (面点编号1, 面点编号2, 面点编号3)): 目标角度}
        self.surface_surface_angle_constraints = {}  # 存储面面角约束，格式为 {((面1点编号1, 面1点编号2, 面1点编号3), (面2点编号1, 面2点编号2,
        # 面2点编号3)): 目标角度}
        self.area_constraints = {}  # 存储面积约束，格式为 {(点编号1, 点编号2, ..., 点编号N): 目标面积}
        self.symmetric_constraints = []  # 存储对称约束，格式为 {(点编号1, 点编号2):(对称线点1，点2), ...}

    def add_point(self, point_id, point: Point):
        self.points[point_id] = point

    def add_line_constraint(self, point_ids, length):
        constraint = {tuple(point_ids): length}
        self.line_constraints.append(constraint)

    def add_angle_constraint(self, point_ids, angle):
        constraint = {tuple(point_ids): angle}
        self.angle_constraints.append(constraint)

    def add_parallel_constraint(self, point_ids: list):  # 点1，2的线平行3，4的
        constraint = list(point_ids)
        self.parallel_constraints.append(constraint)

    def add_line_surface_angle_constraint(self, line_point_ids: list, surface_point_ids: list, target_angle):
        constraint = (
            (line_point_ids[0], line_point_ids[1]), (surface_point_ids[0], surface_point_ids[1], surface_point_ids[2]))
        self.line_surface_angle_constraints[constraint] = target_angle

    def add_surface_surface_angle_constraint(self, surface1_point_ids: list, surface2_point_ids: list, target_angle):
        constraint = ((surface1_point_ids[0], surface1_point_ids[1], surface1_point_ids[2]),
                      (surface2_point_ids[0], surface2_point_ids[1], surface2_point_ids[2]))
        self.surface_surface_angle_constraints[constraint] = target_angle

    def add_area_constraint(self, point_ids, target_area):
        constraint = tuple(point_ids)
        self.area_constraints[constraint] = target_area

    def add_symmetric_constraint(self, point1_id, point2_id, symmetry_line_point_ids: list):
        constraint = (point1_id, point2_id)
        self.symmetric_constraints[constraint] = symmetry_line_point_ids
