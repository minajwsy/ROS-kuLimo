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

if __name__ == "__main__":
    main()
