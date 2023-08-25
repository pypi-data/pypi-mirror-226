import sys

from oltea_dummy_pack import mama, rares


def main():
    if len(sys.argv) > 2:
        mama.mama_func_1(sys.argv[1])
    elif len(sys.argv) > 1:
        mama.mama_func_2()

    else:
        rares.add_three_numbers(1, 2, 3)


if __name__ == "__main__":
    main()
