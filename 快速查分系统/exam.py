import json
from 快速查分系统.spider_for_exam import Spider
from concurrent import futures

file = open('achievement.json', 'r')
a = json.load(file)
b = []
c = []
for i in a:
    # print(i)
    num = 0
    if i['name']=='管志飞':
        print(i)
    for k in i['result']:
        # if k==' 02010035 Js+Jquery':
        #     print(i['name'], k, i['result'][k])
        num += int(i['result'][k])
    b.append(i['name'])
    c.append(num)

data = dict(zip(b, c))
# data['黄世鹏'] =
i = sorted(data.items(), key=lambda item: item[1], reverse=True)
sum = 0
for k in i:
    sum += 1
    print(sum, k)
