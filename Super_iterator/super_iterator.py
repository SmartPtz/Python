
from collections import Iterable

data = [[[1,2,3,[4,5,6,7,8,[9,0,1,2,3,4,5]]], 2, 3, 4],[1, 2, 3, 4]]

def super_iterator(data):
    if isinstance(data, Iterable):
        for value in data:
            if isinstance(value, Iterable):
                for subvalue in super_iterator(value):
                    yield subvalue
            else:
                yield value

    else:
        yield data

for i in super_iterator(data):
    print(i)