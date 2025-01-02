from utility_methods import *
import math
import random


class Mage:
    def __init__(self, mage_data):
        self.mage_data = mage_data

    def get_skills(self):
        return self.mage_data["skills"]

    def add_skill(self, skill, cost):
        if skill in self.mage_data["skills"]:
            raise Exception("Skill already accquired.")

        if cost < 0:
            raise Exception("Skill cost error, try again.")

        if cost > self.mage_data["skill_points"]:
            raise Exception("Not enough skill points.")

        # precondition: mage doesn't have skill & cost >= 0
        self.mage_data["skill_points"] -= cost
        self.mage_data["skills"].append(skill)

    def remove_skill(self, skill, cost):
        if skill not in self.mage_data["skills"]:
            raise Exception("Unlearned skill.")

        if cost < 0:
            raise Exception("Skill cost error, try again.")

        self.mage_data["skill_points"] += cost
        self.mage_data["skills"].append(skill)

    def get_skill_points(self):
        return int (self.mage_data["skill_points"])

    def update_skill_points(self, operation, amount):
        if operation == "add":
            self.mage_data["skill_points"] += amount
        elif operation == "subtract":
            self.mage_data["skill_points"] -= amount

        return int (self.mage_data["skill_points"])

    def get_base_stats(self):
        # first time loading stats we need to calculate certain base_stats
        if self.mage_data["base_stats"]["max_mana"] < 1:
            self.calculate_stats()
            # after calculating mana for the first time, set current mana to calculated result.
            # we do it here so we don't reset mana after updating stats.
            self.mage_data["base_stats"]["current_mana"] = self.mage_data["base_stats"]["max_mana"]

        return self.mage_data["base_stats"]

    def update_base_stat(self, operation, base_stat, stat_points):
        if stat_points > self.mage_data["stat_points"]:
            raise Exception("Not enough stat points.")

        if self.mage_data["base_stats"][base_stat] in self.mage_data["base_stats"][base_stat]:
            # add stat modifer for specific base_stats.
            if base_stat == "wisdom": stat_points * 3
            if base_stat == "defense": stat_points * 2
            if base_stat == "max_health": stat_points * 5
            if base_stat == "speed": stat_points * 2

            if operation == "add":
                self.mage_data["base_stats"][base_stat] += stat_points
            elif operation == "subtract":
                self.mage_data["base_stats"][base_stat] -= stat_points

        self.calculate_stats()

    def get_stat_points(self):
        return int(self.mage_data["stat_points"])

    def update_stat_points(self, operation, points = 0):
        if operation == "add":
            points = 5 + random.randint(1, 5)
            self.mage_data["stat_points"] += points
        elif operation == "subtract":
            self.mage_data["stat_points"] -= int(points)

        return int(self.mage_data["stat_points"])

    def calculate_lvl(self):
        base_exp = 100
        growth_factor = 1.25

        if self.mage_data["exp"] <= 0:
            self.mage_data["lvl"] = 1

        # approximate level using the inverse of the experience formula
        level_approx = math.log(self.mage_data["exp"] / base_exp, growth_factor) + 1
        level = int(level_approx)

        # ensure level doesn't exceed the maximum (100 in this case)
        level = min(level, 100)

        # set level to char
        self.mage_data["lvl"] = level

        return level

    def get_lvl(self):
        return self.mage_data["lvl"]

    def get_exp(self):
        return self.mage_data["exp"]

    def add_exp(self, exp):
        # add exp, calculate level, if new level, gain_stat_points(), return
        self.mage_data["exp"] += exp
        old_lvl = self.mage_data["lvl"]
        current_lvl = self.calculate_lvl()

        if old_lvl < current_lvl:
            # player leveled up, lets heal em.
            self.mage_data["base_stats"]["current_health"] = self.mage_data["base_stats"]["max_health"]
            self.mage_data["base_stats"]["current_mana"] = self.mage_data["base_stats"]["max_mana"]
            return {"level_up": True, "level": current_lvl, "current_stat_points": self.update_stat_points("add")}

        return {"level_up": False, "level": current_lvl, "current_stat_points": self.get_stat_points()}

    def calculate_stats(self):
        """
            mana, magic_regen, health_regen, and evasion all need to be calculated
            as they are based on other stats.
        """
        self.mage_data["base_stats"]["max_mana"] = int(self.mage_data["base_stats"]["wisdom"] * 5.5)
        self.mage_data["base_stats"]["mana_regen"] = int(self.mage_data["base_stats"]["wisdom"] * 0.25)
        self.mage_data["base_stats"]["health_regen"] = int(self.mage_data["base_stats"]["max_health"] * 0.25)
        self.mage_data["base_stats"]["evasion"] = int(self.mage_data["base_stats"]["speed"] * 0.25)

    def get_weapons(self):
        return self.mage_data["weapons"]

    def update_weapons(self, operation, weapon):
        if operation == "add":
            self.mage_data["weapons"].append(weapon)
        elif operation == "subtract":
            self.mage_data["weapons"].remove(weapon)

    def equip_weapon(self, weapon, damage_bonus):
        self.mage_data["equipped"]["weapon"] = weapon
        self.mage_data["equipped"]["damage_bonus"] = damage_bonus

    def get_armors(self):
        return self.mage_data["armors"]

    def update_armors(self, operation, armor):
        if operation == "add":
            self.mage_data["armors"].append(armor)
        elif operation == "subtract":
            self.mage_data["armors"].remove(armor)

    def equip_armor(self, armor, armor_bonus):
        self.mage_data["equipped"]["armor"] = armor
        self.mage_data["equipped"]["armor_bonus"] = armor_bonus

    def get_equipped_items(self):
        return self.mage_data["equipped_items"]

    def update_gold(self, operation, amount):
        if operation == "add":
            self.mage_data["gold"] += int(amount)
        elif operation == "subtract":
            self.mage_data["gold"] -= int(amount)
        return self.mage_data["gold"]

    def update_health(self, operation, amount):
        if operation == "add":
            self.mage_data["base_stats"]["max_health"] += int(amount)
        elif operation == "subtract":
            self.mage_data["base_stats"]["max_health"] -= int(amount)
        return self.mage_data["base_stats"]["max_health"]

    def update_current_health(self, operation, amount):
        if operation == "add":
            self.mage_data["current_health"] += int(amount)
        elif operation == "subtract":
            self.mage_data["current_health"] -= int(amount)
        elif operation == "update":
            self.mage_data["current_health"] = amount
        return self.mage_data["current_health"]

    def update_current_mana(self, operation, amount):
        if operation == "add":
            self.mage_data["current_mana"] += int(amount)
        elif operation == "subtract":
            self.mage_data["current_mana"] -= int(amount)
        elif operation == "update":
            self.mage_data["current_mana"] = amount
        return self.mage_data["current_mana"]

    def update_mana(self, operation, amount):
        if operation == "add":
            self.mage_data["base_stats"]["max_mana"] += int(amount)
        elif operation == "subtract":
            self.mage_data["base_stats"]["max_mana"] -= int(amount)
        return self.mage_data["base_stats"]["max_mana"]