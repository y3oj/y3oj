import random
a=[random.random()]
while True:
    a.extend([x for x in a])