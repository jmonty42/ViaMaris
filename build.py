#!/usr/bin/env python3
import re
import flint
import os

from classes.commodity import Commodity
from classes.base import Base
from classes.pricelist import PriceList

# This is found in the EXE\flhook_plugins\ foler
OVERRIDE_FILE = "prices.cfg"


def main():
    flint.set_install_path(os.environ['FREELANCER_FOLDER'])

    # First read in the names of the systems
    systems = {}
    flint_systems: flint.routines.EntitySet[flint.routines.System] = flint.routines.get_systems()

    # Add bases by system
    bases = {}
    flint_system: flint.routines.System
    for flint_system in flint_systems:
        systems[flint_system.nickname.lower()] = flint_system.name()
        base: flint.routines.BaseSolar
        for base in flint_system.bases():
            bases[base.base.lower()] = Base(
                name=base.name(),
                nickname=base.base.lower(),
                system=flint_system.nickname.lower()
            )
            buying_commodities = base.universe_base().buys()
            for commodity in buying_commodities:
                bases[base.base.lower()].commodity_prices[commodity.nickname.lower()] = \
                    buying_commodities[commodity]
            selling_commodities = base.universe_base().sells()
            for commodity in selling_commodities:
                bases[base.base.lower()].commodity_prices[commodity.nickname.lower()] = \
                    selling_commodities[commodity]
                bases[base.base.lower()].commodities_to_buy.add(commodity.nickname.lower())

    # Next read in the names of the commodities
    commodities = {}
    flint_commodities = flint.get_commodities()

    for fl_commodity in flint_commodities:
        new_commodity = Commodity(name=fl_commodity.name(), price=fl_commodity.price())
        new_commodity.volume = int(fl_commodity.volume)
        commodities[fl_commodity.nickname.lower()] = new_commodity

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
            base_id = result.group(1).lower()
            commodity = result.group(2).lower()
            price = int(float(result.group(3)))
            try:
                bases[base_id].commodity_prices[commodity] = price
            except KeyError:
                print("ERROR: unknown base: " + base_id)
                continue
            can_buy = result.group(4) == "0"
            if can_buy:
                bases[base_id].commodities_to_buy.add(commodity)
            else:
                bases[base_id].commodities_to_buy.discard(commodity)
            continue
        elif "MarketGood" in line and ";Market" not in line:
            print("ERROR: line in override file should have matched but didn't: " + line)

    # calculate the best prices for each commodity
    best_trades = PriceList(max_length=20)

    for commodity in commodities:
        for base_id in bases:
            if bases[base_id].system == "iw09":
                # ignore the Bastille Prison System
                continue
            if commodity in bases[base_id].commodity_prices:
                price = bases[base_id].commodity_prices[commodity]
                commodities[commodity].price_map[base_id] = price
                commodities[commodity].best_sell_prices.add_price(price, base_id)
                if commodity in bases[base_id].commodities_to_buy:
                    commodities[commodity].best_buy_prices.add_price(price, base_id)
        if commodities[commodity].best_buy_prices.length > 0 and \
                commodities[commodity].best_sell_prices.length > 0:
            diff = commodities[commodity].best_sell_prices.top.price - commodities[commodity].best_buy_prices.top.price
            cargo_space = 1 if commodities[commodity].volume == 0 else commodities[commodity].volume
            best_trades.add_price(int(diff / cargo_space), commodity)

    print("Top 20 most lucrative commodities:")
    current = best_trades.top
    while current:
        base: Base = bases[commodities[current.base].best_buy_prices.top.base]
        print("Buy {} at {} ({}) in {} ({}) for {} ({} cargo)".format(
            commodities[current.base].name,
            base.name,
            base.nickname,
            systems[base.system],
            base.system,
            base.commodity_prices[current.base],
            commodities[current.base].volume
        ))
        base: Base = bases[commodities[current.base].best_sell_prices.top.base]
        print("Sell it at {} ({}) in {} ({}) for {} ({} profit per cargo space)".format(
            base.name,
            base.nickname,
            systems[base.system],
            base.system,
            base.commodity_prices[current.base],
            current.price
        ))
        current = current.next


if __name__ == '__main__':
    main()
