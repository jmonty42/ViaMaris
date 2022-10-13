from classes.base import Base
from classes.gamestate import GameState
from classes.pricelist import PriceList


def main():

    game = GameState()

    best_trades = PriceList(max_length=20)

    for commodity_id in game.commodities:
        if game.commodities[commodity_id].best_buy_prices.length > 0 and \
                game.commodities[commodity_id].best_sell_prices.length > 0:
            diff = game.commodities[commodity_id].best_sell_prices.top.price - \
                   game.commodities[commodity_id].best_buy_prices.top.price
            cargo_space = 1 if game.commodities[commodity_id].volume == 0 else game.commodities[commodity_id].volume
            best_trades.add_price(int(diff / cargo_space), commodity_id)

    print("Top 20 most lucrative commodities:")
    current = best_trades.top
    while current:
        base: Base = game.bases[game.commodities[current.identifier].best_buy_prices.top.identifier]
        print("Buy {} at {} ({}) in {} ({}) for {} ({} cargo)".format(
            game.commodities[current.identifier].name,
            base.name,
            base.base_id,
            game.systems[base.system].name,
            base.system,
            base.commodity_prices[current.identifier],
            game.commodities[current.identifier].volume
        ))
        base: Base = game.bases[game.commodities[current.identifier].best_sell_prices.top.identifier]
        print("Sell it at {} ({}) in {} ({}) for {} ({} profit per cargo space)".format(
            base.name,
            base.base_id,
            game.systems[base.system].name,
            base.system,
            base.commodity_prices[current.identifier],
            current.price
        ))
        current = current.next


if __name__ == '__main__':
    main()
