from pprint import pprint
from random import randrange

XP_FROM_1_TO_2 = 5
XP_FROM_2_TO_3 = 10
XP_FROM_3_TO_4 = 20
XP_FROM_4_TO_5 = 50


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
        self.xp = 0
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
            return 1.2
        elif level_difference == -2:
            return 1.4
        elif level_difference == -3:
            return 1.7
        elif level_difference == -4:
            return 2
        elif -4 > level_difference > -8:
            return 5
        else:
            return 10

    def start_fight(self, enemy):
        print(f"### You meet a {enemy.name} ! ###")
        print("")
        print(f"{enemy.name} is level {enemy.level}")
        print(f"{enemy.name} has {e.hp}")
        print(f"{enemy.name} has this weapon in left hand : {enemy.left_weapon}")
        print(f"{enemy.name} has this weapon in right hand : {enemy.right_weapon}")
        print("")
        print(f"You are level {self.level}")
        print(f"You have {self.hp}")
        print(f"You have this weapon in left hand : {self.left_weapon}")
        print(f"You have this weapon in right hand : {self.right_weapon}")
        print("")

        run_away = False
        choose = 0
        while enemy.is_alive and self.is_alive and not run_away:
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
            print(f"You hit {enemy.name} for {damage} damage")
            enemy.hp -= damage
            print(f"{enemy.name} is now {enemy.hp} hp")
            if enemy.hp <= 0:
                enemy.is_alive = False
                print(f"### YOU KILL {enemy.name} !!! ###")
                xp_win = coef * randrange(1, 4)
                print(f"You win {xp_win} xp !")
                self.get_xp(xp_win)
                self.get_loot(enemy.id)
                return

        # Enemy turn
        print(f"{enemy.name} is attacking you")
        damage = randrange(4) * coef
        if damage == 0:
            print(f"{enemy.name} miss you")
        else:
            print(f"{enemy.name} hit you for {damage} damage")
            self.hp -= damage
            print(f"You now have {self.hp} hp")
            if self.hp <= 0:
                self.is_alive = False
                print("### YOU ARE DEAD ###")
                return

        print("")
        print(f"# You have {self.hp} hp remaining #")
        print(f"# {enemy.name} is {enemy.hp} hp remaining #")
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

    def get_xp(self, xp_win):
        self.xp += xp_win

        if self.level == 1:
            if self.xp < XP_FROM_1_TO_2:
                print(f"You need {XP_FROM_1_TO_2 - self.xp} more xp to level up !")
            else:
                print("### You level up ! You are now level 2 ! ###")
                self.xp -= XP_FROM_1_TO_2
                self.level += 1
        elif self.level == 2:
            if self.xp < XP_FROM_2_TO_3:
                print(f"You need {XP_FROM_2_TO_3 - self.xp} more xp to level up !")
            else:
                print("### You level up ! You are now level 3 ! ###")
                self.xp -= XP_FROM_2_TO_3
                self.level += 1
        elif self.level == 3:
            if self.xp < XP_FROM_3_TO_4:
                print(f"You need {XP_FROM_3_TO_4 - self.xp} more xp to level up !")
            else:
                print("### You level up ! You are now level 4 ! ###")
                self.xp -= XP_FROM_3_TO_4
                self.level += 1
        elif self.level == 4:
            if self.xp < XP_FROM_4_TO_5:
                print(f"You need {XP_FROM_4_TO_5 - self.xp} more xp to level up !")
            else:
                print("### You level up ! You are now level 5 ! ###")
                self.xp -= XP_FROM_4_TO_5
                self.level += 1
        else:
            print("###You are already at the maximum level (5) ! Congratulation ! More to come soon ###")

    def get_loot(self, enemy_id):
        pass


class Enemy(Character):
    def __init__(self, name,enemy_id):
        super().__init__(name)
        self.id = enemy_id


if __name__ == "__main__":
    c = Character("Aanks")
    e = Enemy("Dwarf troll", 0)


    c.start_fight(e)
