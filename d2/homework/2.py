d = {
    'a': 20,
    'b': 9,
    'c': 3,
    'B': 45,
    'C': 2
}

ans = {
    x.lower(): d.get(x.lower(), 0) + d.get(x.upper(), 0)
    for x in d.keys()
}

print(ans)
