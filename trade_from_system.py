from classes.gamestate import GameState
from classes.pricelist import PriceList


def main():

    game = GameState()

    system = input("What system are you trading from? ").lower()

    if system not in game.systems:
        print(f"{system} is not a valid system")

    best_trades = PriceList(max_length=10)

    for base_id in game.systems[system].bases:
        for commodity_id in game.bases[base_id].commodities_to_buy:
            buy_price = game.bases[base_id].commodity_prices[commodity_id]
            if commodity_id in game.commodities:
                if game.commodities[commodity_id].best_sell_prices.top:
                    top_sell_price = game.commodities[commodity_id].best_sell_prices.top.price
                    top_sell_base = game.commodities[commodity_id].best_sell_prices.top.string_id
                    cargo_space = 1 if game.commodities[commodity_id].volume == 0 \
                        else game.commodities[commodity_id].volume
                    profit = int((top_sell_price - buy_price)/cargo_space)
                    if profit > 0:
                        best_trades.add_price(price=profit, string_id=(base_id, commodity_id, top_sell_base))

    current = best_trades.top

    while current:
        base_id = current.string_id[0]
        base_name = game.bases[base_id].name
        commodity_id = current.string_id[1]
        commodity_name = game.commodities[commodity_id].name
        buy_price = game.bases[base_id].commodity_prices[commodity_id]
        sell_base_id = current.string_id[2]
        sell_base_name = game.bases[sell_base_id].name
        system_name = game.systems[game.bases[sell_base_id].system].name
        sell_price = game.bases[sell_base_id].commodity_prices[commodity_id]
        print(f"At {base_name} buy {commodity_name} for {buy_price}")
        print(f"Sell it to {sell_base_name} in {system_name} for {sell_price} ({current.price} profit per cargo space)")
        current = current.next


if __name__ == '__main__':
    main()
