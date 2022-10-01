#!/usr/bin/env python3
import re
from classes.good import Good

CARGO_NAMES_FILE = "GAMEDATA_cargo.txt"
SYSTEM_NAMES_FILE = "GAMEDATA_systems.txt"
GOODS_FILE = "goods.ini"


def main():
    # First read in the name of the commodities
    goods_table = {}
    with open(CARGO_NAMES_FILE, 'r') as names_file:
        names = names_file.readlines()

    # https://regex101.com/r/uTcJWs/1
    name_regex = re.compile(r"^\d+ = ([\w-]+), (.+)$")
    for line in names:
        result = name_regex.match(line)
        if result:
            goods_table[result.group(1)] = Good(name=result.group(2))
        else:
            print("Error reading line from " + CARGO_NAMES_FILE + ": '" + line + "', skipping")
    print("Found " + str(len(goods_table)) + " goods.")

    """ DEBUG
    for key in goods_table:
        print(key + ": " + str(goods_table[key]))
    """

    # Next read in the names of the systems
    systems = {}
    with open(SYSTEM_NAMES_FILE, 'r') as systems_file:
        system_lines = systems_file.readlines()

    # https://regex101.com/r/2WzcpX/1
    system_regex = re.compile(r"^([a-zA-Z]{2}[0-9]{1,2}[a-z]?) = ([A-Z]{2} )?([^\(\n]+)")
    for line in system_lines:
        result = system_regex.match(line)
        if result:
            systems[result.group(1)] = result.group(3)
        else:
            print("Error reading line from " + SYSTEM_NAMES_FILE + ": '" + line + "', skipping")
    print("Found " + str(len(systems)) + " systems.")

    """ DEBUG
    print(systems)
    """


if __name__ == '__main__':
    main()
