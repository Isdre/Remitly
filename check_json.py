import sys
from JsonChecker import JsonChecker

if __name__ == "__main__":
    print(sys.argv[1])
    checker = JsonChecker(sys.argv[1])
    print(checker.check())