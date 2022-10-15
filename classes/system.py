class System:

    system_id: str
    name: str
    bases: set[str]

    def __init__(self, system_id, name):
        self.system_id = system_id
        self.name = name
        self.bases = set()
