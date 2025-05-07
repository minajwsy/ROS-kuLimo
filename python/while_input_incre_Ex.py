count  = int(input('반복할 횟수를 입력하세요:'))

# 방식 1
# i=0
# while i < count:
#     print("Hello World!", i)
#     i+=1

# 방식 2
while count > 0:
    print("Hello World!", count)
    count -= 1