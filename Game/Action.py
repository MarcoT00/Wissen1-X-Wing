# class Action:
#     @staticmethod
#     def acceleration(speed: int):
#         speed += 1

#     @staticmethod
#     def hold(speed: int):
#         pass

#     @staticmethod
#     def slow(speed: int):
#         speed -= 1


from enum import Enum


class Action(Enum):
    B = "Beschleunigen"
    H = "Geschwindigkeit halten"
    V = "Verlangsamen"
