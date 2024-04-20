# class Point:
#     def draw(self):
#         print("draw")

# point = Point()
# print(type(point))
# print(isinstance(point, Point))


# constracture

# class Point:
#     def __init__(self, x, y):
#        self.x = x
#        self.y = y


#     def draw(self):
#       print(f"Point ({self.x}, {self.y})")


# point = Point(1,2)
# point.draw()


# another = Point(3,4)
# another.draw()

# class method vs instance method
# class Point:
#     # //isinstance
#     def __init__(self, x, y):

#        self.x = x
#        self.y = y

#     #class
#     @classmethod
#     def zero(cls):
#        return cls(0,0)


#      # //isinstance

#     def draw(self):
#       print(f"Point ({self.x}, {self.y})")


# point = Point.zero()

# magic method
# __str__ for sting
# __init__ for constructor

# __eq__ for equal
# __gt__ for greaterthan
# __add__ for adding

# comparing object

# class Point:


#     # //isinstance
#     def __init__(self, x, y):

#         self.x = x
#         self.y = y

#     def __add__(self, other):
#         return Point(self.x + other.x, self.y + other.y)

#     def __eq__(self, other):
#         return self.x == other.x and self.y == other.y

#     def __gt__(self, other):
#         return self.x > other.x and self.y > other.y
#       # //isinstance

#     def draw(self):
#         print(f"Point ({self.x}, {self.y})")


# point = Point(5, 4)
# otherP = Point(1, 2)

# print(point == otherP)
# print(point > otherP)
# combind = point + otherP
# print(combind.x)

class InvalidOperationError(Exception):
    pass

class Stream:
    def __init__(self):
        self.opened = False

    def open(self):
        if self.opened:
            raise InvalidOperationError("stream is already opened")
        self.opened = True

    def close(self):
        if not self.opened:
            raise InvalidOperationError("stram is already closed")
        self.opened =False


class FileStream(Stream):
    def read(self):
        print("reading from file")
                


class NetworkStream(Stream):
    def read(self):
        print("reading from Network")
                


