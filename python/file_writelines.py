#lines = ['안녕~', '파이썬', '코딩 도장이야']
lines = ['안녕~\n', '파이썬\n', '코딩 도장이야\n']
with open('hello.txt', 'w') as file:
    file.writelines(lines) 