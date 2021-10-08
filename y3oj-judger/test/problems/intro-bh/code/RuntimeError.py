# -*- coding: UTF-8 -*-

import sys
import random

with open('bh.csv', 'r+') as csv_file:
    lines = csv_file.readlines()

n = len(lines)
luck = [''] * n
for i in range(n):
    luck[i] = lines[i]
    if luck[i].endswith('\n'):
        luck[i] = luck[i][:-1]

m = int(input('请输入要抽取的车牌数: '))

count = 0
choosed = [False] * (n - 1)

while count < m:
    k = random.randint(0, n - 1)
    if choosed[k]:
        continue
    count += 1
    choosed[k] = True
    print(luck[k])