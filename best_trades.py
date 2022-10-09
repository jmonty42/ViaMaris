#!/usr/bin/env python3

from classes.commodity import Commodity
from classes.base import Base
from classes.pricelist import PriceList
from classes.gamestate import GameState


def main():

    game = GameState()

    # calculate the best prices for each commodity
    best_trades = PriceList(max_length=20)

    for commodity_id in game.commodities:
        for base_id in game.bases:
            if game.bases[base_id].system == "iw09":
                # ignore the Bastille Prison System
                continue
            if commodity_id in game.bases[base_id].commodity_prices:
                price = game.bases[base_id].commodity_prices[commodity_id]
                game.commodities[commodity_id].price_map[base_id] = price
                game.commodities[commodity_id].best_sell_prices.add_price(price, base_id)
                if commodity_id in game.bases[base_id].commodities_to_buy:
                    game.commodities[commodity_id].best_buy_prices.add_price(price, base_id)
        if game.commodities[commodity_id].best_buy_prices.length > 0 and \
                game.commodities[commodity_id].best_sell_prices.length > 0:
            diff = game.commodities[commodity_id].best_sell_prices.top.price - \
                   game.commodities[commodity_id].best_buy_prices.top.price
            cargo_space = 1 if game.commodities[commodity_id].volume == 0 else game.commodities[commodity_id].volume
            best_trades.add_price(int(diff / cargo_space), commodity_id)

    print("Top 20 most lucrative commodities:")
    current = best_trades.top
    while current:
        base: Base = game.bases[game.commodities[current.string_id].best_buy_prices.top.string_id]
        print("Buy {} at {} ({}) in {} ({}) for {} ({} cargo)".format(
            game.commodities[current.string_id].name,
            base.name,
            base.base_id,
            game.systems[base.system],
            base.system,
            base.commodity_prices[current.string_id],
            game.commodities[current.string_id].volume
        ))
        base: Base = game.bases[game.commodities[current.string_id].best_sell_prices.top.string_id]
        print("Sell it at {} ({}) in {} ({}) for {} ({} profit per cargo space)".format(
            base.name,
            base.base_id,
            game.systems[base.system],
            base.system,
            base.commodity_prices[current.string_id],
            current.price
        ))
        current = current.next


if __name__ == '__main__':
    main()
