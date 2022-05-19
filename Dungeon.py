from time import sleep

from Character import Enemy


class Dungeon:
    def __init__(self, dungeon_name):
        self.dungeon_name = dungeon_name


class Level:
    def __init__(self, level_number):
        self.third_enemy = None
        self.second_enemy = None
        self.first_enemy = None
        self.level_number = level_number
        self.create()

    def create(self):
        if self.level_number == 1:
            self.first_enemy = Enemy("pitiful Goblin", 1)
            self.second_enemy = Enemy("Slave Goblin", 2)
            self.third_enemy = Enemy("Goblin Master", 3)

    def run(self, player):
        print("#" * 100)
        print("#" * 30 + "    Welcome to the very first level    " + "#" * 31)
        print("#" * 100)
        print("")
        print("")
        player.start_fight(self.first_enemy)
        if not self.first_enemy.is_alive:
            print("")
            print("You continue inside the dungeon ", end="")
            for _ in range(3, 0, -1):
                sleep(1)
                print(".", end="")
            print("")
            player.start_fight(self.second_enemy)
            if not self.second_enemy.is_alive:
                print("")
                print("You found a Potion on the slave Goblin ! You decide to drink it right now before continuing !")
                print("Drinking ", end="")
                for _ in range(5, 0, -1):
                    sleep(1)
                    print(".", end="")
                print("")
                player.inventory["Potion"] += 1
                player.use_object_from_inventory("Potion")
                player.pass_next_turn = False
                print("")
                print("You see something coming in the dark ...")
                player.start_fight(self.third_enemy)
                if not self.third_enemy.is_alive:
                    print("")
                    print("CONGRATULATION ! You succeed the very first level !!!!")
