a = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

b = [i for row in a for i in row]

print(b)