def is_palindrome(word):
#     #is_palindrome = False
#     if len(word) == 1: 
#         return True  
#     is_palindrome = (word[0] == word[-1]) and is_palindrome(word[1:-1])
#     word = word[1:-1]
#     return is_palindrome
    if len(word) < 2:
        return True
    if word[0] != word[-1]:
        return False
    return is_palindrome(word[1:-1])

print(is_palindrome('hello'))
print(is_palindrome('level'))
print(is_palindrome('abcdedcba'))