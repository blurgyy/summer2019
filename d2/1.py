#!/usr/bin/python

class first:
    def __init__(self, x, ):
        self.x = x;
    def __str__(self, ):
        return "class `first` with %d" % self.x;

class second(first):
    def __init__(self, x = 10, ):
        super().__init__(x);
        pass;

a = second();
print(a.x)

