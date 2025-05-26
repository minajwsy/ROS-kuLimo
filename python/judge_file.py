with open('words.txt', 'r') as file:
    words = file.read()
   #print(words)
   #words = list(map(str, words.split(' '))) -> 불요!
    words = words.split(' ')
    #print(words)      
    for word in words:
        word = word.strip(',.')
        if 'c' in word:
            print(word) 