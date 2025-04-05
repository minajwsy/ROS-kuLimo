def main():
    li1 = [i + 1 for i in range(100) if i % 2 == 1]
    print(li1)
    array = ["사과", "자두", "초콜릿", "바나나", "체리"]
    li2 = [fruit for fruit in array if fruit != "바나나"]
    print(li2)

if __name__ == "__main__":
    main()
