import random

a = {1 : 11}
b = {2 : 22}
c = {3 : 33}

d ={**a, **b, **c}

num1, num2 = random.choice(list(d.items()))

print(d)
print(num1,num2)