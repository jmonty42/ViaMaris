from classes.faction import Faction
from classes.gamestate import GameState


def main():
    game = GameState()

    for faction_id in game.factions:
        # I think these are player factions
        if not faction_id.startswith("pf"):
            print(f"{faction_id}: {game.factions[faction_id].name}")

    faction_id = input("Enter a faction id: ").lower()
    while faction_id not in game.factions:
        faction_id = input("Ivalid id, try again: ").lower()

    faction = game.factions[faction_id]
    print(faction.name)
    print("Bases owned:")
    for base_id in faction.bases_owned:
        base_name = game.bases[base_id].name
        system_id = game.bases[base_id].system
        system_name = game.systems[system_id].name
        print(f"{base_name} ({base_id}) in {system_name} ({system_id})")
    print("Bribes found:")
    for base_id in faction.bribes:
        base_name = game.bases[base_id].name
        system_id = game.bases[base_id].system
        system_name = game.systems[system_id].name
        for bribe in faction.bribes[base_id]:
            bribe_num1 = bribe[0]
            bribe_num2 = bribe[1]
            print(f"{base_name} ({base_id}) in {system_name} ({system_id}): ({bribe_num1}, {bribe_num2})")


if __name__ == '__main__':
    main()
