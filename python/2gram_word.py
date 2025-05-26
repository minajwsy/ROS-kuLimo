text = 'this is python script'
words = text.split()
print(words)

for i in range(len(words) - 1 ):
    print(words[i], words[i+1])