def main():
    input_var = input("숫자를 입력하세요:") # 스트링으로만 리턴된다.
    print(f"입력한 숫자는 {input_var} 입니다.")
    print(f"더하기 30은 : {int(input_var) * 30}")

if __name__ == "__main__":
    main()
