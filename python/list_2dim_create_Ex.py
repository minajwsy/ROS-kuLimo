# a = []
# for i in range(3):
#     line = []
#     for j in range(2):
#         line.append(j)
#     a.append(line)
# print(a)

a=[3,1,3,2,5]
b=[] 
for i in a:
    line=[]
    for j in range(i):
        line.append(5)
    b.append(line)
print(b)