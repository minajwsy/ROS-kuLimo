def print_n_times(n : int, *value):
    print(type(value))
    for _ in range(n):
        for v in value:
            print(v)
        print()

def print_n_times_default(value, n=3):
    for _ in range(n):
        print(value)

def print_n_times_keyword(value, *values, a=3, b=4, c=5):
    for _ in range(a):
        print(a, b, c)
        print(value)
        for v in values:
            print(values)

def print_n_times_keyword_variable(value, *values, a=3, b=4, c=5, **kwargd):
    print(type(kwargd)) # dictionary
    for _ in range(a):
        print(a, b, c)
        print(value)
        for v in values:
            print(values)
    for k, v in kwargd.items():
        print(k,v)

def main():
    print_n_times(3, "abc", "def", "안녕", "하세요.")
    print_n_times_default("안녕하세요.")
    print()
    print_n_times_default("안녕하세요.", 5)
    print_n_times_keyword("안녕하세요", 5, "abc", "def")
    print()
    print_n_times_keyword("안녕하세요", 5, "abc", "def", a=6, b=7)
    print()
    print_n_times_keyword_variable("안녕하세요", 5, "abc", "def", a=6, b=7, new="new 의 값")

if __name__ == "__main__":
    main()
