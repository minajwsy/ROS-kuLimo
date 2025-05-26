text = 'python'
slices = [text[i:] for i in range(3)]
print("slice list:", slices)
# 출력: ['python', 'ython', 'thon']

# 방법 1: 리스트를 바로 전달 (잘못된 방법)
result1 = list(zip(slices))
print("zip(slices):", result1)
# 출력: [('python',), ('ython',), ('thon',)]

# 방법 2: 언패킹 사용 (올바른 방법)
result2 = list(zip(*slices))
print("zip(*slices):", result2)
# 출력: [('p', 'y', 't'), ('y', 't', 'h'), ('t', 'h', 'o'), ('h', 'o', 'n')]

# 방법 2는 다음과 동일함
result3 = list(zip('python', 'ython', 'thon'))
print("transfer manually:", result3)
# 출력: [('p', 'y', 't'), ('y', 't', 'h'), ('t', 'h', 'o'), ('h', 'o', 'n')]