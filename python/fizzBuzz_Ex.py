# for i in range(1,31):
#     if i%3==0 and i%5!=0:
#         print('Fizz')
#     elif i%3==0 and i%5==0:
#         print('FizzBuzz')
#     elif i%3!=0 and i%5==0:
#         print('Buzz')
#     else:
#         print(i)

for i in range(1,31):
    
    #if i%3==0 and i%5==0:
    if i%15==0:
        print('FizzBuzz')
    elif i%3==0:
        print('Fizz')
    elif i%5==0:
        print('Buzz')
    else:
        print(i)