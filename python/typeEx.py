def main():
    abc = int()
    abc = 4 # abc --class of int -> object
    print(abc, type(abc))
    abc = 4.5 # abc float
    print(abc, type(abc))
    abc = "this is python" # abc str
    print(abc, type(abc))
    # format -- f-string
    abc = "fstring"
    number = 3.141592
    print(f"string string {abc} pi : {number:.3}")

if __name__ == "__main__":
    main()
