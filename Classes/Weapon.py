import random

class Weapon:
    def __init__(self, weapon_data):
        self.weapon_data = weapon_data

    def get_weapon_by_name(self, name):
        for weapon in self.weapon_data:
            if weapon['name'] == name:
                return weapon
        return None

    def get_all_weapons(self):
        return self.weapon_data

    def get_random_weapon(self):
        rando = random.choice(self.weapon_data)
        return rando["name"]