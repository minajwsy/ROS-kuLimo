a, b = map(int, input().split())

#x = [2**i for i in range(a, b+1) if i != a+1 and i != b-1]
x = [2**i for i in range(a, b+1)]
x.pop(1)
x.pop(-2)

print(x)