import hashlib
import os
import sys


class InvalidInputFormat(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def check_has_sums(dir_file: str, input_file: str):
    with open(input_file, 'r') as file:
        for line in file:
            bin_file, algorithm, hashcode = line.split()
            try:
                with open(os.path.join(dir_file, bin_file), 'rb') as f:
                    hasher = getattr(hashlib, algorithm)
                    hash_result = hasher(f.read()).hexdigest()
                    if hash_result == hashcode:
                        print(bin_file, "OK")
                    else:
                        print(bin_file, "FAIL")
            except FileNotFoundError:
                print(bin_file, "FILE NOT FOUND")


if __name__ == 'main':
    if len(sys.argv) != 3:
        raise InvalidInputFormat(
            "Input is wrong. Use format <your program> <path to the input file> <path to the directory containing "
            "the files to check>"
        )
    check_has_sums(dir_file=sys.argv[2], input_file=sys.argv[1])
