text = 'this is python script'
words = text.split()
print(words)

# for i in range(len(words) - 1 ):
#     print(words[i], words[i+1])

three_gram_word_li = list(zip(words, words[1:], words[2:]))  
for i in three_gram_word_li:
    print(i[0], i[1], i[2])