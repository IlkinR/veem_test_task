import os
import sys
import hashlib


def check_has_sums(dir_filer, input_file):
    with open(input_file, 'r') as file:
        for line in file:
            bin_file, algorithm, hashcode = line.split()

            try:
                with open(os.path.join(dir_filer, bin_file), 'rb') as f:
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
        print("Input is wrong. Use format <your program> <path to the input file> <path to the directory containing "
              "the files to check>")
        sys.exit()

    check_has_sums(sys.argv[2], sys.argv[1])
