#!/usr/bin/env python3
import re
from classes.commodity import Commodity
from classes.base import Base
from classes.pricelist import PriceList

# GAMEDATA files are found in the IONCROSS folder of the game directory
COMMODITY_NAMES_FILE = "GAMEDATA_cargo.txt"
SYSTEM_NAMES_FILE = "GAMEDATA_systems.txt"
BASE_NAMES_FILE = "GAMEDATA_bases.txt"
# These .ini files are found in the DATA\EQUIPMENT\ folder
GOODS_FILE = "goods.ini"
MARKET_FILE = "market_commodities.ini"
# This is found in the EXE\flhook_plugins\ foler
OVERRIDE_FILE = "prices.cfg"


def main():
    # First read in the names of the commodities
    commodities = {}
    with open(COMMODITY_NAMES_FILE, 'r') as names_file:
        names = names_file.readlines()

    # https://regex101.com/r/uTcJWs/1
    name_regex = re.compile(r"^\d+ = ([\w-]+), (.+)$")
    for line in names:
        result = name_regex.match(line)
        if result:
            commodities[result.group(1).lower()] = Commodity(name=result.group(2))
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
            systems[result.group(1).lower()] = result.group(3)
        else:
            print("Error reading line from " + SYSTEM_NAMES_FILE + ": '" + line + "', skipping")
    print("Found " + str(len(systems)) + " systems.")

    """ DEBUG
    print(systems)
    """

    # Read in the base names
    bases = {}
    with open(BASE_NAMES_FILE, 'r') as bases_file:
        base_lines = bases_file.readlines()

    """
    https://regex101.com/r/iH04yW/1
    group1: base id
    group2: system id for the base
    group3: name of the base
    """
    base_regex = re.compile(r"^(([^_]+)\w+) = (.*)$")
    for line in base_lines:
        result = base_regex.match(line)
        if result:
            bases[result.group(1).lower()] = Base(name=result.group(3), system=result.group(2).lower())
        else:
            print("Error reading line from " + BASE_NAMES_FILE + ": '" + line + "', skipping")
    print("Found " + str(len(bases)) + " bases.")

    """ DEBUG
    for key in bases:
        print(key + ": " + bases[key].name + " (" + systems[bases[key].system] + ")")
    """

    # get the base prices for each commodity
    with open(GOODS_FILE, 'r') as goods_file:
        prices_lines = goods_file.readlines()

    name_regex = re.compile(r"^nickname = ([\w\-]+)\s*$")
    price_regex = re.compile(r"^price = (\d+)\s*$")

    current_commodity = ""
    # found_price = True
    price_count = 0
    line_num = -1
    for line in prices_lines:
        line_num += 1
        if "[Good]" in line:
            """ DEBUG
            if not found_price:
                print("Did not find a price for commodity '" + current_commodity + "'")
            """
            current_commodity = ""
            # found_price = False
            continue
        result = name_regex.match(line)
        if result:
            current_commodity = result.group(1).lower()
            continue
        result = price_regex.match(line)
        if result:
            if not current_commodity:
                print("Somehow found a price but not a commodity on line " + str(line_num))
                continue
            if current_commodity not in commodities:
                """ DEBUG
                print("Found a price for '" + current_commodity + "', but it wasn't in our list, adding it.")
                """
                commodities[current_commodity] = Commodity(name=current_commodity)
            commodities[current_commodity].base_price = float(result.group(1))
            # found_price = True
            price_count += 1
            continue

    print("Found " + str(price_count) + " prices")

    """ DEBUG
    for key in commodities:
        print(str(commodities[key]))
    """

    # get the buy/sell prices for each base
    with open(MARKET_FILE, 'r') as market_file:
        market_lines = market_file.readlines()

    base_regex = re.compile(r"^base\s*=\s*(\S+)\s*$")
    """
    https://regex101.com/r/s9zv3C/1
    group1: commodity id
    group2: "0" = player can buy the commodity from the base (but can also sell it at the same price)
    group3: multiplier of the base price for that commodity
    """
    buy_sell_regex = re.compile(r"^MarketGood = ([^,]+),\s*\d*,\s*-?\d*.?\d*,\s*\d*,\s*\d*,\s*(\d*),\s*(\d*\.?\d*)\s*$")

    current_base = ""
    for line in market_lines:
        result = base_regex.match(line)
        if result:
            current_base = result.group(1).lower()
            continue
        result = buy_sell_regex.match(line)
        if result:
            commodity = result.group(1).lower()
            float_multiplier = float(result.group(3))
            try:
                price = int(commodities[commodity].base_price * float_multiplier)
            except KeyError:
                print("ERROR: " + commodity + " was not found in the commodities dictionary")
                continue
            try:
                bases[current_base].commodity_prices[commodity] = price
                if result.group(2) == "0":
                    bases[current_base].commodities_to_buy.add(commodity)
            except KeyError:
                if "_miner" not in current_base:
                    # xxx_miner bases show up with a single line for water, ignoring
                    print("ERROR: " + current_base + " was not found in the bases dictionary")
            continue
        elif "MarketGood" in line and ";MarketGood" not in line:  # ; = commented out line
            print("ERROR: line  should have matched the 'MarketGood' pattern but didn't: " + line)

    # process the override file
    with open(OVERRIDE_FILE, 'r') as override_file:
        override_lines = override_file.readlines()

    """
    https://regex101.com/r/w3smOd/2
    group1: base id
    group2: commodity id
    group3: new price (should override what is already set
    group4: "0" = player can buy this commodity from the base
    """
    override_regex = re.compile(r"^Market[Gg]ood\s*=\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*(\d)")

    for line in override_lines:
        result = override_regex.match(line)
        if result:
            base = result.group(1).lower()
            commodity = result.group(2).lower()
            price = int(float(result.group(3)))
            try:
                bases[base].commodity_prices[commodity] = price
            except KeyError:
                print("ERROR: unknown base: " + base)
                continue
            can_buy = result.group(4) == "0"
            if can_buy:
                bases[base].commodities_to_buy.add(commodity)
            else:
                bases[base].commodities_to_buy.discard(commodity)
            continue
        elif "MarketGood" in line and ";Market" not in line:
            print("ERROR: line in override file should have matched but didn't: " + line)

    """ DEBUG
    print("Commodity prices for Harrisburg Station:")
    for commodity in bases["li09_08_base"].commodity_prices:
        if commodity in bases["li09_08_base"].commodities_to_buy:
            print("Player can buy " + commodities[commodity].name + " from this base")
        print("{0}: {1}".format(commodities[commodity].name, bases["li09_08_base"].commodity_prices[commodity]))
    """

    # calculate the best prices for each commodity
    best_trades = PriceList(max_length=20)

    for commodity in commodities:
        for base in bases:
            if bases[base].system == "iw09":
                # ignore the Bastille Prison System
                continue
            if commodity in bases[base].commodity_prices:
                price = bases[base].commodity_prices[commodity]
                commodities[commodity].best_sell_prices.add_price(price, base)
                if commodity in bases[base].commodities_to_buy:
                    commodities[commodity].best_buy_prices.add_price(price, base)
        if commodities[commodity].best_buy_prices.length > 0 and \
                commodities[commodity].best_sell_prices.length > 0:
            diff = commodities[commodity].best_sell_prices.top.price - commodities[commodity].best_buy_prices.top.price
            best_trades.add_price(diff, commodity)

    print("Top 20 most lucrative commodities:")
    current = best_trades.top
    while current:
        base = bases[commodities[current.base].best_buy_prices.top.base]
        print("Buy {} at {} in {} for {}".format(
            commodities[current.base].name,
            base.name,
            systems[base.system],
            base.commodity_prices[current.base]
        ))
        base = bases[commodities[current.base].best_sell_prices.top.base]
        print("Sell it at {} in {} for {} ({} profit)".format(
            base.name,
            systems[base.system],
            base.commodity_prices[current.base],
            current.price
        ))
        current = current.next

    """ DEBUG
    print("Best places to sell " + commodities["commodity_xenos"].name + ":")
    current_node = commodities["commodity_xenos"].best_sell_prices.top
    while current_node:
        print(bases[current_node.base].name + ": " + str(current_node.price))
        current_node = current_node.next

    print("Best places to buy " + commodities["commodity_drillbits"].name + ":")
    current_node = commodities["commodity_drillbits"].best_buy_prices.top
    while current_node:
        print(bases[current_node.base].name + ": " + str(current_node.price))
        current_node = current_node.next

    print("Best places to sell " + commodities["commodity_drillbits"].name + ":")
    current_node = commodities["commodity_drillbits"].best_sell_prices.top
    while current_node:
        print(bases[current_node.base].name + ": " + str(current_node.price))
        current_node = current_node.next
    """


if __name__ == '__main__':
    main()
