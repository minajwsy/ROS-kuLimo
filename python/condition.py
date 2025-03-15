def main():
    # 조건문
    number  = int(input("숫자를 넣어주세요 : "))
    if number % 2 == 0:
        print("짝수 입니다.")
    else:
        print("홀수 입니다.")

    # 반복문 for
    for i in range(10): # n번 반복 --0 부터 시작 --- n-1 까지 반복
        print(f" {i} 번째 반복되는 문장입니다.")
    print(list(range(10)))

if __name__ == "__main__":
    main()
