file = open('words.txt', 'r')
words = file.readlines()
#print(words)

for word in words:
    word = word.strip('\n')

    is_palindrome = True
    for i in range(len(word)//2):
        if word[i] != word[-1-i]: 
            is_palindrome = False
        else:
            break
    if is_palindrome:
        print(word)