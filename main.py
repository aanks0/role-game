import database
from Character import *
from Dungeon import Level
from database import *

if __name__ == "__main__":
    player_name = "Aanks2"
    level_1 = Level(1)
    level_1.create()

    connection = database.open_db("role-game")
    create_table(connection)

    player = load_save(connection, player_name)
    if not player:
        init_save(connection, name=player_name)
        player = Player(player_name)
    level_1.run(player, connection)
    database.close_db(connection)

