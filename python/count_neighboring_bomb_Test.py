row, col = map(int, input().split())
matrix = []
for i in range(row):
    #matrix.append(input())  # 주의: 문제 제대로 안 읽어서 Err! -> 이것 빼곤 다 자력으로 풀었다!!!!!
    matrix.append(list(input()))

for rr in range(row):
    for cc in range(col):
        if matrix[rr][cc] == '.':
            nb = 0
            for i in range(max(rr-1,0), min(row,rr+2)):
                for j in range(max(cc-1,0), min(col,cc+2)):
                    if matrix[i][j] == '*':
                            nb += 1
            matrix[rr][cc] = nb
            
for rr in range(row):
    for cc in range(col):
        print(matrix[rr][cc], end='')
    print()