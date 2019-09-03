fname = "article.txt"
with open(fname) as f:
    text = f.read()

# text = input()
seps = "(),.\n\t'’&?!"
for sep in seps:
    text = text.replace(sep, ' ')
# print(text)
words = text.split(' ')
words = [x for x in words if len(x) > 0]
print(len(words), "words in article")
