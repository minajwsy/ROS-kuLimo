def process_order(customer_name, *items, **details):
    """
    주문 처리 함수
    - customer_name: 고정 매개변수 (고객명)
    - *items: 가변인수 (주문 상품들)
    - **details: 키워드인수 (주문 세부사항)
    """
    print(f"고객명: {customer_name}")
    
    print("주문 상품:")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    
    print("주문 세부사항:")
    for key, value in details.items():
        print(f"  {key}: {value}")
    
    print("-" * 30)

# 함수 호출 예시들
print("=== 예시 1: 기본 사용 ===")
process_order("박정우", "피자", "콜라", 
              address="서울시 서초구", 
              phone="010-1234-5678", 
              payment="카드")

print("\n=== 예시 2: 다양한 개수의 인수 ===")
process_order("이영희", "치킨", "맥주", "감자튀김", "치즈볼",
              address="부산시 해운대구",
              delivery_time="30분",
              special_request="매운맛으로")

print("\n=== 예시 3: 최소한의 인수만 사용 ===")
process_order("박민수", "햄버거",
              phone="010-9876-5432")
