from classes.gamestate import GameState
from classes.pricelist import PriceList


def main():

    game = GameState()

    from_system_id = input("What system are you trading from? ").lower()
    while from_system_id not in game.systems:
        from_system_id = input(f"{from_system_id} is not a valid system. Try again: ")
    from_system = game.systems[from_system_id]
    to_system_id = input("What system are you going to? ").lower()
    if to_system_id not in game.systems:
        to_system_id = input(f"{to_system_id} is not a valid system. Try again: ")
    to_system = game.systems[to_system_id]

    best_trades = PriceList()

    # for each base in the from system
    for from_base_id in from_system.bases:
        # find each commodity it is selling
        from_base = game.bases[from_base_id]
        for commodity_id in from_base.commodities_to_buy:
            buy_price = from_base.commodity_prices[commodity_id]
            # find the best sell price for each base in the to system
            for to_base_id in to_system.bases:
                to_base = game.bases[to_base_id]
                if commodity_id in to_base.commodity_prices:
                    sell_price = to_base.commodity_prices[commodity_id]
                    profit = sell_price - buy_price
                    if profit > 0:
                        cargo_space = game.commodities[commodity_id].volume
                        if cargo_space == 0:
                            cargo_space = 1
                        profit_per_cargo = int(profit/cargo_space)
                        best_trades.add_price(
                            price=profit_per_cargo,
                            identifier=(commodity_id, from_base_id, to_base_id)
                        )

    current = best_trades.top

    while current:
        commodity_id = current.identifier[0]
        commodity_name = game.commodities[commodity_id].name
        from_base_id = current.identifier[1]
        from_base_name = game.bases[from_base_id].name
        buy_price = game.bases[from_base_id].commodity_prices[commodity_id]
        to_base_id = current.identifier[2]
        to_base_name = game.bases[to_base_id].name
        sell_price = game.bases[to_base_id].commodity_prices[commodity_id]
        profit_per_cargo = current.price
        print(f"Buy {commodity_name} at {from_base_name} for {buy_price}.")
        print(f"Sell at {to_base_name} for {sell_price} ({profit_per_cargo} profit per cargo space)")

        current = current.next


if __name__ == '__main__':
    main()
