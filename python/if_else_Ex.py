kor, eng, mat, sci = map(int, input().split())

if 0 <= kor <=100 and 0 <= eng <=100 and 0 <= mat <=100 and 0 <= sci <=100:
    ave = (kor + eng + mat + sci)/4
    if ave >= 80:
        print('합격')
    else:
        print('불합격')
else:
    print('잘못된 점수')