files = input().split()

#leng = len(files[:files.index('.')]) 
    
# print(list(map(lambda x: x.zfill(8), files)))
print(list(map(lambda x: x.zfill(len(x[x.index('.'):])+3), files)))