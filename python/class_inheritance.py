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
    # print(choi.get_graduate_sum())

if __name__ == "__main__":
    main()
