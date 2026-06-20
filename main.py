import pandas as pd

from src.c_a import clean_data, top_3

def main():
    path = input("Enter file path ")
    data = clean_data(path)
    top = top_3(data)
    print(top)

if __name__ == "__main__":
    main()