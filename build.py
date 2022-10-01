#!/usr/bin/env python3
import re
from classes.good import Good

CARGO_NAMES_FILE = "GAMEDATA_cargo.txt"
GOODS_FILE = "goods.ini"


def main():
    goods_table = {}
    with open(CARGO_NAMES_FILE, 'r') as names_file:
        names = names_file.readlines()

    name_regex = re.compile("^\d+ = ([\w-]+), (.+)$")
    for line in names:
        result = name_regex.match(line)
        if result:
            goods_table[result.group(1)] = Good(name=result.group(2))
        else:
            print("Error reading line: '" + line + "', skipping")
    print("Found " + str(len(goods_table)) + " goods.")

    """ DEBUG
    for key in goods_table:
        print(key + ": " + str(goods_table[key]))
    """


if __name__ == '__main__':
    main()