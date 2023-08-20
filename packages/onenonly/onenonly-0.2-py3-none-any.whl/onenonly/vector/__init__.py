import onenonly.maths as maths

class Vector:
    def __init__(self,vector):
        if not isinstance(vector,list):
            vector = list(vector)
        if len(vector) != 3:
            raise ValueError("Vector must have 3 directions")
        self.x = vector[0]
        self.y = vector[1]
        self.z = vector[2]

    def __repr__(self):
        return f"<{self.x} {self.y} {self.z}>"

    def toList(self):
        return [self.x,self.y,self.z]

    def get(self,direction:int=1):
        if direction == 1:
            return self.x
        elif direction == 2:
            return self.y
        elif direction == 3:
            return self.z
        else:
            raise IndexError("out of range!")

    def assign(self,direction:int,value:int|float):
        if direction == 1:
            self.x = value
        elif direction == 2:
            self.y = value
        elif direction == 3:
            self.z = value
        else:
            raise IndexError("out of range!")

    def dot(self,other):
        if not isinstance(other,Vector):
            try:
                other = Vector(other)
            except Exception as e:
                return e
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self,other):
        if not isinstance(other,Vector):
            try:
                other = Vector(other)
            except Exception as e:
                return e
        X = self.y * other.z - other.y * self.z
        Y = -(self.x * other.z - other.x * self.z)
        Z = self.x * other.y - self.y * other.x
        return Vector((X,Y,Z))
    
    def magnitude(self):
        return maths.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
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
            return Vector((self.x + other,self.y + other,self.z + other))
        if isinstance(other,Vector):
            return Vector((self.x + other.x,self.y + other.y,self.z + other.z))
        raise ValueError("invalid arguments!")
    
    def sub(self,other):
        if isinstance(other,int|float):
            return Vector((self.x - other,self.y - other,self.z - other))
        if isinstance(other,Vector):
            return Vector((self.x - other.x,self.y - other.y,self.z - other.z))
        raise ValueError("invalid arguments!")
    
    def pow(self,exponent=1.0):
        return Vector(self.x ** exponent,self.y ** exponent,self.z ** exponent)

    def prod(self,scalar=1.0):
        return Vector(self.x * scalar,self.y * scalar,self.z * scalar)
    
    def div(self,scalar=1.0):
        return Vector(self.x / scalar,self.y / scalar,self.z / scalar)
    
    def floor_div(self,scalar=1.0):
        return Vector(self.x // scalar,self.y // scalar,self.z // scalar)
