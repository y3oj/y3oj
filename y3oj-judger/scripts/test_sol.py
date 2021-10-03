import random
from os import path

# dir = path.abspath(path.dirname(__file__))
# with open(path.join(dir, '..', 'hack.txt'), 'w+', encoding='utf-8') as file:
#     file.write('hacked.')

a, b = map(int, input().split())
print(a + b - random.randint(0, 1))
