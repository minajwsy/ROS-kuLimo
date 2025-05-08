### PJW 자력으로 해결 ### 
# row, col = map(int, input().split())
# matrix = []
# for i in range(row):
#     #matrix.append(input())  # 주의: 문제 제대로 안 읽어서 Err! -> 이것 빼곤 다 자력으로 풀었다!!!!!
#     matrix.append(list(input()))

# for rr in range(row):
#     for cc in range(col):
#         if matrix[rr][cc] == '.':
#             nb = 0
#             for i in range(max(rr-1,0), min(row,rr+2)):
#                 for j in range(max(cc-1,0), min(col,cc+2)):
#                     if matrix[i][j] == '*':
#                             nb += 1
#             matrix[rr][cc] = nb
            
# for rr in range(row):
#     for cc in range(col):
#         print(matrix[rr][cc], end='')
#     print()

### 코딩도장 site의 해설 참고하여 수정:
## 해설만 보고 자력으로 풀었다!!  
row, col = map(int, input().split())
matrix = []
for i in range(row):
    matrix.append(list(input()))

for rr in range(row):
    for cc in range(col):
        if matrix[rr][cc] == '.':
            nb = 0
            for i in range(rr-1,rr+2):
                if i<0 or i>=row: 
                    continue
                for j in range(cc-1,cc+2):
                    if j<0 or j>=col: 
                        continue
                
                    if matrix[i][j] == '*':
                            nb += 1
            matrix[rr][cc] = nb
            
for rr in range(row):
    for cc in range(col):
        print(matrix[rr][cc], end='')
    print()