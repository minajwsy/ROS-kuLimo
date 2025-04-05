def return_100():
    return 100, 200, "되돌아 가는 문자", True, False

def main():
    a, b, *c = return_100()
    # print(type(var))
    # print(var)
    print(a)
    print(b)
    print(c)
    lambda 

if __name__ == "__main__":
    main()
