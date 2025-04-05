class Student(object):
    count = 0 # 클래스 변수
    students = []
    def __init__(self, name, korean, math, english, science, *a, **kwargs):
        # (*this) = self
        self.name = name # a.name self -> a
        self.korean = korean
        self.math = math
        self.english = english
        self.science = science
        self.sum = 0
        Student.count += 1
        Student.students.append(self)
        print(f"{Student.count} 번째 학생이 생성 되었습니다.")

    def get_sum(self):
        sum = self.korean + self.math + self.english + self.science
        return sum

    def get_calculated_sum(self):
        return self.sum

    def get_average(self):
        return (self.korean + self.math + self.english + self.science) / 4
    
    @classmethod
    def print(cls):
        print(f"현재 총 학생수는 {cls.count}명 입니다.")
        for student in cls.students:
            print(student)

    def __str__(self):
        return f"Name : {self.name}, Average : {self.get_average()}"

    def __eq__(self, value):
        if isinstance(value, Student):
            return self.get_sum() == value.get_sum()
        elif isinstance(value, int):
            return self.get_sum() == value
        else:
            raise ValueError("인트도 아니고 스트던트도 아님")


def main():
    Student("choi", 10, 20, 15, 17)
    Student("pack", 20, 20 ,18, 17)
    Student("Jung", 20, 10, 17, 15)
    print(Student.students[0], Student.students[1])
    a= Student.students[0]
    b= Student.students[1]
    c= Student.students[2]
    print(a.get_calculated_sum())
    print(a.get_average())
    try:
        if a == c:
            print("a 의 총점과 c 의 총점이 같다.")
        else:
            print("a 와 c 의 총점은 다르다.")

        if b == 75:
            print("b 의 총점은 75 이다.")
        else:
            print("b 의 총점은 75 가 아니다.")
    except ValueError as e:
        print("에러 발생", e)
    except Exception:
        print("Exception")
    else:
        print("정상 작동했다.")
    print(f"현재 생성된 총 학생 수는 {Student.count} 명 입니다.")
    Student.print()
    # print(f"현재 생성된 총 학생 수는 {a.count} 명 입니다.")
    # a.print()

if __name__ == "__main__":
    main()
