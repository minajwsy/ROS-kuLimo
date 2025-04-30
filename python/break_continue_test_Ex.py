start, stop = map(int, input().split())

i = start
 
while True:
    if i % 10 == 3:
        i += 1
        continue
    
    if i > stop:
        break
    
    print(i, end=' ')
    i += 1   