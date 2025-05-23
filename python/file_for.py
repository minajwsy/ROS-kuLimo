with open('hello.txt', 'r') as file:
    for line in file:
        print(line.strip('\n'))