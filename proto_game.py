from utility_methods import *
from Classes.Armor import Armor
from Classes.Weapon import Weapon
from Classes.Monster import Monster
from Classes.BossMonster import BossMonster
from Classes.SkillManager import SkillManager
from Classes.Mage import Mage

# load data classes
armor_data = read_json_file("./JsonData/","armors")
armor_manager = Armor(armor_data)

weapon_data = read_json_file("./JsonData/","weapons")
weapon_manager = Weapon(weapon_data)

monster_data = read_json_file("./JsonData/","monsters")
monster_manager = Monster(monster_data)

boss_monster_data = read_json_file("./JsonData/","boss_monsters")
boss_monster_manager = BossMonster(boss_monster_data)

skill_data = read_json_file("./JsonData/","mage_skills")
skill_manager = SkillManager(skill_data)

mage_data = read_json_file("./JsonData/","mage")
mage_manager = Mage(mage_data)

# start game
intro_text = """
Darkness... A bone-jarring fall. *thud*
You awaken with a gasp, disoriented. Your head throbs.
You are alone, lost, and your magic feels… muted, uncertain.
You must find a way out of this cavern before your dwindling supplies and dwindling courage give out.
"""

#slow_print(intro_text)
while True:
    current_room = enter_room()
    slow_print(current_room["text"])

    if current_room["monster"]:
        base_stats = mage_manager.get_base_stats()
        equipped_items = mage_manager.get_equipped_items()
        # current health will be retained after battle, need to update player health after fight, assuming they dont die.
        mage_info = {
            "double_cast": False,
            "damage_immune": False,
            "damage_immune_counter": 0,
            "damage_bonus": equipped_items["damage_bonus"],
            "defense_bonus": equipped_items["defense_bonus"],
            "strength": base_stats["strength"],
            "wisdom": base_stats["wisdom"],
            "defense": base_stats["defense"],
            "current_mana": base_stats["current_mana"],
            "max_mana": base_stats["max_mana"],
            "health_regen": base_stats["health_regen"],
            "mana_regen": base_stats["mana_regen"],
            "current_health": base_stats["current_health"],
            "max_health": base_stats["max_health"],
            "evasion": base_stats["evasion"],
            "speed": base_stats["speed"],
            "skills": mage_manager.get_skills()
        }

        current_monster = {}
        if random.random() <= 0.25:
            current_monster = boss_monster_manager.get_random_boss_monster()
        else:
            current_monster = monster_manager.get_random_monster()
        # monsters dont have current health as each time you encounter them, we need to have a fresh monster
        current_monster["current_health"] = current_monster["base_stats"]["max_health"]
        # during fights being able to make a monster or player immune to damage would be nice if it was just a toggle check.
        current_monster["damage_immune"] = False
        # at 0, less immunity
        current_monster["damage_immune_counter"] = 0

        slow_print(f"""You've encountered a monster, get ready to fight!""")
        # get turn order
        turn_order = []
        while mage_info["current_health"] > 0 and current_monster["current_health"] > 0:
            # if everyone is still alive, and we are done with current turn_order, refill it.
            if len(turn_order) == 0: turn_order = setup_turn_order(current_monster["base_stats"]["speed"], mage_info["speed"])
            turn = turn_order[0]

            if turn == "monster":
                monster_attack = random.choice(current_monster["abilities"])
                attack_damage = current_monster["base_stats"]["damage"] - int(mage_info["defense"] + mage_info["defense_bonus"])

                immune_statement = " \n"
                if mage_info["damage_immune"]:
                    mage_info["damage_immune_counter"] -= 1
                    attack_damage = 0
                    immune_statement = f"You lose an immunity counter. You have {mage_info['damage_immune_counter']} immunity counters left. \n"
                    if mage_info["damage_immune_counter"] == 0:
                        mage_info["damage_immune"] = False
                        immune_statement = "You lose an immunity counter. \n You have no more damage protection."

                # update player health
                mage_info["current_health"] -= attack_damage

                turn_text = f"""
                    {current_monster["name"]} Attacks! It uses it's {monster_attack} to deal {attack_damage} damage.
                    {immune_statement}
                """
                slow_print(turn_text)

            if turn == "mage":
                mage_info["current_health"] += mage_info["health_regen"]
                mage_info["current_mana"] += mage_info["mana_regen"]
                start_of_mage_turn_text = f"""
                    At the start of your turn, your vitality and focus increase.
                    You gain {mage_info["health_regen"]} health and {mage_info["mana_regen"]}
                """
                slow_print(start_of_mage_turn_text)

                # if mage health or mana have healed above the max, set it to max.
                if mage_info["current_health"] > mage_info["max_health"]: mage_info["current_health"] = mage_info["max_health"]
                if mage_info["current_mana"] > mage_info["max_mana"]: mage_info["current_mana"] = mage_info["max_mana"]

                text = f"""
                ____________________
                {current_monster["name"]}
                Health: {current_monster["current_health"]} / {current_monster["base_stats"]["max_health"]}
                ____________________
                Player
                Health: {mage_info["current_health"]} / {mage_info["max_health"]}
                Mana: {mage_info["current_mana"]} / {mage_info["max_mana"]}
                ____________________
                Turn Order:\n {turn_order} \n
                """

                slow_print(text)

                fight_options = ["Attack", "Use Skill"]

                while True:
                    chosen_option = get_user_choice(fight_options)

                    if chosen_option == "Attack":
                        if random.random() < current_monster["base_stats"]["evasion"] / 100:
                            slow_print(f"You swing for an attack, you miss! {current_monster['name']} evades your strike!")
                            break
                        attack_damage = int(mage_info["strength"] + mage_info["damage_bonus"])
                        current_monster["current_health"] -= attack_damage
                        slow_print(f"You swing for an attack, you hit! {current_monster['name']} takes {attack_damage} damage!")
                        break
                    if chosen_option == "Use Skill":
                        # display skills
                        slow_print("Available skills:")
                        for name in mage_info["skills"]:
                            searched_skill = skill_manager.get_skill_by_name(name)
                            searched_skill_text = f"""
                                {searched_skill['name'].title()}
                                Mana Cost: {searched_skill['mana_cost']}
                                Damage: {searched_skill['damage']}
                                Description: {searched_skill['description']}
                            """
                            slow_print(searched_skill_text)
                        # get user choice, or reset option so user can go back to use attack or skill.
                        skill_options = ["cancel"] + mage_info["skills"]
                        skill_choice = get_user_choice(skill_options)
                        # restart loop, we continue until user takes an action resulting in damage.
                        if skill_choice == "cancel": continue
                        if skill_choice == "aether_shield":
                            mage_info["double_cast"] = True
                            doublecast_statement = f"""
                                A faint violet aura surrounds you...
                                Your next damage skill will hit twice.
                                """
                            slow_print(doublecast_statement)
                            break
                        if skill_choice == "identify":
                            monster_text = f"""
                                name: {current_monster["name"]}
                                description: {current_monster["description"]}
                                damage: {current_monster["base_stats"]["damage"]}
                                evasion: {current_monster["base_stats"]["evasion"]}
                                speed: {current_monster["base_stats"]["speed"]}
                                max_health: {current_monster["base_stats"]["max_health"]}
                                abilities: {current_monster["abilities"]}
                            """
                            slow_print(monster_text)
                            break
                        if skill_choice == "aether_shield":
                            mage_info["damage_immune"] = True
                            mage_info["damage_immune_counter"] += 1 # Ya, these can stack if you're fast enough.
                            immune_statement = f"""
                                A faint white aura surrounds you...
                                You gain an immunity counter. You have {mage_info["damage_immune_counter"]} Immunity Counters.
                            """
                            slow_print(immune_statement)
                            break

                        skill = skill_manager.get_skill_by_name(skill_choice)
                        attack_damage = int(skill["damage"] + mage_info["damage_bonus"])
                        if mage_info["double_cast"]:
                            # we add an additional attack for doublecast
                            attack_damage += int(skill["damage"] + mage_info["damage_bonus"])
                        current_monster["current_health"] -= attack_damage
                        damage_text = f"""
                            You feel a warm sensation flow through your body.
                            You're mind focuses on manipulating the environment, bending reality to your will.
                            {skill["name"].title()}!!! {current_monster["name"].title()} can't evade the attack, it takes a direct hit!
                            {current_monster["name"].title()} takes {attack_damage} damage.
                        """
                        if mage_info["double_cast"]:
                            damage_text += "The violet aura fades. Doublecast has been spent."

                        slow_print(damage_text)
                        break

            # at the end of the turn, remove it from the turn_order
            # check if monster is defeated, check if player is defeated. exit fight if so.
            if current_monster["current_health"] <= 0 or mage_info["current_health"] <= 0: break
            # remove turn that was just taken before reiterating.
            turn_order.pop(0)
        #####################################
        # handle player or monster death
        if mage_info["current_health"] <= 0:
            slow_print("You have taken fatal damage, the monster devours you as the life drains from your eyes...\nGame over.")
            break

        if current_monster["current_health"] <= 0:
            exp = random.randint(50, 100)
            if random.random() <= 25: exp += 25 #random bonus exp

            mage_manager.add_exp(exp)
            slow_print(f"You have dealt fatal damage. {current_monster["name"].title()} has perished. You've gained {exp} exp")
            gold_amount = random.randint(1, 50)
            mage_manager.update_gold("add", gold_amount)
            text = f"You loot the creature, gaining {gold_amount} gold."
            if random.random() <= 0.35:
                mage_manager.update_armors("add", armor_manager.get_random_armor())
                text += " An armor piece."
            if random.random() <= 0.25:
                mage_manager.update_weapons("add", weapon_manager.get_random_weapon())
                text += " And a weapon."
            if random.random() <= 0.15:
                mage_manager.update_skill_points("add", 1)
                text += " And a Skill Card - a skill point will be added to your current skill points."
        mage_manager.update_current_health("update", mage_info["current_health"])
        mage_manager.update_current_mana("update", mage_info["current_mana"])
    # get user choice for how they handle the room, they get one action.
    user_action = show_room_options(current_room)
    # if user chooses "enter_room" the if statements get looked over and the cycle restarts.
    if user_action == "exit_area":
        # user has chosen to end game.
        break
    if user_action == "open_chest":
        if current_room["trap"]:
            damage = random.randint(1, 10)
            current_health = mage_manager.update_current_health("subtract", damage)

            if current_health <= 0:
                print(f"You open the chest, a mimic devours you! Game Over...")
                break
            print(f"You open the chest, a mimic bites you! You take {damage}! And manage to smash it to pieces. Frustrated, you exit this room.")
            continue
        else:
            chest_contents = open_chest([armor_manager.get_random_armor()], [weapon_manager.get_random_weapon()])
            """
            {
            "gold": gold_amount,
            "armor": armor_choice,
            "weapon": weapon_choice,
            "text": text
            }
            """
            mage_manager.update_gold("add", chest_contents["gold"])
            mage_manager.update_weapons("add", chest_contents["weapon"])
            mage_manager.update_armors("add", chest_contents["armor"])
            slow_print(chest_contents["text"])
            print(f"Impressed with your loot, you decide to venture forth.")
    if user_action == "show_char_options":
        while True:
            menu_action = show_menu_options()
            if menu_action == "close menu":
                break
            if menu_action == "view armor inventory":
                avail_armor = mage_manager.get_armors()
                print('available armor \n', avail_armor)
                if len(avail_armor) == 0 or avail_armor is None:
                    slow_print("You have no armor in your inventory.")
                    continue

                armor_list = """
                    Available Armor:
                    ______________________
                """
                for armor_name in avail_armor:
                    armor = armor_manager.get_armor_by_name(armor_name)
                    armor_list += f"""
                        name: {armor["name"]}
                        defense: {armor["defense"]}
                        ______________________
                    """
                print(armor_list)
                continue
            if menu_action == "equip armor":
                avail_armor = mage_manager.get_armors()
                # do nothing if no armors
                if len(avail_armor) == 0:
                    slow_print("You have no armor in your inventory.")
                    # take user back to main menu
                    continue
                    # create armor list.
                armor_list = """
                            Available Armor:
                            ______________________
                            """
                for armor_name in avail_armor:
                    armor = armor_manager.get_armor_by_name(armor_name)
                    armor_list += f"""
                        name: {armor["name"]}
                        defense: {armor["defense"]}
                        ______________________
                        """
                slow_print(armor_list)
                slow_print("Choose an armor.")
                chosen_armor = armor_manager.get_armor_by_name(get_user_choice(avail_armor))
                mage_manager.equip_armor(chosen_armor["name"], chosen_armor["defense"])
                slow_print(f"You have equiped {chosen_armor["name"]} with an armor bonus of {chosen_armor["defense"]}.")
            if menu_action == "view weapon inventory":
                avail_weapons = mage_manager.get_weapons()
                if len(avail_weapons) == 0:
                    slow_print("You have no weapons in your inventory.")
                    continue

                weapon_list = """
                        Available Weapons:
                        ______________________
                        """
                for weapon_name in avail_weapons:
                    weapon = weapon_manager.get_weapon_by_name(weapon_name)
                    weapon_list += f"""
                                    name: {weapon["name"]}
                                    attack: {weapon["attack"]}
                                    ______________________
                                    """
                print(weapon_list)
                continue
            if menu_action == "equip weapon":
                avail_weapons = mage_manager.get_weapons()
                if len(avail_weapons) == 0:
                    slow_print("You have no weapons in your inventory.")
                    continue

                weapon_list = """
                            Available Weapons:
                            ______________________
                            """
                for weapon_name in avail_weapons:
                    weapon = weapon_manager.get_weapon_by_name(weapon_name)
                    weapon_list += f"""
                        name: {weapon["name"]}
                        attack: {weapon["attack"]}
                        ______________________
                        """
                slow_print(weapon_list)
                slow_print("Choose an Weapon.")
                chosen_weapon = weapon_manager.get_weapon_by_name(get_user_choice(avail_weapons))
                mage_manager.equip_weapon(chosen_weapon["name"], chosen_weapon["attack"])
                slow_print(f"You have equiped {chosen_weapon["name"]} with an damage bonus of {chosen_weapon["attack"]}.")
            if menu_action == "view skills":
                avail_items = mage_manager.get_skills()
                if len(avail_items) == 0:
                    slow_print("You have no skills unlocked.")
                    continue

                item_list = """
                Available Skills:
                ______________________
                """
                for item_name in avail_items:
                    item = skill_manager.get_skill_by_name(item_name)
                    item_list += f"""
                        name: {item["name"]}
                        description: {item["description"]}
                        cost: {item["skill_point_cost"]} skill points
                    ______________________
                    """
                print(item_list)
                continue
            if menu_action == "unlock skill":
                avail_skill_points = mage_manager.get_skill_points()
                if avail_skill_points == 0:
                    slow_print("You have no skills points available.")
                    continue

                unlocked_skills = mage_manager.get_skills()
                all_skills = skill_manager.get_all_skills()
                locked_skills = []

                for index, skill in enumerate(all_skills):
                    if skill["name"] not in unlocked_skills:
                        locked_skills.append(skill)

                item_list = f"""
                Available Skill Points: {avail_skill_points}
                Available Skills:
                ______________________
                """

                for skill in locked_skills:
                    item_list += f"""
                    name: {skill["name"]}
                    description: {skill["description"]}
                    cost: {skill["skill_point_cost"]} skill points
                    ______________________
                    """

                slow_print(item_list)

                while True:
                    skill_choices = ["Finish upgrading skills."]
                    for skill in locked_skills:
                        skill_choices.append({"name": skill["name"], "skill_point_cost": skill["skill_point_cost"]})

                    chosen_skill = get_user_choice(skill_choices)

                    if chosen_skill == "Finish upgrading skills.": break

                    try:
                        print(f"adding a skill, chosen_skill['name'] = {chosen_skill["name"]}, chosen_skill['skill_point_cost'] = {chosen_skill["skill_point_cost"]}")
                        mage_manager.add_skill(chosen_skill["name"], chosen_skill["skill_point_cost"])
                    except Exception as e:
                        error_message = str(e)  # Capture the exception message
                        slow_print(f"Error: {error_message}")
                        continue

                    slow_print(f"You have unlocked {chosen_skill["name"]}.")
                    break
                continue
            if menu_action == "view stats":
                base_stats = mage_manager.get_base_stats()
                equipped_items = mage_manager.get_equipped_items()

                item_list = f"""
                ______________________
                Character Stats
                ______________________
                strength: {base_stats["strength"]},
                wisdom: {base_stats["wisdom"]},
                defense: {base_stats["defense"]},
                current_mana: {base_stats["current_mana"]},
                max_mana: {base_stats["max_mana"]},
                health_regen: {base_stats["health_regen"]},
                mana_regen: {base_stats["mana_regen"]},
                max_health: {base_stats["max_health"]},
                evasion: {base_stats["evasion"]},
                speed: {base_stats["speed"]}
                ______________________
                Stat Points Available: {mage_manager.get_stat_points()}
                ______________________
                Equipped Items
                ______________________
                Weapon: {equipped_items["weapon"]} +{equipped_items["damage_bonus"]} damage
                Armor: {equipped_items["armor"]} +{equipped_items["defense_bonus"]} defense
                ______________________
                Current exp: {mage_manager.get_exp()}
                Current lvl: {mage_manager.get_lvl()}
                """
                slow_print(item_list)
            if menu_action == "upgrade stats":
                show_char_stats(mage_manager.get_base_stats(), mage_manager.get_stat_points())
                upgrade_options = ["strength", "wisdom", "defense", "max_health", "speed", "done"]

                while True:
                    if mage_manager.get_stat_points() == 0:
                        print("You're out of stat points. Returning to main menu.")
                        break

                    upgrade_choice = get_user_choice(upgrade_options)

                    if upgrade_choice == "done": break

                    mage_manager.update_base_stat("add", upgrade_choice, mage_manager.get_stat_points())
                    show_char_stats(mage_manager.get_base_stats(), mage_manager.get_stat_points())