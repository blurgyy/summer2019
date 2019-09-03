import random
word=random.choice(['apple','banana','orange','watermelon','son','bed','father'])
n=len(word)
outline = '-' * n
print(outline)
out = list(outline)
num = 5 + n
cnt_wrong = 0
win = False
while(cnt_wrong < 5):
    m = input('用户输入字母为：')
    if word.find(m)==-1:
        cnt_wrong += 1
        print(f'猜错，剩余次数为:{5-cnt_wrong}')
    else:
        for i in range(0,n):
            if word[i]==m:
               out[i]=m
        if list(word) == out:
            win = True
            break
    for j in range(0,n):
        print(out[j],end='')
    print()
if(win):
    print("YOU WIN")
else:
    print(f'次数用光，游戏结束')
