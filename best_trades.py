#!/usr/bin/env python3
import re
import flint
import os

from classes.commodity import Commodity
from classes.base import Base
from classes.pricelist import PriceList

# This is found in the EXE\flhook_plugins\ folder
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
            system_id = flint_system.nickname.lower()
            base_id = base.base.lower()
            if not base_id.startswith(system_id):
                # two bases currently have mismatched base names, which is annoying
                match base_id:
                    case "br04_01_base":
                        base_id = "bw01_01_base"
                    case "rh10_02_base":
                        base_id = "rh01_01_base"
            bases[base_id] = Base(
                name=base.name(),
                base_id=base_id,
                system=system_id
            )
            buying_commodities = base.universe_base().buys()
            for commodity in buying_commodities:
                bases[base_id].commodity_prices[commodity.nickname.lower()] = \
                    buying_commodities[commodity]
            selling_commodities = base.universe_base().sells()
            for commodity in selling_commodities:
                bases[base_id].commodity_prices[commodity.nickname.lower()] = \
                    selling_commodities[commodity]
                bases[base_id].commodities_to_buy.add(commodity.nickname.lower())

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
            commodity_id = result.group(2).lower()
            price = int(float(result.group(3)))
            try:
                bases[base_id].commodity_prices[commodity_id] = price
            except KeyError:
                print("ERROR: unknown base: " + base_id)
                continue
            can_buy = result.group(4) == "0"
            if can_buy:
                bases[base_id].commodities_to_buy.add(commodity_id)
            else:
                bases[base_id].commodities_to_buy.discard(commodity_id)
            continue
        elif "MarketGood" in line and ";Market" not in line:
            print("ERROR: line in override file should have matched but didn't: " + line)

    # calculate the best prices for each commodity
    best_trades = PriceList(max_length=20)

    for commodity_id in commodities:
        for base_id in bases:
            if bases[base_id].system == "iw09":
                # ignore the Bastille Prison System
                continue
            if commodity_id in bases[base_id].commodity_prices:
                price = bases[base_id].commodity_prices[commodity_id]
                commodities[commodity_id].price_map[base_id] = price
                commodities[commodity_id].best_sell_prices.add_price(price, base_id)
                if commodity_id in bases[base_id].commodities_to_buy:
                    commodities[commodity_id].best_buy_prices.add_price(price, base_id)
        if commodities[commodity_id].best_buy_prices.length > 0 and \
                commodities[commodity_id].best_sell_prices.length > 0:
            diff = commodities[commodity_id].best_sell_prices.top.price - \
                   commodities[commodity_id].best_buy_prices.top.price
            cargo_space = 1 if commodities[commodity_id].volume == 0 else commodities[commodity_id].volume
            best_trades.add_price(int(diff / cargo_space), commodity_id)

    print("Top 20 most lucrative commodities:")
    current = best_trades.top
    while current:
        base: Base = bases[commodities[current.string_id].best_buy_prices.top.string_id]
        print("Buy {} at {} ({}) in {} ({}) for {} ({} cargo)".format(
            commodities[current.string_id].name,
            base.name,
            base.base_id,
            systems[base.system],
            base.system,
            base.commodity_prices[current.string_id],
            commodities[current.string_id].volume
        ))
        base: Base = bases[commodities[current.string_id].best_sell_prices.top.string_id]
        print("Sell it at {} ({}) in {} ({}) for {} ({} profit per cargo space)".format(
            base.name,
            base.base_id,
            systems[base.system],
            base.system,
            base.commodity_prices[current.string_id],
            current.price
        ))
        current = current.next


if __name__ == '__main__':
    main()
