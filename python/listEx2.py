def main():
    list_a = [1, 2, 3]
    list_b = [4, 5, 6]
    print(list_a + list_b) # [1,2,3,4,5,6]
    print(list_a*3) # [1,2,3,1,2,3,1,2,3]
    list_a.append("추가원소") # type: ignore
    list_a.insert(1, "insert 추가원소") # type: ignore
    print(list_a)
    del list_a[2] # [1, "insert 추가원소", 3, "추가원소"]
    print(list_a)
    list_a.pop(1) # [1, 3, "추가원소"]
    print(list_a)
    list_a.remove(3) # [1, "추가원소"]
    print(list_a)
    
    if 5 in list_b:
        print("5 는 list_b 에 있습니다.")
    else:
        print("5 는 list_b 에 없습니다.")

    j =0
    for i in list_b:
        j +=1
        print(f"{j} 번째 요소는 {i} 입니다.")

    for j, i in enumerate(list_b):
        print(f"{j+1} 번째 요소는 {i} 입니다.")

if __name__ == "__main__":
    main()
