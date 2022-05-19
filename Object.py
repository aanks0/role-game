from random import randrange


class Object:
    def __init__(self, object_name):
        self.name = object_name
        self.usable = True

    def __str__(self):
        return self.name


class Potion(Object):
    def __init__(self, object_name):
        super().__init__(object_name)
        self.level = 1
        self.hp_healed = randrange(15, 50)
        self.compute_potion(Potion)

    def compute_potion(self, object_name):
        if self.name == "Super Potion":
            self.level = 2
            self.hp_healed = randrange(30, 60)
        elif self.name == "Maxi Potion":
            self.level = 3
            self.hp_healed = randrange(40, 80)

    def use(self, object_name, player):
        if object_name in ["Potion", "Super Potion", "Maxi Potion"]:
            print("")
            print(f"HP potion heal you for {self.hp_healed}")
            player.hp += self.hp_healed
            if player.hp > player.max_hp:
                player.hp = player.max_hp
            print(f"You have now {player.hp}")
            print("")
            print("You gonna skip your next turn")
            player.pass_next_turn = True


class Weapon(Object):
    def __init__(self, object_name):
        super().__init__(object_name)
        self.usable = False
