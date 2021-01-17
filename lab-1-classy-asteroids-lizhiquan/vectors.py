"""
This module houses the implementation of the Vector class.
A vector is comprised of x, y, and z coordinates in a 3D space.
"""

from __future__ import annotations
from math import sqrt
from random import randint


class Vector:
    """
    This class represents a vector, which has x, y and z coordinates
    and a magnitude.
    """

    def __init__(self, x: float, y: float, z: float):
        """
        Initializes a Vector object with x, y, and z coordinates.
        :param x: a float, represents x-coordinate
        :param y: a float, represents y-coordinate
        :param z: a float, represents z-coordinate
        """
        self.x = x
        self.y = y
        self.z = z

    @property
    def magnitude(self) -> float:
        """
        Calculates and returns the magnitude of this vector.
        :return: a float, the magnitude of the vector
        """
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def __str__(self):
        return f'Vector (x: {self.x}, y: {self.y}, z: {self.z})'

    @classmethod
    def generate_random_vector(cls, min_val: int, max_val: int) -> Vector:
        """
        Generates x, y, z values from the given range [min_val, max_val]
        and returns a new Vector object from those values.
        :param min_val: an int, the min value of the range, inclusive
        :param max_val: an int, the max value of the range, inclusive
        :return: a Vector, with x, y, and z are randomized from the
                 range [min_val, max_val]
        """
        x = randint(min_val, max_val)
        y = randint(min_val, max_val)
        z = randint(min_val, max_val)
        return cls(x, y, z)

    def __getitem__(self, item: str) -> float:
        """
        Accesses and returns values via []. Supported values are "x",
        "y", "z" and "magnitude".
        :param item: a str, the name of the value to retrieve
        :return: a float, the value related to the item argument
        """
        item_mapper = {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'magnitude': self.magnitude,
        }
        return item_mapper[item]

    def __setitem__(self, key: str, value: float) -> None:
        """
        Sets the given value to the attribute correlated with key.
        Supported keys are "x", "y" and "z".
        :param key: a str, the attribute name to set
        :param value: a float, the new value of the attribute
        :return: None
        """
        if key == 'x':
            self.x = value
        elif key == 'y':
            self.y = value
        elif key == 'z':
            self.z = value

    def __add__(self, other: Vector) -> Vector:
        """
        Adds this with the other vector and returns the result.
        :param other: a Vector, the vector to be added with
        :return: a Vector, the result of the addition
        """
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector) -> Vector:
        """
        Subtracts this with the other vector and returns the result.
        :param other: a Vector, the vector to be subtracted with
        :return: a Vector, the result of the subtraction
        """
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other) -> Vector:
        """
        Multiplies this vector with a scalar or another vector (cross
        product) and returns the result.
        :param other: a Vector, the vector to be multiplied with
        :return: a Vector, the result of the multiplication
        """
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other, self.z * other)
        return Vector(
            self.y*other.z - self.z*other.y,
            self.z*other.x - self.x*other.z,
            self.x*other.y - self.y*other.x,
        )

    def __rmul__(self, other) -> Vector:
        """
        Supports multiplication when the vector is on the right hand
        side of the expression.
        :param other: a Vector, the vector to be multiplied with
        :return: a Vector, the result of the multiplication
        """
        return self.__mul__(other)

    def __abs__(self) -> float:
        """
        Returns the magnitude of this vector.
        :return: a float, the magnitude of this vector
        """
        return self.magnitude

    def __eq__(self, other) -> bool:
        """
        Checks and returns True if 2 vectors are equal. 2 vectors are
        equal if and only if their x, y and z values are all the same.
        :param other: a Vector, the other vector to be compared with
        :return: a bool, the result of the comparison
        """
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other) -> bool:
        """
        Checks and returns True if 2 vectors are not equal.
        :param other: a Vector, the other vector to be compared with
        :return: a bool, the result of the comparison
        """
        return not self.__eq__(other)

    def __lt__(self, other) -> bool:
        """
        Compares the magnitudes and returns True if the magnitude is
        less than other's magnitude.
        :param other: a Vector, the other vector to be compared with
        :return: a bool, the result of the comparison
        """
        return self.magnitude < other.magnitude

    def __gt__(self, other) -> bool:
        """
        Compares the magnitudes and returns True if the magnitude is
        greater than other's magnitude.
        :param other: a Vector, the other vector to be compared with
        :return: a bool, the result of the comparison
        """
        return self.magnitude > other.magnitude

    def __le__(self, other) -> bool:
        """
        Compares the magnitudes and returns True if the magnitude is
        less than or equal other's magnitude.
        :param other: a Vector, the other vector to be compared with
        :return: a bool, the result of the comparison
        """
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other) -> bool:
        """
        Compares the magnitudes and returns True if the magnitude is
        greater than or equal other's magnitude.
        :param other: a Vector, the other vector to be compared with
        :return: a bool, the result of the comparison
        """
        return self.__gt__(other) or self.__eq__(other)


def main():
    """
    Demonstrates uses of the Vector class.
    """

    v1 = Vector(1, 2, 3)
    v2 = Vector(2, 3, 4)
    v3 = Vector(1, 2, 3)

    print('v1:', v1, v1.magnitude)
    print('v2:', v2, v2.magnitude)
    print('v3:', v3, v3.magnitude)

    print("v1['x']:", v1['x'])
    print("v1['y']:", v1['y'])
    print("v1['z']:", v1['z'])
    print("v1['magnitude']:", v1['magnitude'])

    v2['x'] = 4
    v2['y'] = 2
    v2['z'] = 3
    print("v2['x']=4     v2['y']=2     v2['z']=3    ", v2)

    print('v1 == v3', v1 == v3)
    print('v1 != v3', v1 != v3)
    print('v1 >= v3', v1 >= v3)
    print('v1 <= v3', v1 <= v3)
    print('v2 == v3', v2 == v3)
    print('v2 != v3', v2 != v3)
    print('v1 magnitude', abs(v1))
    print('v2 magnitude', abs(v2))
    print('v1 < v2', v1 < v2)
    print('v1 > v2', v1 > v2)
    print('v1 >= v2', v1 >= v2)
    print('v1 <= v2', v1 <= v2)

    print('abs(v3):', abs(v3))
    print('abs(v3) == v3.magnitude', abs(v3) == v3.magnitude)

    v4 = v1 + v3
    print('v4 = v1 + v3       v4:', v4)
    v4 += v1
    print('v4 += v1           v4:', v4)
    v4 = v4 - v1
    print('v4 = v4 - v1       v4:', v4)
    v4 -= v3
    print('v4 -= v3           v4:', v4)
    v4 = v4 * 2
    print('v4 = v4 * 2        v4:', v4)
    v4 = 3 * v4
    print('v4 = 3 * v4        v4:', v4)
    v4 *= 2
    print('v4 *= 2            v4:', v4)
    v4 = Vector(1, 2, 3) * Vector(2, 3, 4)
    print('Vector(1, 2, 3) * Vector(2, 3, 4) =', v4)


if __name__ == '__main__':
    main()
