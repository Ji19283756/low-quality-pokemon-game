import random
from random import randrange, randint, choice


class Pokemon:
    def __init__(self, name, type_, current_health='AvgHealth', cc='AvgCC', cd='AvgCD', acc='AvgAcc',
                 dph='AvgHit',
                 level=1):
        attributes = {'AvgHealth': 100, 'AvgCC': 30, 'AvgCD': 30, 'AvgAcc': 70, 'AvgHit': 25, 'HiHealth': 200,
                      'HiCC': 60, 'HiCD': 60, 'HiACC': 90, 'HiHit': 50}
        self.name = name
        self.OG_name = name
        self.level = level
        self.type = type_
        self.exp = 0
        self.is_knocked_out = False
        self.OG_health = attributes[current_health]
        self.max_health = attributes[current_health]
        self.health = attributes[current_health]
        self.cc = attributes[cc]
        self.cd = attributes[cd]
        self.acc = attributes[acc]
        self.dph = attributes[dph]
        self.ex = False

    def __repr__(self):
        return f"{self.name}: " \
               f"\nHealth: {self.health} Exp: {self.exp} Type: {self.type}\n" \
               f"Level: {self.level}    Knocked out: {self.is_knocked_out}"


    def level_up(self, exp_gained: int):
        self.exp += exp_gained
        if self.exp > (self.level * 100):
            self.level += 1
            self.max_health += (self.level * 1.5) * 50
            self.health = round(self.health + 50, 2)
            print(f"{self.name}'s level is now {self.level}\n"
                  f"{self.name}'s max health is now {self.max_health}\n"
                  f"{self.name} also gains 50 health\n"
                  f"{self.name} now has {self.health} health")

        if self.health > self.max_health:
            self.health = self.max_health
        # if self.health is greater than max health then it's set to max health, otherwise it's just health

    def lose_health(self, damage: int):
        self.health = round((self.health - damage), 2)
        self.is_knocked_out = (self.health <= 0)
        print(f"{(self.is_knocked_out) * f'{self.name} is knocked out'}"
              f"{(not damage) * f'{self.name} now has {self.health} health'}")

    def gain_health(self, potions_used: int, player):
        self.health = round(self.health + heal_calc(potions_used, player), 2)
        self.health = ((self.health > self.max_health) * self.max_health) + (
                (self.health <= self.max_health) * self.health)
        print(f"{self.name} now has {self.health} health")

    def attack_pokemon(self, trainer, other_trainer, other_pokemon, damage=0):
        damage = damage_calc(trainer, other_trainer, self)
        other_pokemon.lose_health(damage)
        exp = round(damage * 0.7, 2)
        self.level_up(exp)
        if damage:
            print(f"{self.name} has gained {exp} exp\n"
                  f"{trainer.name}: {encouragement_gen(trainer, other_trainer)}")


class Trainer:
    def __init__(self, name, potions, pokemon, active_pokemon):
        self.name = name
        self.potions = potions
        self.pokemon = pokemon
        self.OG_pokemon = pokemon
        self.active_pokemon = 0
        self.alive_pokemon = pokemon
        self.alive = True
        self.turn = 0
        print(self.pokemon)
        self.OG_pokemonDict = {self.pokemon[x].name.lower(): x for x in range(len(pokemon))}
        self.pokemonDict = {self.pokemon[x].name.lower(): x for x in range(len(pokemon))}

    def print_stats(self):
        print(f"Name: {self.name}\n"
              f"Potions: {self.potions}\n"
              f"Active pokemon: {self.pokemon[self.active_pokemon]}\n"
              f"Pokemon status: ")
        for pokemon in self.pokemon:
            if pokemon.is_knocked_out:
                print(f"{pokemon.name}: Dead")
            else:
                print(f"{pokemon.name}: Alive (HP{pokemon.health})")

    def print_pokemon_stats(self):
        print("Pokemon stats: ")
        for pokemon in self.pokemon:
            print(pokemon)

    def print_alive_pokemon(self):
        for pokemon in self.pokemon:
            if not pokemon.is_knocked_out:
                print(pokemon.name)

    def am_i_alive(self, other_player):
        if self.alive_pokemon == 0:
            self.alive = False
            self.death_message(other_player)
        return self.alive_pokemon != 0

    def heal(self, potions_used):
        print(f"{self.name} uses {potions_used} potion(s) to heal {self.pokemon[self.active_pokemon]}"
              f"({self.pokemon[self.active_pokemon].health}HP)")
        self.turn += 1
        self.pokemon[self.active_pokemon].gain_health(potions_used, self)
        self.potions -= potions_used
        print(f"{self.name} now has {self.potions} potion(s) left")

    def attack_trainer(self, other_trainer):
        other_trainer_pokemon = other_trainer.pokemon[other_trainer.active_pokemon]
        own_pokemon = self.pokemon[self.active_pokemon]
        own_pokemon.attack_pokemon(self, other_trainer, other_trainer_pokemon)
        if other_trainer_pokemon.is_knocked_out:
            other_trainer.alive_pokemon = [pokemon for pokemon in other_trainer.alive_pokemon if
                                           not pokemon.is_knocked_out]
            print(f"{other_trainer.name} has {len(other_trainer.pokemon)} pokemon left")
            if len(other_trainer.alive_pokemon) == 0:
                other_trainer.switch_to_not_knocked_out(self, True, False)
        if own_pokemon.level == 10 and not own_pokemon.ex and other_trainer.am_i_alive():
            # if pokemon level==2, and is not ex, and the other player is alive
            own_pokemon.name += " EX"
            print(f"{own_pokemon.name} has evolved after reaching level 10 and is now "
                  f"{self.pokemon[self.active_pokemon].name}")
            own_pokemon.ex = True
            self.pokemonDict = {self.pokemon[x].name.lower(): x for x in range(len(self.pokemon))}
        self.turn += 1

    def switch_active(self, switch_to, Forced=False, first=False):
        number_of_active = self.pokemonDict.get(switch_to)
        if self.pokemon[number_of_active].is_knocked_out:
            print(f"{self.name} can't switch to that pokemon because it is knocked out")
        else:
            if not first:
                print(f"{self.name}'s active pokemon is now {self.pokemon[self.active_pokemon].name}")
            print(f"{self.name} switched his main pokemon from {self.pokemon[self.active_pokemon].name}"
                  f" to {self.pokemon[number_of_active].name}")
            self.active_pokemon = number_of_active
        if not Forced:
            self.turn += 1

    def death_message(self, other_player):
        print(f"{self.name}tries to reach for his next pokeball only to find that he has none left"
                        ", the gravity of the situation dawns upon him as he sees all his pokemon"
                        " lay in front of him\n"
              f"{self.name} realizes that he has no hope as all of his pokemon are knocked out"
              f" \nhe looks into his rival's eyes for the last time and closes his eyes as he accepts his fate\n"
              f"{other_player.name} lowers his hat to cover his eyes as he orders his "
              f"{other_player.pokemon[other_player.active_pokemon].name} to commit its final attack upon"
              f" {self.name}\n{self.name.upper()} HAS BEEN BRUTALLY KILLED BY {other_player.name.upper()}'S"
              f"{other_player.pokemon[other_player.active_pokemon].name.upper()}")


    def switch_to_not_knocked_out(self, other_player, case1_forced, case2_choice):
        current = 0
        if case1_forced:
            for x in range(len(self.pokemon)):
                if (self.pokemon[current]).is_knocked_out:
                    current += 1
                elif not self.pokemon[current].is_knocked_out and not self.active_pokemon == current:
                    self.active_pokemon = current
                    self.turn += 1
        elif case2_choice:
            for pokemon in self.pokemon:
                if not is_1_weak_against_2(self.pokemon,other_player.pokemon)\
                        and not pokemon.is_knocked_out and not pokemon == self.pokemon[self.active_pokemon]:
                    self.switch_active(pokemon.name.lower())
                    self.turn -= 2
                    break
            if self.pokemon[self.active_pokemon].is_knocked_out:
                for x in range(len(self.pokemon)):
                    if (self.pokemon[current]).is_knocked_out:
                        current += 1
                    elif not self.pokemon[current].is_knocked_out:
                        self.active_pokemon = current
                        self.turn -= 2
        if current >= len(self.pokemon) or not self.alive:
            self.alive = False
            self.death_message(other_player)


# water bois
Magicarp = Pokemon(name='Magicarp', type_='water', acc='HiACC')
Clamperl = Pokemon(name='Clamperl', type_='water', current_health='HiHealth')
Frogadier = Pokemon(name='Frogadier', type_='water', cc='HiCC')
Squirtle = Pokemon(name='Squirtle', type_='water', cd='HiCD')
Gyrados = Pokemon(name='Gyrados', type_='water', dph='HiHit')
weed = Pokemon(name="420", type_='grass', dph='HiHit', cc='HiCC', cd='HiCD', acc='HiACC',
               current_health="HiHealth")
# fire bois
TalonFlame = Pokemon(name='TalonFlame', type_='fire', acc='HiACC')
Entei = Pokemon(name='Entei', type_='fire', current_health='HiHealth')
Charmander = Pokemon(name='Charmander', type_='fire', cc='HiCC')
Archanine = Pokemon(name='Archanine', type_='fire', cd='HiCD')
Blaziken = Pokemon(name='Blaiziken', type_='fire', dph='HiHit')
##grass bois
Treecko = Pokemon(name='Treecko', type_='grass', acc='HiACC')
Torterra = Pokemon(name='Torterra', type_='grass', current_health='HiHealth')
Exeggutor = Pokemon(name='Exeggutor', type_='grass', cc='HiCC')
Bulbasaur = Pokemon(name='Bulbasaur', type_='grass', cd='HiCD')
Sceptile = Pokemon(name='Sceptile', type_='grass', dph='HiHit')
# weed=Pokemon(name="420",type_='grass',dph='Hidph',cc='HiCC',cd='HiCD',acc='HiACC',current_health="HiHealth")
grassPokemonList = [Treecko, Torterra, Exeggutor, Bulbasaur, Sceptile]
firePokemonList = [TalonFlame, Entei, Charmander, Archanine, Blaziken]
waterPokemonList = [Magicarp, Clamperl, Frogadier, Squirtle, Gyrados]
all_pokemon = waterPokemonList + firePokemonList + grassPokemonList
grassPokemon = {'hiacc': Treecko, 'hihealth': Torterra, 'hicc': Exeggutor, 'hicd': Bulbasaur, 'hidph': Sceptile}
firePokemon = {'hiacc': TalonFlame, 'hihealth': Entei, 'hicc': Charmander, 'hicd': Archanine, 'hidph': Blaziken}
waterPokemon = {'hiacc': Magicarp, 'hihealth': Clamperl, 'hicc': Frogadier, 'hicd': Squirtle, 'hidph': Gyrados}
PokeDict = {'grass': grassPokemon, 'fire': firePokemon, 'water': waterPokemon}


def is_1_weak_against_2(pokemon1_type: str, pokemon2_type: str) -> bool:
    if pokemon1_type == pokemon2_type:
        return None
    elif pokemon1_type == 'grass':
        return pokemon2_type == "water"
    elif pokemon1_type == 'water':
        return pokemon2_type == "grass"
    elif pokemon1_type == 'fire':
        return pokemon2_type == "water"


def damage_calc(trainer: Trainer, other_trainer: Trainer, self) -> int:
    other_pokemon = other_trainer.pokemon[other_trainer.active_pokemon]
    dph = self.dph
    name = self.name
    pokemon_misses = randrange(0, 100) > self.acc
    if pokemon_misses:
        print(f"{name} missed\n"
              f" {trainer.name}: WTF {self.name.upper()}? {insult_gen()}")
        return 0
    else:
        weak_attack = is_1_weak_against_2(self.type, other_pokemon.type)
        # print(name+"nomrally does"+str(self.dph))
        type_multiplier = ((0.75 * (weak_attack == True)) +
                           (1.25 * (weak_attack == False)) +
                           ((weak_attack == None) * 1))
        crit_mulitplier = round(1 + (randrange(0, 100) > self.cc) * (self.cd * .01), 2)
        # print("the type multiplier causese "+name+"to do "+str(dph*type_multiplier)+"damage")
        dph = round(dph * type_multiplier * crit_mulitplier, 2)
        print(f"{trainer.name}'s {name} attacks\n"
              f"{other_trainer.name}'s {other_pokemon.name} (HP{other_pokemon.health})\n"
              f"{name} does {dph} damage")
        return dph


def heal_calc(potions_used: int, player: Trainer) -> int:
    RNG = randrange(0, 100)
    heal_amount = ((RNG > 99) * -5) + \
                  ((RNG <= 99 and RNG >= 90) * 70) + \
                  ((RNG < 90) * 50)
    print(f"{player.name}'s potions(s) "
          f"{(RNG > 99) * 'did not work that well, so each potion causes a loss of 5 health'}"
          f"{(RNG <= 99 and RNG >= 90) * 'did not exactly work that well, so each potion causes a loss of 5 health'}"
          f"{(RNG < 90) * 'successfully heals, so each potion causes a gain of 50 health'}")
    return heal_amount * potions_used


def choose_pokemon(personal_list: list, not_finished: bool, pal="Stranger: ") -> list:
    def pokemon_choice(type, personal_list, input_not_valid=True, pal="Stranger: "):
        print(f"{pal} Now, what special trait do you want?"
              f"\n the options are: \nhiacc \nhicc \nhicd  \nhidph"
              f" \nonce you've made your pick, print out your selection"
              f" (enter ? to find out what those abbreviations mean)")
        msg = f"{pal} You already chose that specific pokemon, choose a different special trait"
        while input_not_valid:
            string = input().lower().strip()
            try:
                if (PokeDict[type])[string] in personal_list:
                    print(msg)
                elif string == '?':
                    print(f'{pal} Ok so if I remember correctly'
                          f'\nhiacc = High Accuracy\nhihealth= High Health'
                          f'\nhicc = High Critical Chance\nhicd = High Critical Damage'
                          f'\nhidph = High Damage Per Hit')
                else:
                    print(f'{pal}Wow you got a {PokeDict[type][string].name}')
                    if (PokeDict[type])[string].type == "fire":
                        firePokemonList.remove((PokeDict[type])[string])
                    elif (PokeDict[type])[string].type == "water":
                        waterPokemonList.remove((PokeDict[type])[string])
                    elif (PokeDict[type])[string].type == "grass":
                        grassPokemonList.remove((PokeDict[type])[string])
                    return (PokeDict[type])[string]
            except KeyError:
                print(f"{pal} What? That's not an option, try again")

    while not_finished < 3:
        print(f'{pal} pick either water, fire, or grass')
        types = ['grass', 'water', 'fire']
        typeChoice = input().lower().strip()
        if typeChoice in types:
            personal_list.append(pokemon_choice(typeChoice, personal_list))
            not_finished += 1
        else:
            print(f"{pal}What? That wasn't one of the options, choose again")
    return personal_list


def decide(final_choice: bool, personal_list: list, first_dialog: bool) -> list:
    while True:
        print(f'{pal}so these are the pokemon that you have chosen:')
        for pokemon in personal_list:
            print(pokemon.name)
        print(f"{pal}{first_dialog * 'No lie, those choices of pokemon were PRETTY BAD'}" +
              (not first_dialog) * ("...to be honest I think that these new pokemon are"
                                   " worse than your original choice" +
              ", but i still belive in your ability now that I think about it, "
              "do you wanna switch or do you wanna fight with those pokemon?\n(print switch or stay)"))
        answer = input().lower().strip()
        if answer == 'switch':
            temp_dict = {"fire": firePokemonList, "water": waterPokemonList, "grass": grassPokemonList}
            for pokemon in personal_list:
                list_to_append_to = temp_dict[pokemon.type]
                temp_dict.append(pokemon)

                # if pokemon.type == 'fire':
                #    firePokemonList.append(pokemon)
                # if pokemon.type == 'water':
                #    waterPokemonList.append(pokemon)
                # if pokemon.type == 'grass':
                #    grassPokemonList.append(pokemon)
            personal_list = []
            personal_list = choose_pokemon(personal_list, 0)
            first_dialog = False
        elif answer == 'stay':
            break
        else:
            print(f"{pal}what?\nLook I'm going to say this again")
    return personal_list


def createNew(pokemon_amount: int, return_list=[]) -> list:
    while len(return_list) < pokemon_amount:
        random_type = choice([0, 1, 2])
        if random_type == 0 and firePokemonList:
            fire_pokemon = choice(firePokemonList)
            return_list.append(fire_pokemon)
            firePokemonList.remove(fire_pokemon)
        elif random_type == 1 and waterPokemonList:
            water_pokemon = choice(waterPokemonList)
            return_list.append(water_pokemon)
            waterPokemonList.remove(water_pokemon)
        elif random_type == 2 and grassPokemonList:
            grass_pokemon = choice(grassPokemonList)
            return_list.append(grass_pokemon)

    return return_list


def createEnemy(currentPlayer: Trainer) -> list:
    enemy_list = []
    for pokemon in currentPlayer.pokemon:
        if is_1_weak_against_2(pokemon.type, 'fire') and firePokemonList:
            fire_pokemon = choice(firePokemonList)
            enemy_list.append(fire_pokemon)
            firePokemonList.remove(fire_pokemon)
        elif is_1_weak_against_2(pokemon.type, 'water') and waterPokemonList:
            water_pokemon = choice(waterPokemonList)
            enemy_list.append(water_pokemon)
            waterPokemonList.remove(water_pokemon)
        elif is_1_weak_against_2(pokemon.type, 'grass') and grassPokemonList:
            grass_pokemon = choice(grassPokemonList)
            enemy_list.append(grass_pokemon)
            grassPokemonList.remove(grass_pokemon)
        else:
            enemy_list = createNew(1, enemy_list)
    return enemy_list


def enemyDesicionTree(enemy: Trainer, player: Trainer):
    switch_times = 0
    enemy.turn = ((enemy.turn >= 3) * 3) + ((enemy.turn < 3) * enemy.turn)

    enemys_current_pokemon_is_knocked_out = enemy.pokemon[enemy.active_pokemon].is_knocked_out
    enemy_can_switch_has_a_weak_pokemon_hasnt_already_switched_pokemon_and_has_pokemon_to_spare = \
        enemy.turn >= 3 and is_1_weak_against_2(enemy.pokemon[enemy.active_pokemon].type, player.pokemon[
            player.active_pokemon].type) and switch_times == 0 and not len(enemy.alive_pokemon) == 1
    current_pokemon_is_half_health_and_trainer_has_potions = enemy.pokemon[enemy.active_pokemon].health <= (
        enemy.pokemon[enemy.active_pokemon].max_health) / 2 and enemy.potions >= 1

    if enemys_current_pokemon_is_knocked_out:
        enemy.switch_to_not_knocked_out(player, True, False)
        switch_times += 1

    if enemy_can_switch_has_a_weak_pokemon_hasnt_already_switched_pokemon_and_has_pokemon_to_spare:
        enemy.switch_to_not_knocked_out(player, False, True)

    elif current_pokemon_is_half_health_and_trainer_has_potions:
        enemy.heal(1)
    else:
        enemy.attack_trainer(player)


def playerDecision(player, enemy, action_done):
    if not player.am_i_alive(enemy):
        player.switch_to_not_knocked_out(player, enemy, True, False)
    else:
        while True:
            if player.pokemon[player.active_pokemon].is_knocked_out:
                while True:
                    try:
                        print(
                            'Your pokemon has been knocked out and you have to replace it,'
                            ' who is now going to be your active pokemon?\n')
                        player.print_alive_pokemon()
                        switch_to = input().strip().lower()
                        player.switch_active(switch_to, Forced=True)
                    except TypeError:
                        print("That wasn't one of the options")
            action = input(
                "What do you wanna do now?\nOptions:\n-Attack\n-Heal\n-Switch\n-Print Stats"
                "\n-Regret Life Decisions\n").lower().strip()
            if action == 'attack':
                player.attack_trainer(enemy)
                break
            elif action == 'heal':
                if player.potions >= 1:
                    while True:
                        try:
                            potions_used = int(input("How many potions would you like to use?\n"))
                            if potions_used > player.potions:
                                print(f"You can't use that many potions because you only have "
                                      f"{player.potions} potions(s)")
                            else:
                                player.heal(int(potions_used))
                                break
                        except TypeError:
                            print("that is an invalid number of potions\nTry again")
                        except ValueError:
                            print("that is an invalid number of potions\nTry again")
                    break
                else:
                    print("You can't heal your pokemon because you have no potions left")
            elif action == "switch":
                # if player.turn < 2:
                #    print("You can only switch pokemon once every 3 turns, you'll
                #    have to try again later \nyou have "+3-self.turn+" turn(s) left until you can switch")
                # else:
                while True:
                    try:
                        print('Which pokemon do you want to switch to? Options:')
                        player.print_alive_pokemon()
                        print("-cancel")
                        switch_to = input().strip().lower()
                        if switch_to == "cancel":
                            break
                        else:
                            player.switch_active(switch_to, Forced=False)
                            break
                    except TypeError:
                        print("That wasn't one of the options try again")
                break
            elif action == "print stats":
                stats_choice = input(
                    "whose stats do you want to print?\n-my stats\n-my pokemon's stats"
                    "\n-enemy's stats\n-enemy's pokemon stats-\nall my stats"
                    "\n-all my enemy's stats\n-all stats\n").lower().strip()
                if stats_choice == 'my stats':
                    player.print_stats()
                elif stats_choice == "my pokemon's stats":
                    player.print_pokemon_stats()
                elif stats_choice == "enemy's stats":
                    enemy.print_stats()
                elif stats_choice == "enemy's pokemon stats":
                    enemy.print_pokemon_stats()

                elif stats_choice == "all my stats":
                    player.print_stats()
                    player.print_pokemon_stats()
                elif stats_choice == "all my enemy's stats":
                    enemy.print_stats()
                    enemy.print_pokemon_stats()
                elif stats_choice == "all stats":
                    player.print_stats()
                    player.print_pokemon_stats()
                    enemy.print_stats()
                    enemy.print_pokemon_stats()
                else:
                    print('That is not a valid choice')
            elif action == 'regret life decisions':
                print('Regretting life decisions...')
            else:
                print('That is not a valid response, try again')


def real_fight(player1, enemy):
    while enemy.am_i_alive(player1) and player1.am_i_alive(enemy):
        print('''Your turn:\n___________________________''')
        if enemy.am_i_alive(player1) and player1.am_i_alive(enemy):
            playerDecision(player1, enemy, False)
            input("\n")
            print('''Enemy's turn:\n___________________________''')
        enemyDesicionTree(enemy, player1)


def reset(player1, enemy):
    print("RESET")
    players = [player1, enemy]
    for player in players:
        player.alive = True
        player.potions = 5
        player.pokemon = player.OG_pokemon
        player.pokemonDict = player.OG_pokemonDict
        for pokemon in player.pokemon:
            pokemon.health = pokemon.OG_health
            pokemon.ex = False
            pokemon.name = pokemon.OG_name
            pokemon.is_knocked_out = False
            pokemon.level = 0
            pokemon.exp = 0
            pokemon.ex = False
            player.alive_pokemon.append(pokemon)


def advance_reset(player1, enemy):
    players = [player1, enemy]
    print("ADVANCE RESET")
    for player in players:
        player.alive = True
        player.potions = 5
        for pokemon in player.pokemon:
            pokemon.health = pokemon.OG_health
            pokemon.ex = False
            pokemon.name = pokemon.OG_name
            pokemon.is_knocked_out = False
            pokemon.level = 0
            pokemon.exp = 0
            pokemon.ex = False
            player.alive_pokemon.append(pokemon)
            if pokemon.type == 'fire':
                firePokemonList.append(pokemon)
            elif pokemon.type == 'water':
                waterPokemonList.append(pokemon)
            elif pokemon.type == 'grass':
                grassPokemonList.append(pokemon)
        player.pokemonDict = None
        player.pokemon = None
    default_pokemon = createNew(7)
    for pokemon in default_pokemon:
        print(pokemon.name)
    default = Trainer('Ash', 5, default_pokemon, 0)
    default.print_stats()
    print("__________________________")
    enemy = Trainer('Blue', 5, createEnemy(default), random.randint(0, len(default.pokemon) - 1))
    print('''Enemy's pokemon are ''')
    enemy.print_stats()


def insult_gen():
    insults = [
        "I'VE SEEN ACTUAL POTATOES HAVE BETTER AIM!",
        "I COULDN'T HAVE DONE WORSE IF I WAS TRYING TO SABATOGE OUR GAME!",
        "I'LL Kill YOU!", "LOOKS LIKE SOMEONE WANTS TO DIE!", "REEEEEEEEEEEE!",
        "\n(grabs bat)\nStranger: HEY HEY, lets focus on fighting the OTHER guy ok?",
        "AARRGGGG!", "NEXT TIME MAKE SURE YOUR OPPONENT DOESN'T LIVE TO SEE THE NEXT DAY!",
        "YOU'RE USELESS TO ME!", "AFTER THIS, ITS OFF TO THE GULAGS WITH YOU!",
        "THATS IT! YOU ARE NOW AN ENEMY TO THE STATE!", "IF YOU'RE NOT WITH ME THEN YOU'RE AGAINST ME!",
        "I FEEL LIKE YOUR PARENTS BECAUSE I'M SO DISSAPOINTED RIGHT NOW!",
        "YOU'RE LIKE SWAIN, YOU'RE A FAILURE!", "TIME TO DIE!", "WHY DO YOU SUCK SO MUCH?",
        "THERE IS NO WORD THAT CAN POSSIBLE DESCRIBE HOW BAD YOU ARE!"
    ]
    return choice(insults)


def encouragement_gen(self: Trainer, other_player: Trainer) -> str:
    encouragement = [
        f"Nice job {self.pokemon[self.active_pokemon]}\n hey {other_player.name}! next he's going to do that to you!",
        f"Way to go {self.pokemon[self.active_pokemon]}!", "god it HURTS to be this good",
        "AYYYYYYYYYYY", f"Aw god {other_player.name} it must suck to suck huh?",
        f"Hey {other_player.name} ! when my {self.pokemon[self.active_pokemon].name}"
        f" hit your pokemon I was imagining that its face was yours!",
        "HAHAHAHAHAHAHAHAHHA FEEL THE PAIN!!!", f"GOD I CANNOT IMAGINE BEING AS BAD AS YOU {other_player.name}!" +
        "YES BEAT THAT M!&#*$#&@!", f"SUCK IT {other_player.name.upper()}!",
        f"Hey {other_player.name} I bet you wish you were as good as me huh?\n keyword being \"wish\"",
        "LETS GOOOOOO!", "Bro when you run out of pokemon I'm going to feel SOOO good beating you up",
        f"Hey {other_player.name} I bet last time you got beat this bad it was with a belt right?",
        f"NICE, I only need to kill a few more pokemon until I can beat the crap out of {other_player.name}",
        f"Hey {other_player.name}! I bet you regret messing with me now right?\n No? Well you're about to!",
        "Yknow, I once had a nightmare where I was an absolute loser so I guess I know what it felt to be like you ",

        f"Yknow they say that a pokemon represents their trainer I guess that's why your "
        f"{other_player.pokemon[other_player.active_pokemon].name} took that punch like a little b&#@$",

        f"Yknow {other_player.name}? You should actually feel privileged to fight someone as great as me",
        'GOD, I almost feel bad for you!\nKeyword "almost"',
        f"Hey things are looking bad for you {other_player.name}! \nI guess I should ask now,"
        f" do you wanna be punted to death or kicked to death?\nOh well I guess I'll do both",

        f"*sigh* Yknow, it sucks that I'll only get to ABSOLUTELY destroy you once {other_player.name}"
        f"\nActually yknow what?\nDoing it again would be REALLY easy",

        "Yknow Albert Einstein said that two things were infinite, the amount of times that I WIN and your stupidity",
        "UGH, this is actually boring now, its like beating up a toddler,"
        " but I guess as long as that toddler is you, it's fine",
        "When I'm done with you, homeless people will donate to you",
        f"I guess the rumors are true {other_player.name}, you suck at everything"
    ]
    return choice(encouragement)


# _________________________________________________________________________________________________________
fight_choice = input("what kinda fight?\n")
if fight_choice == 'real':
    pal = 'Stranger: '
    enemy_dialog = "Blue: "
    print(
        pal + '''Ayo that kid over there is talking smack about you \nyou gotta defend your honor! \nYou should definately fight him. \nWhat? you don't have any pokemon? \nWhat are you POOR? Fine, I'll let you borrow mine for 500 dollars per minute. \nYeah it's a great deal I know''' + '\n Anyways what pokemon do you want? You only get to choose 3 so make good decisions\nTo start off you must first')
    personal_list = []
    personal_list = choose_pokemon(personal_list, 0)
    personal_list = decide(False, personal_list, first_dialog=True)
    print(
        pal + "*sigh* well I guess these pokemon aren't THAT bad anyways you should buy some potions, \npotions heal your pokemon so their suffering continues \nAnyways lets see how many potions we can buy with your money")
    input('(press any key to reach into your pocket to check for money)\n')
    print(
        "(you find that your pocket is empty)\n" + pal + "Oh yeah I forgot, back when I was pickpocketing you for money I found 5 bucks, but don't worry I already bought you some potions\n*hands you 5 potions*")
    name = input("Oh yeah it's kinda weird to ask this after everything, but what's your name?\n")
    player1 = Trainer(name, 5, personal_list, 0)
    input(
        pal + name.upper() + "??? Thats the stupidest name I've ever heard in my life\n seriously though whats your name\n(press enter to continue)\n")
    print(
        pal + "oh... I see so that IS your real name... well. I should let you know that " + name + " means something unspeakable in several languages here\nAnyways what pokemon are you going to have active?\nHere a list of your pokemon in case you forgot")
    print(player1.print_alive_pokemon())
    while True:
        active = input().lower()
        try:
            player1.switch_active(active, first=True)
            break
        except TypeError:
            print(pal + 'Bruh what? you dont have that pokemon, try again')
    print(
        pal + "ugh, why'd you have to change to your worst pokemon\nYknow as punishment that decisions is going to be one that you can't change until your actually in battle, serves you right\n")
    input(
        pal + "Anyways all you need to do now is fight him, cmon you gotta face your fears and go there!\nPress enter to approach\n")
    input(
        enemy_dialog + "Oh? Your approaching me? Instead of running away you're coming right towards me?\n(Press enter to respond)\n")
    input(
        name + ": I can't beat the crap out of you without getting getting closer\n" + enemy_dialog + " Oh? Then come as close as you like\n(Both of you begin to approach each other)\n")
    print("\nTime to fight" + '\nYour stats are: ')
    player1.print_stats()
    input("\n")
    enemy = Trainer('Blue', 5, createEnemy(player1), random.randint(0, 4))
    print('''Enemy's pokemon are: ''')
    enemy.print_stats()
    real_fight(player1, enemy)
elif fight_choice == "skip":
    pokemon_amount = int(input("how many pokemon do you want?"))
    default_pokemon = createNew(pokemon_amount)
    default = Trainer('Ash', 5, default_pokemon, 0)
    default.print_stats()
    input("\n")
    print("__________________________")
    enemy = Trainer('Blue', 5, createEnemy(default), random.randint(0, len(default.pokemon) - 1))
    print('''Enemy's pokemon are ''')
    enemy.print_stats()
    real_fight(default, enemy)
elif fight_choice == "test":
    personal_list = []
    personal_list = choose_pokemon(personal_list, 0)
    personal_list = decide(False, personal_list, first_dialog=True)
    default = Trainer('Ash', 5, personal_list, 0)
    default.print_stats()
    input("\n")
    print("__________________________")
    enemy = Trainer('Blue', 5, createEnemy(default), 0)
    print('''Enemy's pokemon are: ''')
    enemy.print_stats()
    real_fight(default, enemy)
else:
    default_pokemon = createNew(7)
    default = Trainer('Ash', 5, default_pokemon, 0)
    default.print_stats()
    print("__________________________")
    enemy = Trainer('Blue', 5, createEnemy(default), random.randint(0, len(default.pokemon) - 1))
    print('''Enemy's pokemon are ''')
    enemy.print_stats()
    for x in range(1):
        while enemy.am_i_alive(default) and default.am_i_alive(enemy) and enemy.alive and default.alive:
            print('''Your turn:\n___________________________''')
            # default.print_stats()
            # playerDecision(player1,enemy,True)
            # default.print_stats()
            enemyDesicionTree(default, enemy)
            # enemy.print_stats()
            if enemy.am_i_alive(default) and default.am_i_alive(enemy) and enemy.alive and default.alive:
                print('''Enemy's turn:\n___________________________''')
                enemyDesicionTree(enemy, default)
    #    reset(default,enemy)
    #    #advance_reset(default,enemy)
    #    print(str(x))
    #    default.print_stats()
    #    default.print_pokemon_stats()
    #    enemy.print_stats()
    #    enemy.print_pokemon_stats()
