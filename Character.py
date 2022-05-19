from pprint import pprint
from random import randrange
import questionary
import template

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
        self.max_hp = 50
        self.hp = 50
        self.level = 1
        self.pass_next_turn = False

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
        print(f"{enemy.name} has {e.hp} hp")
        print(f"{enemy.name} has this weapon in left hand : {enemy.left_weapon}")
        print(f"{enemy.name} has this weapon in right hand : {enemy.right_weapon}")
        print("")
        print(f"You are level {self.level}")
        print(f"You have {self.hp} hp")
        print(f"You have this weapon equiped in left hand : {self.left_weapon}")
        print(f"You have this weapon equiped in right hand : {self.right_weapon}")
        print("")

        run_away = False
        choose = 0
        while enemy.is_alive and self.is_alive and not run_away:
            print("")
            while choose < 1 or choose > 3:
                print("### What do you want to do ? ###")
                print("1. Start attacking")
                print("2. Open your inventory")
                print("3. Try to run away")
                choose = 1 if self.pass_next_turn else int(input())
            if choose == 1:
                self.attack(e)
            elif choose == 2:
                self.open_inventory()
            elif choose == 3:
                run = randrange(2)
                if run == 0:
                    print("# You fail to run away #")
                else:
                    print("# You run away ! #")
                    run_away = True
            choose = 0

    def attack(self, enemy):
        coef = self._get_coef(enemy)
        if not self.pass_next_turn:
            print(f"You decide to attack {enemy.name}")
            damage = round(randrange(5, 10) * coef, 2)
            if damage == 0:
                print("You miss your attack")
            else:
                print(f"You hit {enemy.name} for {damage} damage")
                enemy.hp -= damage
                enemy.hp = round(enemy.hp, 2)
                print(f"{enemy.name} is now {enemy.hp} hp")
                if enemy.hp <= 0:
                    enemy.is_alive = False
                    print(f"### YOU KILL {enemy.name} !!! ###")
                    # xp_win = coef * randrange(1, 4)
                    xp_win = randrange(1, 4)  # TODO : find a bestway to compute xp
                    print(f"You win {xp_win} xp !")
                    self.get_xp(xp_win)
                    self.get_loot(enemy.id)
                    return
        else:
            print("")
            print("YOU USE A POTION LAST TURN, YOU HAVE TO SKIP THIS ONE ! ")
            print("")
            self.pass_next_turn = False

        # Enemy turn
        print(f"{enemy.name} is attacking you")
        damage = round(randrange(5, 15) * coef, 2)
        if damage == 0:
            print(f"{enemy.name} miss you")
        else:
            print(f"{enemy.name} hit you for {damage} damage")
            self.hp -= damage
            self.hp = round(self.hp, 2)
            print(f"You now have {self.hp} hp")
            if self.hp <= 0:
                self.is_alive = False
                print("### YOU ARE DEAD ###")
                return

        print("")
        print(f"# You have {self.hp} hp remaining #")
        print(f"# {enemy.name} is {enemy.hp} hp remaining #")
        print("")

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


class Player(Character):
    def __init__(self, name):
        super().__init__(name)
        self.xp = 0
        self.gold = 0
        self.left_weapon = None
        self.right_weapon = None
        self.inventory = {
            "Potion": 2,
            "Mana potion": 0,
        }

    def open_inventory(self):
        usage = -1
        key_list = []
        message = "# You take a look at your bag. You have this objects # "
        inventory_list = [f"{object_name} : {object_quantity}" for object_name, object_quantity in
                          self.inventory.items() if object_quantity]
        inventory_list.append("<< GO BACK")
        answer = questionary.select(
            message,
            choices=inventory_list,
            use_arrow_keys=True,
            show_selected=False,
        ).ask()

        object_name = 0 if answer == "<< GO BACK" else answer.split(':')[0].strip()

        # for object_name, object_quantity in self.inventory.items():
        #    if not object_quantity:
        #        print(strike(f"{object_name.upper()} : {object_quantity}"))
        #   else:
        #      print(f"{object_name.upper()} : {object_quantity}")
        # print("0. GO BACK")

        # Return to previous menu
        if object_name == 0:
            return
        else:
            self.use_object_from_inventory(object_name)

    def use_object_from_inventory(self, object_name):

        if "potion" in object_name.lower():
            potion = Potion(object_name)
            potion.use(object_name, self)
            # Update object in inventory
            self.inventory[object_name] -= 1


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
            player.pass_next_turn = True


class Weapon(Object):
    def __init__(self, object_name):
        super().__init__(object_name)
        self.usable = False


class Enemy(Character):
    def __init__(self, name, e_id):
        super().__init__(name)
        self.id = e_id
        self.name = name
        for enemy_id, enemy_info in template.enemies.items():
            if enemy_id == e_id:
                for key in enemy_info:
                    if key == "name":
                        pass
                    elif key == "hp":
                        self.hp = enemy_info[key]
                    elif key == "level":
                        self.level = enemy_info[key]
                    elif key == "left_weapon":
                        self.left_weapon = enemy_info[key]
                    elif key == "right_weapon":
                        self.right_weapon = enemy_info[key]


if __name__ == "__main__":
    c = Player("Aanks")
    e = Enemy("Electric Dwarf", 1)

    c.start_fight(e)
