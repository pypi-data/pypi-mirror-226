import onenonly.maths as maths

class Vector:
    def __init__(self,vector):
        for x in vector:
            if not isinstance(x,int|float):
                raise ValueError("Vector must integer or floating values")
        if not isinstance(vector,list):
            vector = list(vector)
        if len(vector) != 3:
            raise ValueError("Vector must have 3 directions")
        self.i = vector[0]
        self.j = vector[1]
        self.k = vector[2]

    def __repr__(self):
        return f"<{self.i} {self.j} {self.k}>"

    def toList(self):
        return [self.i,self.j,self.k]

    def get(self,direction):
        if direction == 1:
            return self.i
        elif direction == 2:
            return self.j
        elif direction == 3:
            return self.k
        else:
            raise IndexError("out of range!")

    def assign(self,direction:int,value:int|float):
        if direction == 1:
            self.i = value
        elif direction == 2:
            self.j = value
        elif direction == 3:
            self.k = value
        else:
            raise IndexError("out of range!")
        return Vector((self.i,self.j,self.k))

    def dot(self,other):
        if not isinstance(other,Vector):
            try:
                other = Vector(other)
            except Exception as e:
                return e
        return self.i * other.i + self.j * other.j + self.k * other.k

    def cross(self,other):
        if not isinstance(other,Vector):
            try:
                other = Vector(other)
            except Exception as e:
                return e
        X = self.j * other.k - other.j * self.k
        Y = -(self.i * other.k - other.i * self.k)
        Z = self.i * other.j - self.j * other.i
        return Vector((X,Y,Z))
    
    def magnitude(self):
        return maths.sqrt(self.i * self.i + self.j * self.j + self.k * self.k)
    
    def projection(self,other):
        dot_product = self.dot(other)
        other_magnitude_squared = other.magnitude() ** 2
        projection_values = []
        for direction in range(1,4):
            projection_value = (dot_product / other_magnitude_squared) * other.get(direction)
            projection_values.append(projection_value)
        return Vector(projection_values)
    
    def add(self,other):
        if isinstance(other,int|float):
            return Vector((self.i + other,self.j + other,self.k + other))
        if isinstance(other,Vector):
            return Vector((self.i + other.i,self.j + other.j,self.k + other.k))
        raise ValueError("invalid arguments!")
    
    def sub(self,other):
        if isinstance(other,int|float):
            return Vector((self.i - other,self.j - other,self.k - other))
        if isinstance(other,Vector):
            return Vector((self.i - other.i,self.j - other.j,self.k - other.k))
        raise ValueError("invalid arguments!")
    
    def pow(self,exponent=1.0):
        return Vector((self.i ** exponent,self.j ** exponent,self.k ** exponent))

    def prod(self,scalar=1.0):
        return Vector((self.i * scalar,self.j * scalar,self.k * scalar))
    
    def div(self,scalar=1.0):
        return Vector((self.i / scalar,self.j / scalar,self.k / scalar))
    
    def floor_div(self,scalar=1.0):
        return Vector((self.i // scalar,self.j // scalar,self.k // scalar))

    def octant(self):
        if self.i == 0 and self.j == 0 and self.k == 0:
            return 0
        if self.i >= 0 and self.j >= 0 and self.k >= 0:
            return 1
        elif self.i < 0 and self.j >= 0 and self.k >= 0:
            return 2
        elif self.i < 0 and self.j < 0 and self.k >= 0:
            return 3
        elif self.i >= 0 and self.j < 0 and self.k >= 0:
            return 4
        elif self.i >= 0 and self.j >= 0 and self.k < 0:
            return 5
        elif self.i < 0 and self.j >= 0 and self.i < 0:
            return 6
        elif self.i < 0 and self.j < 0 and self.k < 0:
            return 7
        elif self.i >= 0 and self.j < 0 and self.k < 0:
            return 8
