import random

class BossMonster:
    def __init__(self, monster_data):
        self.monster_data = monster_data

    def get_boss_monster_by_name(self, name):
        for monster in self.monster_data:
            if monster['name'] == name:
                return monster
        return None

    def get_all_boss_monsters(self):
        return self.monster_data

    def get_random_boss_monster(self):
        return random.choice(self.monster_data)