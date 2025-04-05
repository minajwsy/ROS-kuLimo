def power(n: int) -> int:
    return n * n

def under_10(n: int) -> bool:
    return n < 10


def main():
    li = [i+1 for i in range(20)]
    output_map = map(power, li)
    output_filter = filter(under_10, li)
    print("map 의 결과", list(output_map))
    print("filter 의 결과", list(output_filter))

if __name__ == "__main__":
    main()
