import random

class Armor:
    def __init__(self, armor_data):
        self.armor_data = armor_data

    def get_armor_by_name(self, name):
        for armor in self.armor_data:
            if armor['name'] == name:
                return armor
        return None

    def get_all_armor(self):
        return self.armor_data

    def get_random_armor(self):
        rando = random.choice(self.armor_data)
        return rando["name"]