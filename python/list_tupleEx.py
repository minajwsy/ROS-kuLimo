#step = input()           # wrong
#step = map(int, input())  # wrong
#step, = map(int, input())  # 방법1
step = int(input())        # 방법2 <- 이 방법이 더 좋음!

tup1 = tuple(range(-10, 10, step))
print(tup1)