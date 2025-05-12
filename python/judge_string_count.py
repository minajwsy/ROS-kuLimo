parag = input()
words = parag.split(' ')
#print(words)

count = 0
for i in words:
    i = i.strip(',.')  ## 주의 : 우변의 결과를 변수로 할당해야 !!
    if i == 'the':
        count += 1
print(count)