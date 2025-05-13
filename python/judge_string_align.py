sentence = input()
#words = sentence.split(';')   # wrong
#words = map(int, sentence.split(';'))  # wrong??    
words = list(map(int, sentence.split(';')))   

# prices1 = []
# for i in words:
#     prices1.append(int(i))
# prices1.sort(reverse=True)
    
words.sort(reverse=True)
#print(words)
#prices = []

for i in words:
    #i = '{0: >9}'.format(i, ',')  # err
    i = '{0: >9,}'.format(i)
    #print(type(i))   # str
    i = i.strip().replace(',', '')  
    num = int(i)           
    #i = format(i, ',')            # wrong
    #formatted_num = f"{num:,}"
    formatted_num = format(num, ',') 
    #print(type(formatted_num))  # str
    #prices.append(formatted_num)  # wrong 
    print(formatted_num)      