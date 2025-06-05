#files = input().split()
#files = ['1.jpg', '10.png', '11.png', '2.jpg', '3.png'] 
#files = ['97.xlsx', '98.docx', '99.docx', '100.xlsx', '101.docx', '102.docx'] 
#leng = len(files[:files.index('.')]) 
    
# print(list(map(lambda x: x.zfill(8), files)))
## print(list(map(lambda x: x.zfill(len(x[x.index('.'):])+3), files)))                              #ans 1
#for file in files:
#    file = file.split('.')[0]

#x = '3.jpg'
#x = '10.png'
#x = '102.docx'
#'{0:0>3+len(x[x.index('.'):])}'.format(int(x.split('.')[0]))
#'{0:0>3}'.format(int(x.split('.')[0]))
#str('{0:0>3}'.format(int(x.split('.')[0]))) + '.' + x.split('.')[1]

#print(list(map(lambda x: '{0:0>(3+len(x[x.index('.'):]))}'.format(x.split('.')[0]), files)))
#print(str('{0:0>3}'.format(int(x.split('.')[0]))) + '.' + x.split('.')[1])
#print(list(map(lambda x: str('{0:0>3}'.format(int(x.split('.')[0]))) + '.' + x.split('.')[1], files)))  #ans 2

## python 인터프리터에서 연습!! :
#ftn = lambda x: '{0:03d}.{1}'.format(int(x.split('.')[0]), x.split('.')[1])
#ftn(x)                                   

print(list(map(lambda x: '{0:03d}.{1}'.format(int(x.split('.')[0]), x.split('.')[1]), files)))           #ans 3   