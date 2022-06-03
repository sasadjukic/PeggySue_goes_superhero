

import random, time
from easter_egg import EASTER_EGG

WEAPONS = {'Wooden Sword': 25, 'Iron Sword': 30, 'Spear': 35, 'Mace': 45}
LOOT_ITEMS = ['Food', 'Monster Energy Snack', 'Speed Boost Snacks', 'Nothing']
LOCATIONS = ['door', 'passage', 'bridge', 'narrow walkaway']
ATTACK_TERMS = ['attacking', 'pushing forward', 'finding space', 'taking advantage of bad defense']

class Hero:

    def __init__(self):
        self.name: str = 'PeggySue'
        self.backpack = {'Food': 0, 'Monster Energy Snack': 0, 'Speed Boost Snacks': 0}
        self.weapon: int = 0
        self.energy: int = 100
        self.speed: int = 50
        self.wins: int = 0
        self.easteregg: int = 0

class Enemy:

    def __init__(self, speed, energy, name, weapon):
        self.speed = speed
        self.energy = energy
        self.name = name
        self.weapon = weapon

def game_intro() -> str:

    print("\t\t\t***************************************")
    print("\t\t\t********PeggySue Goes Superhero********")
    print("\t\t\t***************************************")
    print("\n")
    print("\t\t\t-------------GAME RULES----------------")
    print("1. You start with no weapon, so it's wise to pick up the first weapon you find")
    print("2. 'Food' increases energy +15 and up to 100")
    print("3. 'Monster Energy Snack' increases energy +25 and beyond 100")
    print("4. 'Speed Boost Snack' increases speed +10")
    print("5. Carrying a heavy weapon (ex 'Mace') will lower your speed but increase your damage dealt")
    print("6. Higher the speed, higher the chances of your hero getting a turn")
    print("7. Encountering an enemy, you can choose to fight or answer an easter egg question for a safe passage")
    print("8. Failing to answer easter egg question forces you to fight the enemy you encountered")
    print("9. Your goal is to win 3 battles and rank up your hero")
    print("\t\t\t---------------------------------------")
    print("\n")
    return input("Press 'Y' to play the game: ")

def beginning() -> bool:

    torch = input('A lone torch illuminates otherwise dark cave. Pick it up and explore[Y/N]?: ').upper()
    if torch == 'Y':
        return True
    else:
        return False

def search() -> str:

    item_one = random.choice(LOOT_ITEMS)
    item_two = random.choice(LOOT_ITEMS)
    item_three = random.choice(list(WEAPONS.keys()))

    return item_one, item_two, item_three

def update_hero_items(loot_items, hero) -> None:

    for item in loot_items:
        if item in hero.backpack.keys():
            print(f'You have found {item.upper()}')
            add_item = input(f"Press 'Y' to add {item.upper()} to your backpack: ")
            if add_item.upper() == 'Y':
                hero.backpack[item] += 1
            else:
                hero.backpack[item]

def update_hero_weapons(loot_weapons, hero) -> str:

    for item in loot_weapons:
        if item in WEAPONS.keys():
            print(f'You have found {item.upper()}')
            if not WEAPONS[item] == hero.weapon:
                add_weapon = input(f"Press 'Y' to equip {item.upper()}: ")
                if add_weapon.upper() == 'Y':
                    hero.weapon = WEAPONS[item]
                    if hero.weapon == 25:
                        hero.speed += 10
                    elif hero.weapon == 45:
                        hero.speed -= 10
                elif add_weapon.upper() == 'N':
                    break
            else:
                time.sleep(1)
                print(f'But... you already have {item} equipped')
                pass

    for key, values in WEAPONS.items():
        if hero.weapon == values:
            return key

def check_status(hero_status, arms) -> None:

    print('\n\t\t\t*******************************')
    print('\t\t\t**********YOUR STATUS**********')
    print('\t\t\t*******************************')
    for key, values in hero_status.backpack.items():
        print(f'\t\t\t{key}: {values}')
    print(f'\t\t\tWeapon: {arms}')
    print(f'\t\t\tEnergy: {hero_status.energy}')
    print(f'\t\t\tSpeed: {hero_status.speed}')
    print(f'\t\t\tBattles Won: {hero_status.wins}')
    print(f'\t\t\tEaster Eggs answered: {hero_status.easteregg}')

def consume_items(hero) -> None:

    while hero.backpack['Food'] > 0:
        if hero.backpack['Food'] > 0:
            consume_food = input("Press 'Y' to consume food to increase your energy: ")
            if consume_food.upper() == 'Y':
                hero.backpack['Food'] -= 1
                hero.energy += 15
                if hero.energy > 100:
                    hero.energy = 100
            else:
                break

    while hero.backpack['Monster Energy Snack'] > 0:
        if hero.backpack['Monster Energy Snack'] > 0:
            consume_mes = input("Press 'Y' to consume Monster Energy Snack to increase your energy: ")
            if consume_mes.upper() == 'Y':
                hero.backpack['Monster Energy Snack'] -= 1
                hero.energy += 25
            else:
                break

    while hero.backpack['Speed Boost Snacks'] > 0:
        if hero.backpack['Speed Boost Snacks'] > 0:
            consume_sbs = input("Press 'Y' to consume Speed Boost Snacks to increase your speed: ")
            if consume_sbs.upper() == 'Y':
                hero.backpack['Speed Boost Snacks'] -= 1
                hero.speed += 10
            else:
                break

def fight(hero, enemy) -> str:

    while True:
        if next_turn(hero, enemy) == hero.name:
            print(f'\n\t\t\t{hero.name} is {random.choice(ATTACK_TERMS)}: ')
            if hit_register():
                print("\t\t\t\t\tIt's a hit")
                enemy.energy -= hero.weapon
                if hero_wins(enemy.energy):
                    print(f'\n\t\t\t\t\t{hero.name} WINS')
                    return hero.name
            else:
                print('\t\t\t\t\tMISS')

        else:
            print(f'\n\t\t\t{enemy.name} is {random.choice(ATTACK_TERMS)}: ')
            if hit_register():
                print('\t\t\t\t\tClean hit')
                hero.energy -= enemy.weapon
                if enemy_wins(hero.energy):
                    print(f'\n\t\t\t\t\t{hero.name} is dead')
                    print('\t\t\t\t\tGame over!!!')
                    return enemy.name
            else:
                print('\t\t\t\t\tMISS')

def next_turn(protagonist, antagonist) -> str:

    chances = []
    for turn in range(protagonist.speed):
        chances.append(protagonist.name)

    for turn in range(antagonist.speed):
        chances.append(antagonist.name)

    next_turn = random.choice(chances)
    return next_turn

def hit_register() -> bool:

    hit = random.randint(0, 1)
    if hit == 1:
        return True
    else:
        return False

def hero_wins(enemy_energy) -> bool:

    if enemy_energy <= 0:
        return True
    else:
        return False

def enemy_wins(hero_energy) -> bool:

    if hero_energy <= 0:
        return True
    else:
        return False

def easter_egg(EE, hero) -> bool:

    quotes = [key for key, value in EE.items()]
    answers = []
    answer_index = 0

    for quote in quotes:
        random_quote = random.choice(quotes)
        if EE[random_quote] not in answers:
            answers.append(EE[random_quote])
            answer_index += 1
            if answer_index == 3:
                break

    print('\n\t\t\tWhich movie features the following quote:')
    print(f"\t\t\t'{random_quote}'")

    letters = 'ABC'
    letters_index = 0
    for answer in answers:
        print(f'\t\t\t{letters[letters_index]}. {answer}')
        letters_index += 1

    user_answer = input('Enter movie title: ')

    if user_answer == EE[random_quote]:
        print('Correct. You may pass.')
        hero.easteregg += 1
        return True
    else:
        print('Incorrect. Redy for the fight...')
        return False

def main():

    hero = Hero()
    if game_intro().upper() == 'Y':

        print('\n\t\t\t---------------------------------------')
        print('\nFADE IN: ')
        if beginning():
            looting = search()
            update_hero_items(looting, hero)
            weapon = update_hero_weapons(looting, hero)
            print('\n\t\t\t---------------------------------------')
            u_input = input("\nCheck your status and items by pressing 's': ").upper()
            if u_input == 'S':
                check_status(hero, weapon)
            else:
                pass

            print('\n\t\t\t---------------------------------------')

            chapter_1 = True
            while chapter_1:
                skeleton = Enemy(speed=50, energy=60, name='Skeleton', weapon=WEAPONS['Iron Sword'])
                pit_lord = Enemy(speed=40, energy=100, name='Pit Lord', weapon=WEAPONS['Spear'])
                ogre = Enemy(speed=30, energy=120, name='Ogre', weapon=WEAPONS['Mace'])
                enemies = [skeleton, pit_lord, ogre]
                enemy = random.choice(enemies)
                poi = random.choice(LOCATIONS)
                print(f"\nYour torch catches a glimpse of a {poi}. There's {enemy.name} guarding that {poi}")

                ready_or_not = input('Fight or answer an Easter Egg question?[F/A]: ')
                print('\n\t\t\t---------------------------------------')
                if ready_or_not.upper() == 'F':
                    if fight(hero, enemy) == hero.name:
                        hero.wins += 1
                        if hero.wins == 3:
                            print('\n\t\t\t\t******************************')
                            print('\t\t\t\t******Congratulations!!!******')
                            print('\t\t\t\t******************************')
                            print('\n\t\t\tYou have ranked up and completed the game intro!!!')
                            chapter_1 = False
                            break
                        else:
                            pass
                    else:
                        quit()
                else:
                    if easter_egg(EASTER_EGG, hero):
                        pass
                    else:
                        time.sleep(2)
                        if fight(hero, enemy) == hero.name:
                            hero.wins += 1
                            if hero.wins == 3:
                                print('\n\t\t\t******************************')
                                print('\t\t\t******Congratulations!!!******')
                                print('\t\t\t******************************')
                                print('\n\t\t\tYou have ranked up and completed the game intro')
                                quit()
                            else:
                                pass
                        else:
                            quit()

                print('\n\t\t\t---------------------------------------')

                energy_status = hero.energy
                after_battle_prompt = input(f"\nAfter the encounter your energy is {energy_status}. Press 's' to view your status and consume items: ")
                if after_battle_prompt.upper() == 'S':
                    check_status(hero, weapon)
                    consume_items(hero)

                print('\n\t\t\t---------------------------------------')

                loot_or_not = input(f'\nYou have passed the {poi}. Should you check for some loot[Y/N]?: ')
                if loot_or_not.upper() == 'S':
                    check_status(hero, weapon)
                elif loot_or_not.upper() == 'Y':
                    more_loot = search()
                    update_hero_items(more_loot, hero)
                    weapon = update_hero_weapons(more_loot, hero)
                else:
                    print("\nLet's move on, shall we?")

if __name__ == '__main__':
    main()
