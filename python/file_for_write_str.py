with open('hello.txt', 'w') as file:
    for i in range(5):
        file.write('Hello World! {0}\n'.format(i))