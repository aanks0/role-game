import sqlite3
from sqlite3 import Connection

from Character import Player


def open_db(db_name: str):
    """

    :return: sqlite Connection
    """
    return sqlite3.connect(f"{db_name}.db")


def close_db(connection: Connection):
    """

    :param connection: the Connection object opened with open_db
    :return: nothing
    """
    connection.close()


def create_table(connection: Connection):
    connection.execute(f'''CREATE TABLE IF NOT EXISTS "character"
             (NAME VARCHAR(30) PRIMARY KEY     NOT NULL,
             ISALIVE    BOOL    NOT NULL,
             MAX_HP           INT    NOT NULL,
             HP            INT     NOT NULL,
             LEVEL           INT     NOT NULL,
             PASS_NEXT_TURN        BOOL NOT NULL);
             ''')

    connection.execute('''CREATE TABLE IF NOT EXISTS "player" 
    (NAME VARCHAR(30) PRIMARY KEY NOT NULL,
    XP int,
    LEFT_WEAPON VARCHAR(50),
    RIGHT_WEAPON VARCHAR(50),
    ENEMY_KILLED int);
    ''')

    connection.execute('''CREATE TABLE IF NOT EXISTS "inventory" 
        (OBJECT VARCHAR(100) PRIMARY KEY NOT NULL,
        QUANTITY int,
        PLAYER_NAME VARCHAR(30),
        FOREIGN KEY (PLAYER_NAME) REFERENCES player(NAME));
        ''')


def init_save(connection: Connection, **kwargs):
    try:
        statement = f'INSERT INTO "character" ("NAME", "ISALIVE", "MAX_HP", "HP", "LEVEL", "PASS_NEXT_TURN") VALUES ("{kwargs["name"]}", True, "50", "50", "1", False);'
        # print(statement)
        connection.execute(statement)
        connection.commit()
    except sqlite3.IntegrityError as e:
        print(e)

    try:
        statement = f'INSERT INTO "player" ("NAME", "XP", "LEFT_WEAPON", "RIGHT_WEAPON", "ENEMY_KILLED") VALUES ("{kwargs["name"]}", "0", "None", "None", 0);'
        # print(statement)
        connection.execute(statement)
        connection.commit()
    except sqlite3.IntegrityError as e:
        print(e)


def save(connection: Connection, **kwargs):
    try:
        if kwargs["is_alive"]:
            statement = f'UPDATE character set ISALIVE = "{kwargs["is_alive"]}" where NAME = "{kwargs["name"]}"'
            #print(statement)
            connection.execute(statement)
            connection.commit()
    except KeyError as e:
        print(e)

    try:
        if kwargs["max_hp"]:
            statement = f'UPDATE character set MAX_HP = "{kwargs["max_hp"]}" where NAME = "{kwargs["name"]}"'
            #print(statement)
            connection.execute(statement)
            connection.commit()
    except KeyError as e:
        print(e)

    try:
        if kwargs["hp"]:
            statement = f'UPDATE character set HP = "{kwargs["hp"]}" where NAME = "{kwargs["name"]}"'
            #print(statement)
            connection.execute(statement)
            connection.commit()
    except KeyError as e:
        print(e)

    try:
        if kwargs["level"]:
            statement = f'UPDATE character set LEVEL = "{kwargs["level"]}" where NAME = "{kwargs["name"]}"'
            #print(statement)
            connection.execute(statement)
            connection.commit()
    except KeyError as e:
        print(e)

    try:
        if kwargs["pass_next_turn"]:
            statement = f'UPDATE character set PASS_NEXT_TURN = "{kwargs["pass_next_turn"]}" where NAME = "{kwargs["name"]}"'
            #print(statement)
            connection.execute(statement)
            connection.commit()
    except KeyError as e:
        print(e)

    try:
        if kwargs["xp"]:
            statement = f'UPDATE player set XP = "{kwargs["xp"]}" where NAME = "{kwargs["name"]}"'
            #print(statement)
            connection.execute(statement)
            connection.commit()
    except KeyError as e:
        print(e)

    try:
        if kwargs["left_weapon"]:
            statement = f'UPDATE player set LEFT_WEAPON = "{kwargs["left_weapon"]}" where NAME = "{kwargs["name"]}"'
            #print(statement)
            connection.execute(statement)
            connection.commit()
    except KeyError as e:
        print(e)

    try:
        if kwargs["right_weapon"]:
            statement = f'UPDATE player set RIGHT_WEAPON = "{kwargs["right_weapon"]}" where NAME = "{kwargs["name"]}"'
            #print(statement)
            connection.execute(statement)
            connection.commit()
    except KeyError as e:
        print(e)

    try:
        if kwargs["enemy_killed"]:
            statement = f'UPDATE player set ENEMY_KILLED = "{kwargs["enemy_killed"]}" where NAME = "{kwargs["name"]}"'
            #print(statement)
            connection.execute(statement)
            connection.commit()
    except KeyError as e:
        print(e)


def load_save(connection: Connection, player_name: str):
    statement = f'SELECT * FROM "player" WHERE NAME = "{player_name}";'
    #print(statement)
    cursor = connection.execute(statement)
    for row in cursor:
        # MUST RUTURN ONE LINE (is PK)
        ### have to return a loaded player class
        #print(row)
        player = Player(player_name)
        player.name = row[0]
        player.xp = row[1]
        player.left_weapon = row[2]
        player.right_weapon = row[3]
        player.enemy_killed = row[4]
        statement = f'SELECT * FROM "character" WHERE NAME = "{player_name}";'
        cursor_c = connection.execute(statement)
        for row_character in cursor_c:
            #print(row_character)
            player.is_alive = row_character[1]
            player.max_hp = row_character[2]
            player.hp = row_character[3]
            player.level = row_character[4]
            player.pass_next_turn = row_character[5]
            return player

    return False


if __name__ == "__main__":
    connection = open_db("role-game")
    create_table(connection)
    init_save(connection, name="toto")
    save(connection, name="toto", column_name="ISALIVE", is_alive=False, max_hp="50")
    load_save(connection, "toto")
    close_db(connection)
