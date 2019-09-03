import random 

word_list = [
    "master",
    "space",
    "python",
    "preference",
    "tool",
]

sel = random.choice(word_list)
nxt = sel
length = len(sel)
print(">>>", "-" * length);

cnt = 0 # 错的次数
n = 5 # 错的次数上限
win = False
mask = [False for i in range(length)]
while(cnt < n):
    while(True):
        letter = input("input 1 letter> ")
        if(len(letter) > 0):
            break;

    index = nxt.find(letter)

    if(index == -1):
        cnt += 1
        print(f'wrong, {n-cnt} times remains')
    else:
        slist = list(nxt)
        slist[index] = "*"
        nxt = "".join(slist)
        mask[index] = True
        if(mask == list([True] * length)):
            win = True
    # print(mask)
    print(">>> ", end="")
    for i in range(length):
        if(mask[i]):
            print(sel[i], end="")
        else:
            print('-', end="")
    print()
    if(win):
        break

if(win):
    print("you win")
else:
    print("you lose")
