# from test_a.functionEx import print_3_time, print_n_time, print_var
# from test_a import print_3_time, print_n_time, print_var
import test_a
from class_strudent import Student


class Graduated_Student(Student):
    def __init__(self, name, korean, math, english, science, art, job, *a, **kwargs):
        super().__init__(name, korean, math, english, science, *a, **kwargs)
        self.art = art
        self.job = job

    def get_sum(self):
        return self.get_average()*5 - 10

def main():
    park = Student("choi", 43, 63, 64 ,34)
    choi = Graduated_Student("choi", 43, 63, 64 ,34, 50, "teacher")
    print(choi.get_average())
    students = [park, choi]
    for student in students:
        print(student.get_sum())
    print(isinstance(choi, Graduated_Student)) # True
    print(isinstance(choi, Student)) # True
    print(isinstance(choi, int)) # False
    print(isinstance(choi, object)) # int dict list 내장 클래스 예외
    print(isinstance(int, object))
    print(isinstance(float, object))
    print(test_a.print_var)
    test_a.print_3_time()

if __name__ == "__main__":
    main()
