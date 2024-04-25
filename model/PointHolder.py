class PointHolder:
    __initial: int = 0
    points: int
    wins: int = 0
    name: str = ""

    def __init__(self, custom_initial_points=40):
        self.__initial = custom_initial_points
        self.points = self.__initial
        self.wins = 0

    def increase(self, amount=1):
        self.points += amount

    def decrease(self, amount=1):
        self.points -= amount

    def set_wins(self, amount):
        self.reset_points()
        if amount >= 0 & amount <= 3:
            self.wins = amount

    def reset(self):
        self.reset_points()
        self.reset_wins()

    def reset_wins(self):
        self.wins = 0

    def reset_points(self):
        self.points = self.__initial
