import card
import random
class Deck:
    def __init__(self):
        self.cards = []
        hs = ['黑桃','红心','梅花','方片']
        for i in hs:
            for j in range(1,14):
                self.cards.append(card.Card(i,j))

    def show(self):
        for i in self.cards:
            print(i,end="\t")
        print()
    # 洗牌
    def shuffle(self):
        random.shuffle(self.cards)
    # 发牌
    def deal(self, k = 1, ):
        ret = [];
        for i in range(k):
            ret.append(self.cards.pop());
        return ret;
