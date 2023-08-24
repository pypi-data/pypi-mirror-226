# GeoSolver Doc

## Introduction

This is a library for solving three-dimensional 
geometric constraints. Built on top of Sympy, 
it enables the definition of `Constraint`, processing 
with a `Processor`, and invocation of a `Solver` for solution.

## Table of Contents

- [Point](#Point)
- [Vector](#Vector)
- [Surface](#Surface)
## Point


```
from GeoSolver.Point

A = Point(x=None,y=None,z=None) #Indeterminate Point(None can omit)
A = Point(x=1) #Point with Specified x Value
A = Point(x=1,y=2,z=3) #Fixed Point

A.x #X value
A.fit() #Show coordinate
```

## Vector
```
from GeoSolver.Point
from GeoSolver.Vec


A = Point(x=1,y=2,z=3) 
B = Point(x=2,y=3,z=4) 

V = Vec(A,B) #Define a vector
V.length() #length
V.coordinate() #(1,1,1)
V.dot(V1) #dot product
V.cross(V1) #cross product
```

## Surface
```
from GeoSolver.Vec
V1 = ...
V2 = ...
V3 = ...

from GeoSolver.Surface

S = Surface(V1, V2) #Use two vectors to define a surface
S.line_surface_angle(V3) 

S2 = ...
S.surface_surface_angle(S2)
```

## Solve

```
from point import Point
from constraint import Constraint
from processor import Processor
from solver import Solver


Constraint = Constraint()
solver = Solver(Constraint)

# Add Point and Constraint
Constraint.add_point(0, Point(0, 0, 0))
Constraint.add_point(1, Point(1, 0, 0))
Constraint.add_point(2, Point(z=0))

Constraint.add_line_constraint([0, 1], 1)
Constraint.add_line_constraint([0, 2], 1)
Constraint.add_line_constraint([1, 2], 1)
# Process
Processor(Constraint)


print(solver.solve())
```

### constraints
#### add_line_constraint(point_ids, length)
#### add_angle_constraint(point_ids, angle)
#### add_parallel_constraint(point_ids: list):  # point 1，2 parallel with 3，4
#### add_line_surface_angle_constraint(line_point_ids: list, surface_point_ids: list, target_angle)
#### add_surface_surface_angle_constraint(surface1_point_ids: list, surface2_point_ids: list, target_angle)
#### add_area_constraint(point_ids, target_area)
#### add_symmetric_constraint(point1_id, point2_id, symmetry_line_point_ids: list)
 