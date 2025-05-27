word = 'river' 
#word = word.strip('\n')
print(word)
print(word[1], word[-1-1], sep=' ')
#print(word[1] != word[-1-1])

is_palindrome = True
for i in range(len(word)//2):
    if word[i] != word[-1-i]: 
        is_palindrome = False
    #else:      ## wrong -> 제거해야!
        break
print(is_palindrome)  # why True?? -> else 때문!   
if is_palindrome:
    print(word)