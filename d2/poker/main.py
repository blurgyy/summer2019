#!/usr/bin/python

import deck

while(True):
    p = deck.Deck()
    p.shuffle()
    pai = p.deal(5)
    # assert len(pai) == 5, "??????"
    del p
    pai.sort(key=lambda x:x.figure)
    x = True
    for i in range(1, len(pai)):
        if(pai[i].suit == pai[i-1].suit and (pai[i].figure == pai[i-1].figure + 1 or pai[i].figure == 10 and pai[i-1].figure == 1)):
            continue
        else:
            x = False
            break
    if(x == True):
        for i in pai:
            print(i,end="\t")
        print()

