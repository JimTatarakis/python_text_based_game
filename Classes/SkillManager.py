import random

class SkillManager:
    def __init__(self, skill_data):
        self.skill_data = skill_data

    def get_skill_by_name(self, name):
        for skill in self.skill_data:
            if skill['name'] == name:
                return skill
        return None

    def get_all_skills(self):
        return self.skill_data