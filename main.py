from Character import *
from Dungeon import Level

if __name__ == "__main__":
    aanks = Player("Aanks")

    level_1 = Level(1)
    level_1.create()
    level_1.run(aanks)


