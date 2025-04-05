import datetime


def main():
    list_a = []
    list_b = list()
    list_c = [3,4,5, "문자열입니다.", True]
    print(list_a, list_b, list_c)
    print(type(list_a), type(list_b), type(list_c))
    ptime = datetime.datetime.now()
    list_d = [1, 2, 3.3, "choi", False, ptime]
    print(list_d, list_d[3][2]) # 'o'

if __name__ == "__main__":
    main()
