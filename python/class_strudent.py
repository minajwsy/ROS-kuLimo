class Student:
    def __init__(self, name, korean, math, english, science, *a, **kwargs):
        self.name = name # a.name self -> a
        self.korean = korean
        self.math = math
        self.english = english
        self.science = science
        # (*this) = self


def main():
    a = Student("choi", 10, 20, 15, 17)
    b = Student("pack", 20, 20 ,18, 17)
    print(a, b)
    print(a.name)
    print(a.korean)
    print(a.science)
    print(b.name)
    print(b.korean)
    print(b.science)

if __name__ == "__main__":
    main()
