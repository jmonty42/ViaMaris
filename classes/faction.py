class Faction:

    def __init__(self, faction_id: str, name: str):
        self.faction_id = faction_id
        self.name = name
        # set of base ids that the faction owns
        self.bases_owned = set()
        # base_id -> set of tuples representing each bribe found in mbases.ini
        self.bribes: dict[str, tuple[int, int]] = {}
