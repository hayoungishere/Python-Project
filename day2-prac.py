#00
#   (10,20,30) 튜플에 40,50 데이터를 추가하여
#   (10,20,30,40,50) 튜플을 만들어 출력해라

x=(10,20,30)
x=list(x)
x.extend([40,50])
x=tuple(x)
print(x, " type is ", type(x))

# [문제1] 문자열 나누기
# 홍길동 씨의 주민등록번호는 881120-1068234이다. 홍길동씨의 주민등록번호를 연월일(YYMMDD) 부분과 그 뒤의 숫자 부분으로 나누어 출력해 보자.

ssn="881120-1068234"
print(ssn.split('-'))

# [문제2] 문자열 인덱싱
# 주민등록번호 뒷자리의 맨 첫 번째 숫자는 성별을 나타낸다. 주민등록번호에서 성별을 나타내는 숫자를 출력해 보자.
# >>> pin = "881120-1068234"

pin = "881120-1068234"
sex=pin.split('-')[1]
print(sex[0])

# [문제3] 문자열 바꾸기1
# 다음과 같은 문자열이 있다.
# a:b:c:d
# 문자열의 replace 함수를 이용하여 위 문자열을 다음과 같이 고치시오.
# a#b#c#d
print("#".join('abcd'))

# [문제4] 문자열 바꾸기2
# 다음과 같은 문자열이 있다.
# a:b:c:d
# 문자열의 split와 join 함수를 이용하여 위 문자열을 다음과 같이 고치시오.
# a#b#c#d
# (힌트. 문자열을 ":"으로 split하면 리스트 자료형이 리턴된다. 리스트 자료형은 문자열과 마찬가지로 join이 가능하다.)

str="a:b:c:d"
strlist=str.split(':')
print("#".join(strlist))


# [문제5] 리스트 조인
# ['Life', 'is', 'too', 'short'] 라는 리스트를 Life is too short라는 문자열로 만들어 출력해 보자.
# (힌트. 문자열의 join 함수를 이용해 보자.)

li=['Life', 'is', 'too', 'short']
print(" ".join(li))

# [문제6] 리스트 정렬
# [1, 3, 5, 4, 2]라는 리스트를 [5, 4, 3, 2, 1]로 만들어보자.
# (힌트. 리스트의 내장함수인 sort와 reverse를 활용해 보자.)

li=list()
li=[1,3,5,4,2]
li.sort()
li.reverse()
print(li)

# [문제7] 리스트 생성
# [5, 3, 1, -1, -3, -5, -7, -9]리스트가 출력되게 만들어보자. (range 사용)
li=list(range(5,-10,-2))
print(li)



# [문제8] 합계 출력
# 정수 세 개를 입력받고 합계가 출력되게 만들어보자.
# *실행 결과 예시*
# -10 20 30 (입력)
# 40

a=int(input("정수 세 개를 입력해 주세요\n"))
b=int(input())
c=int(input())
print(a+b+c)







