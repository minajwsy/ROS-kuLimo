## 방법 1
# i = 0
# while True:
#     if i == 74:
#         break
    
#     if i % 10 != 3:
#         i += 1
#         continue
#         #print(i, end=' ')           
#     print(i, end=' ')
#     i += 1
    
## 방법 2
i = 0
while True:
    if i % 10 != 3:
        i += 1
        continue
        #print(i, end=' ')
        
    if i == 74:
        break
    
    print(i, end=' ')
    i += 1        