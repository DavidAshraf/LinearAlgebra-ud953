__author__ = 'David'

from math import  sqrt ,acos,pi
from decimal import  Decimal,getcontext

getcontext().prec = 30

class Vector(object):
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG='Cannot Normalize Zero Vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG='No Unique Parallel Component'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG='No Unique Orthogonal Component'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(Decimal(x) for x in coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, v):
        new_coordinates=[x+y for x,y in zip(self.coordinates,v.coordinates)]
        return Vector(new_coordinates)

    def __sub__(self, v):
        new_coordinates=[x-y for x,y in zip(self.coordinates,v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self,c):
        new_coordinates=[c*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        magnitude=sqrt(sum(coordinates_squared))
        return magnitude

    def normalized(self):
        try:
            magnitude=self.magnitude()
            return self.times_scalar(Decimal('1.0')/magnitude)

        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot(self,v):
        return sum([x*y for x,y in zip(self.coordinates,v.coordinates)])

    def angle_with(self,v,in_degrees=False):
        try:
            u1=self.normalized()
            u2=v.normalized()
            angle_in_radians=acos(u1.dot(u2))

            if in_degrees:
                degrees_per_radian=180./pi
                return angle_in_radians*degrees_per_radian
            else:
                return angle_in_radians

        except Exception as e:
            if str(e)==self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot Compute Angle with zero vector')
            else:
                raise e

    def is_zero(self,tolerance=1e-10):
        return self.magnitude()<tolerance

    def is_orthogonal_to(self,v,tolerance=1e-10):
        return abs(self.dot(v))<tolerance

    def is_parallel_to(self,v):
        return self.is_zero() or v.is_zero() or self.angle_with(v)==0 or self.angle_with(v)==pi

    def component_parallel_to(self,v):
        try:
            u=v.normalized()
            weight=self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e)==self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_orthogonal_to(self,v):
        try:
            parallel_component=self.component_parallel_to(v)
            return self - parallel_component
        except Exception as e:
            if str(e)==self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

v1=Vector([5.581,-2.136])
v2=Vector([1,2,3])

print(v1.magnitude())
print(v1.normalized())
#
# print(v1)
# print(v1.coordinates)
# print(v1.dimension)
# print(v1+v2)
# print(v1-v2)