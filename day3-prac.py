#문제1 :: 딕셔너리 만들기

d={'name':'홍길동','birth':'1128','age':30}
print("문제1****************\n",type(d),d)

#문제2 :: 50점 이상의 총합
#다음은 A학급 학생의 점수를 나타내는 리스트이다. 다음 리스트에서 50점 이상의 점수들의 총합을 구하시오.
#A = [20, 55, 67, 82, 45, 33, 90, 87, 100, 25]
A = [20, 55, 67, 82, 45, 33, 90, 87, 100, 25]
sum=0
for x in A:
    if x >= 50:
        sum=sum+x

print("문제2****************\n", sum)

# [문제3] 별 표시하기1
# while문을 이용하여아래와 같이 별(*)을 표시하는프로그램을 작성해 보자.
#  *
#  **
#  ***
#  ****
print("문제3****************\n")
for i in range(1,5):
    for j in range(0,i):
        print("*", end='')
    print("\n")

#문제4:: 학급의 평균 점수, for문을 이용하여 A 학급의 평균점수를 구해보자
#A = [70, 60, 55, 75, 95, 90, 80, 80, 85, 100]
sum=0
A = [70, 60, 55, 75, 95, 90, 80, 80, 85, 100]

for x in A:
    sum+=x

print("문제4****************\n",sum/len(A))

#문제5: 로또 중복 제거
import random
li=set()
while len(li) < 6:
    r=random.randint(1,45)
    li.add(r)

print("문제5****************\n",li)
