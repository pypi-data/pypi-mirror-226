class Surface:
    def __init__(self, VecA, VecB):
        self.VecA = VecA
        self.VecB = VecB
        self.normalVector = VecA.cross(VecB)

    def line_surface_angle(self, line):
        V1 = self.normalVector
        V2 = line
        sine_angle = V1.dot(V2) / (V1.length() * V2.length())
        cosine_angle = (1 - sine_angle ** 2)**0.5
        return cosine_angle

    def surface_surface_angle(self, surface):
        V1 = self.normalVector
        V2 = surface.normalVector
        cosine_angle = V1.dot(V2) / (V1.length() * V2.length())
        return cosine_angle

