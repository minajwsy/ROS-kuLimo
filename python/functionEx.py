def print_3_time():
    print("안녕하세요")
    print("안녕하세요")
    print("안녕하세요")
    a = 100
    return "ok", 1, "complete", a

def print_n_time(n):
    for i in range(n):
        print("n안녕하세요.")

def main():
    re = print_3_time()
    print_n_time(3)
    print(re)

if __name__ == "__main__":
    main()



