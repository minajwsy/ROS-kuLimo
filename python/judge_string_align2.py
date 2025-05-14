sentence = input()
words = list(map(int, sentence.split(';')))   
words.sort(reverse=True)

for num in words:
    formatted_num = '{0: >9,}'.format(num) 
    print(formatted_num)      