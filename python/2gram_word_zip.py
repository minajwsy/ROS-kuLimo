text = 'this is python script'
words = text.split()
print(words)

# for i in range(len(words) - 1 ):
#     print(words[i], words[i+1])

two_gram_word_li = list(zip(words, words[1:]))  
for i in two_gram_word_li:
    print(i[0], i[1])