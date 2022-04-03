from pprint import pprint
from random import randrange


def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result


class Character:
    def __init__(self, name):
        self.name = name
        self.is_alive = True
        self.max_hp = 10
        self.hp = 10
        self.gold = 0
        self.level = 1
        self.left_weapon = None
        self.right_weapon = None
        self.inventory = {
            1: {"hp_potion": 1},
            2: {"mana_potion": 0}
        }

    def _get_coef(self, enemy):
        """
        :param enemy: enemy (enemy object)
        :return: coefficient for attack/def
        """
        level_difference = enemy.level - self.level
        if level_difference > 7:
            return 0.1
        elif level_difference > 4:
            return 0.25
        elif level_difference == 4:
            return 0.5
        elif level_difference == 3:
            return 0.75
        elif level_difference == 2:
            return 0.85
        elif level_difference == 1:
            return 0.95
        elif level_difference == 0:
            return 1
        elif level_difference == -1:
            return 1.05
        elif level_difference == -2:
            return 1.15
        elif level_difference == -3:
            return 1.25
        elif level_difference == -4:
            return 1.5
        elif -4 > level_difference > -8:
            return 2
        else:
            return 10

    def start_fight(self, enemy):
        print(f"### You meet a {e.name} ! ###")
        print("")
        print(f"{e.name} is level {e.level}")
        print(f"{e.name} has {e.hp}")
        print(f"{e.name} has this weapon in left hand : {e.left_weapon}")
        print(f"{e.name} has this weapon in right hand : {e.right_weapon}")
        print("")
        print(f"You are level {self.level}")
        print(f"You have {self.hp}")
        print(f"You have this weapon in left hand : {self.left_weapon}")
        print(f"You have this weapon in right hand : {self.right_weapon}")
        print("")

        run_away = False
        choose = 0
        while e.is_alive and self.is_alive and not run_away:
            print("")
            print("### What do you want to do ? ###")
            print("1. Start attacking")
            print("2. Open your inventory")
            print("3. Try to run away")
            choose = int(input())
            while choose < 1 or choose > 3:
                print("### What do you want to do ? ###")
                print("1. Start attacking")
                print("2. Open your inventory")
                print("3. Try to run away")
                choose = int(input())
            if choose == 1:
                self.attack(e)
            if choose == 2:
                self.open_inventory()
            if choose == 3:
                run = randrange(2)
                if run == 0:
                    print("# You fail to run away #")
                else:
                    print("# You run away ! #")
                    run_away = True

    def attack(self, enemy):
        coef = self._get_coef(enemy)
        print(f"You decide to attack {enemy.name}")
        damage = randrange(4) * coef
        if damage == 0:
            print("You miss your attack")
        else:
            print(f"You hit {e.name} for {damage} damage")
            enemy.hp -= damage
            print(f"{e.name} is now {e.hp} hp")
            if e.hp <= 0:
                e.is_alive = False
                print(f"### YOU KILL {e.name} !!! ###")
                return
        # Enemy turn
        print(f"{e.name} is attacking you")
        damage = randrange(4) * coef
        if damage == 0:
            print(f"{e.name} miss you")
        else:
            print(f"{e.name} hit you for {damage} damage")
            self.hp -= damage
            print(f"You now have {self.hp} hp")
            if self.hp <= 0:
                self.is_alive = False
                print("### YOU ARE DEAD ###")
                return

        print("")
        print(f"# You have {self.hp} hp remaining #")
        print(f"# {e.name} is {e.hp} hp remaining #")
        print("")

    def open_inventory(self):
        usage = -1
        key_list = []
        print("# You take a look at your bag. You have this objects #")

        for object_id, object_info in self.inventory.items():
            key_list.append(int(object_id))
            print(f"{object_id}. ", end="")
            for key in object_info:
                if object_info[key] <= 0:
                    print(strike(f"{key.upper()} : {object_info[key]}"))
                    key_list.remove(object_id)
                else:
                    print(f"{key.upper()} : {object_info[key]}")
        print("0. GO BACK")
        key_list.append(0)
        print("What do you want to use ? ")

        usage = int(input())
        while usage not in key_list:
            print("Your choice is not correct ! ")
            usage = int(input())

        # Return to previous menu
        if usage == 0:
            return
        else:
            self.use_object_from_inventory(usage)

    def use_object_from_inventory(self, object_id):
        # Use HP potion
        if object_id == 1:
            amount_healed = randrange(3, 6)
            print(f"HP potion heal you for {amount_healed}")
            self.hp += amount_healed
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            print(f"You have now {self.hp}")

            # Update object in inventory
            self.inventory[1]['hp_potion'] = 0



class Enemy(Character):
    def __init__(self, name):
        super().__init__(name)


if __name__ == "__main__":
    c = Character("Aanks")
    e = Enemy("Troll")

    print(f"Character name is {c.name}")
    print(f"Enemy name is {e.name}")

    c.start_fight(e)
