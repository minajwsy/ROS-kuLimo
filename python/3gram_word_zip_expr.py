#text = 'hello'                            # 글자 단위 N-gram의 경우
text = 'Python is a programming language'  
words = text.split()                       # 단어 단위 N-gram의 경우
# print(words)

# two_gram_word_li = list(zip(words, words[1:], words[2:]))  
# for i in two_gram_word_li:
#     print(i[0], i[1], i[2])

list_expr1 = [words[i:] for i in range(3)]  # create a list of slices of the text starting from each index up to the end
print(list_expr1)

list_expr2a = list(zip(list_expr1))   # wrong!
print(list_expr2a)

list_expr2b = list(zip(*list_expr1))  # correct! -> [주의] 리스트 언패킹 필요!!
print(list_expr2b)

#list_expr3 =   zip([text[i:] for i in range(3)])
list_expr3 =   list(zip(*[words[i:] for i in range(3)]))
print(list_expr3)

## 단어 단위 N-gram을 튜플로 출력하기:
n_gram = zip(*[words[i:] for i in range(3)])
for i in n_gram:
    print(i)     