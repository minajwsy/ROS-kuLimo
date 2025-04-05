class Student:
    def __init__(self, name, korean, math, english, science, *a, **kwargs):
        # (*this) = self
        self.name = name # a.name self -> a
        self.korean = korean
        self.math = math
        self.english = english
        self.science = science
        self.sum = 0

    def get_sum(self):
        sum = self.korean + self.math + self.english + self.science
        return sum

    def get_calculated_sum(self):
        return self.sum

    def get_average(self):
        return (self.korean + self.math + self.english + self.science) / 4


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
    # print(a.get_sum())
    print(a.get_calculated_sum())
    print(a.get_average())

if __name__ == "__main__":
    main()
