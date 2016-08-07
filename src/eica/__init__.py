# from enum import Enum     # for enum34, or the stdlib version
# from aenum import Enum  # for the aenum version


def enum(**enums):
    return type('Enum', (), enums)


# Ponto = enum('Ponto', 'x y')
class Ponto:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __repr__(self):
        return self.x, self.y
