class PointHolder:
    __initial: int = 0
    points: int

    def __init__(self, custom_initial_points=40):
        self.__initial = custom_initial_points
        self.points = self.__initial

    def increase(self, amount=1):
        self.points += amount

    def decrease(self, amount=1):
        self.points -= amount

    def reset(self):
        self.points = self.__initial
