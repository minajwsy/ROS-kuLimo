def main():
    li = [i+1 for i in range(20)]
    output_map = map(lambda x : x * x, li)
    output_filter = filter(lambda x : x < 10, li)
    print("map 의 결과", list(output_map))
    print("filter 의 결과", list(output_filter))

    a = lambda x, y : x+y
    print(a(2,3))

if __name__ == "__main__":
    main()
