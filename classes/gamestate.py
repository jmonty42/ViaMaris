import re
import flint
import os

from classes.commodity import Commodity
from classes.base import Base
from classes.pricelist import PriceList

# This is found in the EXE\flhook_plugins\ folder
OVERRIDE_FILE = "prices.cfg"


class GameState(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GameState, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.systems = {}
        self.bases = {}
        self.commodities = {}

        flint.set_install_path(os.environ['FREELANCER_FOLDER'])

        # First read in the names of the systems
        flint_systems: flint.routines.EntitySet[flint.routines.System] = flint.routines.get_systems()

        # Add bases by system
        flint_system: flint.routines.System
        for flint_system in flint_systems:
            self.systems[flint_system.nickname.lower()] = flint_system.name()
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
                self.bases[base_id] = Base(
                    name=base.name(),
                    base_id=base_id,
                    system=system_id
                )
                buying_commodities = base.universe_base().buys()
                for commodity in buying_commodities:
                    commodity_id = commodity.nickname.lower()
                    self.bases[base_id].commodity_prices[commodity_id] = buying_commodities[commodity]
                selling_commodities = base.universe_base().sells()
                for commodity in selling_commodities:
                    commodity_id = commodity.nickname.lower()
                    self.bases[base_id].commodity_prices[commodity_id] = selling_commodities[commodity]
                    self.bases[base_id].commodities_to_buy.add(commodity_id)

        # Next read in the names of the commodities
        flint_commodities = flint.get_commodities()

        for fl_commodity in flint_commodities:
            new_commodity = Commodity(name=fl_commodity.name(), price=fl_commodity.price())
            new_commodity.volume = int(fl_commodity.volume)
            self.commodities[fl_commodity.nickname.lower()] = new_commodity

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
                    self.bases[base_id].commodity_prices[commodity_id] = price
                except KeyError:
                    print("ERROR: unknown base: " + base_id)
                    continue
                can_buy = result.group(4) == "0"
                if can_buy:
                    self.bases[base_id].commodities_to_buy.add(commodity_id)
                else:
                    self.bases[base_id].commodities_to_buy.discard(commodity_id)
                continue
            elif "MarketGood" in line and ";Market" not in line:
                print("ERROR: line in override file should have matched but didn't: " + line)

