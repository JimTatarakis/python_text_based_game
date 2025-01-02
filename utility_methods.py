import json
import time
import random

def read_json_file(path_to_data, filename):
    filepath = path_to_data + filename + ".json"
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Warning: File '{filepath}' not found.")
        return {}  # Return empty dictionary instead of None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON data in '{filepath}'. {e}")
        return {}  # Return empty dictionary instead of None

def slow_print(text):
    for char in text:
        print(char, sep='', end='', flush=True)
        time.sleep(0.01)

    print()

def get_user_choice(options):
    while True:
        slow_print("Please choose from the following options:")
        for i, option in enumerate(options):
            slow_print(f"{i+1}. {option}")

        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                slow_print("Invalid choice. Please try again.")
        except ValueError:
            slow_print("Invalid input. Please enter a number.")

def open_chest(armor_list=None, weapon_list=None):
    if weapon_list is None:
        weapon_list = []
    if armor_list is None:
        armor_list = []

    gold_amount = 0
    armor_choice = ""
    weapon_choice = ""
    text = f"You open a chest containing {gold_amount} gold."

    if random.random() <= 0.95:
        gold_amount = random.randint(1, 50)
    if random.random() <= 0.40:
        armor_choice = random.choice(armor_list)
        text += " An armor piece."
    if random.random() <= 0.40:
        weapon_choice = random.choice(weapon_list)
        text += " And a weapon."

    return {
        "gold": gold_amount,
        "armor": armor_choice,
        "weapon": weapon_choice,
        "text": text
        }

def enter_room():
    ret = {
        "monster": random.random() <= 0.85,
        "chest": random.random() <= 0.25,
        "trap": random.random() <= 0.25,
        "exit": random.random() <= 0.05,
        "text": "You enter a room...\n"
    }

    if ret["chest"]:
        ret["text"] += "You notice in the corner, a chest.\n"

    if ret["exit"]:
        ret["text"] += "As you look across the room, light hits your eyes, you've found the exit.\n"

    if ret["monster"]:
        ret["text"] += ".\n.\n.\n.\n.\nYou hear something approaching you...A monster attacks!! *rawr*"

    return ret

def show_room_options(room = None):
    """
    We need a room obj otherwise, we throwing an exception.
    Monsters should already be faught at this point.
    So no need to worry about them.
        room = {
            "monster": random.random() <= 0.85,
            "chest": random.random() <= 0.25,
            "trap": random.random() <= 0.25,
            "exit": random.random() <= 0.05,
            "text": "You enter a room...\n"
        }
    """
    if room is None:
        raise Exception("An error has occured. err:show_options()")

    ret = []
    options = []
    if room["chest"]:
        options.append("You see a chest, you decide to explore it's contents.")
        ret.append("open_chest")
    if room["exit"]:
        options.append("You see the exit. At last safety is within reach. You venture outside. Congrats on completing the game!")
        ret.append("exit_area")
    else:
        options.append("Nothing else of catches your interest, but another pathway is available, you delve deeper into the unknown.")
        ret.append("enter_room")

    options.append("Meditate. (review character)")
    ret.append("show_char_options")

    # let user know one action per room.
    slow_print("You get the feeling you only have one action available. Choose wisely.")
    # get user choice, return the corresponding index for ret as the chosen option.
    return ret[options.index(get_user_choice(options))]

def show_menu_options():
    options = [
        "view armor inventory",
        "equip armor",
        "view weapon inventory",
        "equip weapon",
        "view skills",
        "unlock skill",
        "view stats",
        "upgrade stats",
        "close menu"
    ]
    print("Main Menu:")
    return get_user_choice(options)

def show_char_stats(base_stats, stat_points):
    item_list = f"""
        ______________________
        Character Stats
        ______________________
        strength: {base_stats["strength"]},
        wisdom: {base_stats["wisdom"]},
        defense: {base_stats["defense"]},
        max_mana: {base_stats["max_mana"]} (cannot upgrade, based on wisdom)
        health_regen: {base_stats["health_regen"]}, (cannot upgrade, based on health)
        mana_regen: {base_stats["mana_regen"]}, (cannot upgrade, based on wisdom)
        max_health: {base_stats["max_health"]},
        evasion: {base_stats["evasion"]}, (cannot upgrade, based on speed)
        speed: {base_stats["speed"]}
        ______________________
        Stat Points Available: {stat_points}
        ______________________
        """

    slow_print(item_list)


def setup_turn_order(monster_speed, mage_speed):
    # will return 10 turns.
    #determine who has more initiative.
    turns = []
    if monster_speed == mage_speed:
        while len(turns) < 10:
            if random.random() <= 0.5:
                turns.append("monster")
                turns.append("mage")
            else:
                turns.append("mage")
                turns.append("monster")
        return turns
    #determine who has more initiative.
    time_till_turn = mage_speed
    if monster_speed < mage_speed: time_till_turn = monster_speed

    monster_counter = 0
    mage_counter = 0

    while len(turns) < 10:
        monster_counter += monster_speed
        mage_counter += mage_speed

        mage_turns = mage_counter // time_till_turn
        mage_counter -= mage_turns * time_till_turn

        monster_turns = monster_counter // time_till_turn
        monster_counter -= monster_turns * time_till_turn

        if monster_speed > mage_speed:
            while monster_turns > 0:
                turns.append("monster")
                monster_turns -= 1
            while mage_turns > 0:
                turns.append("mage")
                mage_turns -= 1
        else:
            while mage_turns > 0:
                turns.append("mage")
                mage_turns -= 1
            while monster_turns > 0:
                turns.append("monster")
                monster_turns -= 1

    return turns