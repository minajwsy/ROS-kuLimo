# print(1, end=' ')
# print(2, end='')
# print(3)

# yy=2000
# mm=10
# dd=27

# hh=11
# min=43
# sec=59

# print(yy,mm,dd,sep='/',end=' ')
# print(hh,min,sec,sep=':')

yy, mm, dd, hh, min, sec = input().split()
print(yy, mm, dd, sep='-', end='T')
print(hh, min, sec, sep=':')