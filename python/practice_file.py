with open('words0.txt', 'r') as file:
    count = 0
    lines = file.readlines()
    print(lines)
    for line in lines:
        #if len(line) <= 10:  # 출력 = 3 -> wrong!!
        if len(line.strip('\n') ) <= 10:
            count += 1 
    print(count)