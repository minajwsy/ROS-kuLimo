text = 'abcde'

# two_gram = zip(text, text[1:])  # 여러 개의 반복 가능한 객체를 받아서-> 같은 위치의 요소들을 튜플로 묶어줌
# for pair in two_gram:
#     print(pair[0], pair[1], sep='')

two_gram_li = list(zip(text, text[1:]))  
for i in two_gram_li:
    print(i[0], i[1], sep='')