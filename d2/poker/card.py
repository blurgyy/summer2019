class Card:
#花色和牌面 属性
    def __init__(self,suit,figure):
        self.suit = suit
        self.figure = figure

    def __str__(self):
        if self.figure == 1:
            figure = 'A'
        elif self.figure == 11:
            figure = 'J'
        elif self.figure == 12:
            figure = 'Q'
        elif self.figure == 13:
            figure = 'K'
        else:
            figure = str(self.figure)
        return self.suit + figure
