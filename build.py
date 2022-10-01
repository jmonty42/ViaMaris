#!/usr/bin/env python3
import re
from classes.commodity import Commodity

COMMODITY_NAMES_FILE = "GAMEDATA_cargo.txt"
SYSTEM_NAMES_FILE = "GAMEDATA_systems.txt"
GOODS_FILE = "goods.ini"


def main():
    # First read in the name of the commodities
    commodities = {}
    with open(COMMODITY_NAMES_FILE, 'r') as names_file:
        names = names_file.readlines()

    # https://regex101.com/r/uTcJWs/1
    name_regex = re.compile(r"^\d+ = ([\w-]+), (.+)$")
    for line in names:
        result = name_regex.match(line)
        if result:
            commodities[result.group(1)] = Commodity(name=result.group(2))
        else:
            print("Error reading line from " + COMMODITY_NAMES_FILE + ": '" + line + "', skipping")
    print("Found " + str(len(commodities)) + " goods.")

    """ DEBUG
    for key in commodities:
        print(key + ": " + str(commodities[key]))
    """

    # Next read in the names of the systems
    systems = {}
    with open(SYSTEM_NAMES_FILE, 'r') as systems_file:
        system_lines = systems_file.readlines()

    """
    https://regex101.com/r/2WzcpX/1
    group1: the system id that is used everywhere (BR14, FP7, St03b, etc)
    group2: two-letter abbreviation denoting what region the system is in (Liberty, Bretonia, etc), ignored
    group3: display name of the system (California, Tau-29, New Cambria, etc)
    group4: some systems have a faction in parenthesis in the text file ("(Xenos)", "(Coalition)", etc), ignored
    """
    system_regex = re.compile(r"^([a-zA-Z]{2}[0-9]{1,2}[a-z]?) = ([A-Z]{2} )?([^\(\n]+)(\s\(.*\))?$")
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
