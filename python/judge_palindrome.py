file = open('words.txt', 'r')
words = file.readlines()
#print(words)

for word in words:
    word = word.strip('\n')
    
    ## 방법1: 반복문 사용
    is_palindrome = True
    for i in range(len(word)//2):
        if word[i] != word[-1-i]: 
            is_palindrome = False
       #else:
            break
    if is_palindrome:
        print(word)
    
    ## 방법2: 시퀀스 뒤집기 (가장 간단한 방법
    # if word == word[::-1]:  # 시퀀스 뒤집기
    #     print(word)