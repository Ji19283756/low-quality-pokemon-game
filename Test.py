import random


class Pokemon:
    def __init__(self, name, type_, current_health='AvgHealth', cc='AvgCC', cd='AvgCD', acc='AvgAcc', dph='AvgHit',
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

    def level_up(self, exp_gained):
        self.exp += exp_gained
        if self.exp > (self.level * 100):
            self.level += 1
            self.max_health = self.max_health + (self.level * 1.5) * 50
            self.health = round(self.health + 50, 2)
            print(self.name + ' has level is now ' + str(self.level) + "\n" + self.name + "'s max health is now " +
                  str(self.max_health) + '\n' + self.name + " also gains 50 health\n" + self.name + " now has " +
                  str(self.health) + " health")
        self.health = (self.health > max_health * self.max_health) + ((self.health <= self.max_health) * self.health)
        # if self.health is greater than max health then it's set to max health, otherwise it's just health

    def lose_health(self, damage):
        self.health = round((self.health - damage), 2)
        self.is_knocked_out = (self.health <= 0)
        print(((self.is_knocked_out) * self.name + " is knocked out") +  # prints if the pokemon is knocked out
              ((damage != 0) * self.name + ' now has ' + str(
                  self.health) + ' health'))  # prints if the pokemon acutally got hit

    def gain_health(self, potions_used, player):
        self.health = round(self.health + heal_calc(potions_used, player), 2)
        self.health = ((self.health > self.max_health) * self.max_health) + (
                    (self.health <= self.max_health) * self.health)
        print(self.name + ' now has ' + str(self.health) + ' health')

    def attack_pokemon(self, trainer, other_trainer, other_pokemon, damage=0):
        damage = damage_calc(trainer, other_trainer, self)
        other_pokemon.lose_health(damage)
        exp = round(damage * 0.7, 2)
        self.level_up(exp)
        if damage > 0:
            print(self.name + " has gained " + str(exp) + " exp\n" + trainer.name + ": " + encouragement_gen(trainer,
                                                                                                             other_trainer))


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
        self.OG_pokemonDict = {self.pokemon[x].name.lower(): x for x in range(len(pokemon))}
        self.pokemonDict = {self.pokemon[x].name.lower(): x for x in range(len(pokemon))}

    def print_stats(self):
        print('Name: ' + self.name + "\nPotions:" + str(self.potions) + "\nActive pokemon:" + self.pokemon[
            self.active_pokemon].name + '\nPokemon status: ')
        for pokemon in self.pokemon:
            if pokemon.is_knocked_out:
                print(pokemon.name + ": Dead")
            else:
                print(pokemon.name + ": Alive (HP" + str(pokemon.health) + ")")

    def print_pokemon_stats(self):
        print("Pokemon stats: ")
        for pokemon in self.pokemon:
            print(pokemon.name + ": \nHealth: " + str(pokemon.health) + " Exp: " + str(
                pokemon.exp) + "  Type: " + pokemon.type + "\nLevel: " + str(pokemon.level) + "    Knocked out: " + str(
                pokemon.is_knocked_out))
        print("Potions: " + str(self.potions))

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
        print(self.name + ' uses ' + str(potions_used) + ' potion(s) to heal '
              + self.pokemon[self.active_pokemon].name + "(" + str(self.pokemon[self.active_pokemon].health) + "HP)")
        self.turn += 1
        self.pokemon[self.active_pokemon].gain_health(potions_used, self)
        self.potions -= potions_used
        print(self.name + " now has " + str(self.potions) + " potion(s) left")

    def attack_trainer(self, other_trainer):
        other_trainer_pokemon = other_trainer.pokemon[other_trainer.active_pokemon]
        own_pokemon = self.pokemon[self.active_pokemon]
        own_pokemon.attack_pokemon(self, other_trainer, other_trainer_pokemon)
        if other_trainer_pokemon.is_knocked_out:
            other_trainer.alive_pokemon = [pokemon for pokemon in other_trainer.alive_pokemon if
                                           not pokemon.is_knocked_out]
            print(other_trainer.name + " has " + str(len(other_trainer.alive_pokemon)) + " pokemon left")
            if len(other_trainer.alive_pokemon) == 0:
                other_trainer.switch_to_not_knocked_out(self, True, False)
        if own_pokemon.level == 10 and not own_pokemon.ex and other_trainer.am_i_alive():
            # if pokemon level==2, and is not ex, and the other player is alive
            own_pokemon.name += " EX"
            print(own_pokemon.name + ' has evolved after reaching level 10 and is now ' + self.pokemon[
                self.active_pokemon].name)
            own_pokemon.ex = True
            self.pokemonDict = {self.pokemon[x].name.lower(): x for x in range(len(self.pokemon))}
        self.turn += 1

    def switch_active(self, switch_to, Forced=False, first=False):
        number_of_active = self.pokemonDict.get(switch_to)
        if self.pokemon[number_of_active].is_knocked_out:
            print(self.name + " can't switch to that pokemon because it is knocked out")
        else:
            if not first:
                print(self.name + "'s active Pokemon is now " + self.pokemon[self.active_pokemon].name)
            print(self.name + ' switched his main pokemon from ' + self.pokemon[self.active_pokemon].name + ' to ' +
                  self.pokemon[number_of_active].name)
            self.active_pokemon = number_of_active
        if not Forced:
            self.turn += 1

    def death_message(self, other_player):
        print(
            self.name + " tries to reach for his next pokeball only to find that he has none left, the gravity of the situation dawns upon him as he sees all his pokemon lay in front of him\n" +
            self.name + " realizes that he has no hope as all of his pokemon are knocked out \nhe looks into his rival's eyes for the last time and closes his eyes as he accepts his fate\n"
            + other_player.name + " lowers his hat to cover his eyes as he orders his " + other_player.pokemon[
                other_player.active_pokemon].name + " to commit its final attack upon " + self.name + "\n"
            + self.name.upper() + " HAS BEEN BRUTALLY KILLED BY " + other_player.name.upper() + "'S " +
            other_player.pokemon[other_player.active_pokemon].name.upper())

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
                if not is_1_weak_against_2(self.pokemon,
                                           other_player.pokemon) and not pokemon.is_knocked_out and not pokemon == \
                                                                                                        self.pokemon[
                                                                                                            self.active_pokemon]:
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
weed = Pokemon(name="420", type_='grass', dph='HiHit', cc='HiCC', cd='HiCD', acc='HiACC', current_health="HiHealth")
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


def is_1_weak_against_2(pokemon1_type, pokemon2_type):
    if pokemon1_type == pokemon2_type:
        return None
    elif pokemon1_type == 'grass':
        return pokemon2_type == "water"
    elif pokemon1_type == 'water':
        return pokemon2_type == "grass"
    elif pokemon1_type == 'fire':
        return pokemon2_type == "water"


def damage_calc(trainer, other_trainer, self):
    other_pokemon = other_trainer.pokemon[other_trainer.active_pokemon]
    dph = self.dph
    name = self.name
    pokemon_misses=random.randint(0, 100) > self.acc
    if pokemon_misses:
        print(name + ' missed\n' + trainer.name + ": WTF " + self.name.upper() + "? " + insult_gen())
        return 0
    else:
        weak_attack = is_1_weak_against_2(self.type, other_pokemon.type)
        # print(name+"nomrally does"+str(self.dph))
        type_multiplier = ((0.75 * (weak_attack == True)) +
                           (1.25 * (weak_attack == False)) +
                           ((weak_attack == None) * 1))
        crit_mulitplier = round(1 + (random.randint(0, 100) > self.cc) * (self.cd * .01), 2)
        # print("the type multiplier causese "+name+"to do "+str(dph*type_multiplier)+"damage")
        dph = round(dph * type_multiplier * crit_mulitplier, 2)
        print(trainer.name + "'s " + name + " attacks \n" + other_trainer.name + "'s " + other_pokemon.name +
              " (HP" + str(other_pokemon.health) + ")\n" + name + " does " + str(dph) + " damage")
        return dph


def heal_calc(potions_used, player):
    RNG = random.randint(0, 100)
    heal_amount = ((RNG > 99) * -5) + \
                  ((RNG <= 99 and RNG >= 90) * 70) + \
                  ((RNG < 90) * 50)
    print(player.name + "'s potion(s) " +
          ((RNG > 99) * "didn't exactly work that well, so each potion causes a loss of 5 health") +
          ((RNG <= 99 and RNG >= 90) * "healed very well, so so each potion causes a gain of 70 health") +
          ((RNG < 90) * "successfully heals, so each potion causes a gain of 50 health"))
    return heal_amount * potions_used


def choose_pokemon(personal_list, not_finished, pal="Stranger: "):
    def pokemon_choice(type, personal_list, input_not_valid=True, pal="Stranger: "):
        print(pal +
              "Now, what special trait do you want?\n the options are: \nhiacc \nhicc \nhicd  \nhidph \nonce you've made your pick, print out your selection (enter ? to find out what those abbreviations mean)")
        msg = pal + "You already chose that specific pokemon, choose a different special trait"
        while input_not_valid:
            string = input().lower().strip()
            try:
                if (PokeDict[type])[string] in personal_list:
                    print(msg)
                elif string == '?':
                    print(pal +
                          ' Ok so if I remember correctly\nhiacc = High Accuracy\nhihealth= High Health\nhicc = High Critical Chance\nhicd = High Critical Damage\nhidph = High Damage Per Hit')
                else:
                    print(pal + 'Wow you got a ' + (PokeDict[type])[string].name)
                    if (PokeDict[type])[string].type == "fire":
                        firePokemonList.remove((PokeDict[type])[string])
                    elif (PokeDict[type])[string].type == "water":
                        waterPokemonList.remove((PokeDict[type])[string])
                    elif (PokeDict[type])[string].type == "grass":
                        grassPokemonList.remove((PokeDict[type])[string])
                    return (PokeDict[type])[string]
            except KeyError:
                print(pal + " What? That's not an option, try again")

    while not_finished < 3:
        print(pal + 'pick either water, fire, or grass')
        types = ['grass', 'water', 'fire']
        typeChoice = input().lower().strip()
        if typeChoice in types:
            personal_list.append(pokemon_choice(typeChoice, personal_list))
            not_finished += 1
        else:
            print(pal + "What? That wasn't one of the options, choose again")
    return personal_list


def decide(final_choice, personal_list, first_dialog):
    while True:
        print(pal + 'so these are the pokemon that you have chosen:')
        for pokemon in personal_list:
            print(pokemon.name)
        print(pal + (first * "No lie, those choices of pokemon were PRETTY BAD") +
              ((not first) * "...to be honest I think that these new pokemon are worse than your original choice") +
              ", but i still belive in your ability now that I think about it, "
              "do you wanna switch or do you wanna fight with those pokemon?\n(print switch or stay)")
        answer = input().lower().strip()
        if answer == 'switch':
            personal_list = []
            for pokemon in personal_list:
                if pokemon.type == 'fire':
                    firePokemonList.append(pokemon)
                if pokemon.type == 'water':
                    waterPokemonList.append(pokemon)
                if pokemon.type == 'grass':
                    grassPokemonList.append(pokemon)
            personal_list = choose_pokemon(personal_list, 0)
            first_dialog = False
        elif answer == 'stay':
            break
        else:
            print(pal + "what?\nLook I'm going to say this again")
    return personal_list


def createNew(pokemon_amount, return_list=[]):
    while pokemon_amount > 0:
        random_type = random.randint(0, 2)
        if random_type == 0 and len(firePokemonList) > 0:
            fire = random.randint(0, len(firePokemonList) - 1)
            return_list.append(firePokemonList[fire])
            firePokemonList.remove(firePokemonList[fire])
            pokemon_amount -= 1
        elif random_type == 1 and len(waterPokemonList) > 0:
            water = random.randint(0, len(waterPokemonList) - 1)
            return_list.append(waterPokemonList[water])
            waterPokemonList.remove(waterPokemonList[water])
            pokemon_amount -= 1
        elif random_type == 2 and len(grassPokemonList) > 0:
            grass = random.randint(0, len(grassPokemonList) - 1)
            return_list.append(grassPokemonList[grass])
            grassPokemonList.remove(grassPokemonList[grass])
            pokemon_amount -= 1
    return return_list


def createEnemy(currentPlayer, enemy_list=[]):
    enemy_list = []
    for pokemon in currentPlayer.pokemon:
        if is_1_weak_against_2(pokemon.type, 'fire') and len(firePokemonList) > 0:
            fire = random.randint(0, len(firePokemonList) - 1)
            enemy_list.append(firePokemonList[fire])
            firePokemonList.remove(firePokemonList[fire])
        elif is_1_weak_against_2(pokemon.type, 'water') and len(waterPokemonList) > 0:
            water = random.randint(0, len(waterPokemonList) - 1)
            enemy_list.append(waterPokemonList[water])
            waterPokemonList.remove(waterPokemonList[water])
        elif is_1_weak_against_2(pokemon.type, 'grass') and len(grassPokemonList) > 0:
            grass = random.randint(0, len(grassPokemonList) - 1)
            enemy_list.append(grassPokemonList[grass])
            grassPokemonList.remove(grassPokemonList[grass])
        else:
            enemy_list = createNew(1, enemy_list)
    return enemy_list


def enemyDesicionTree(enemy, player):
    switch_times = 0
    enemy.turn = ((enemy.turn >= 3) * 3) + ((enemy.turn < 3) * enemy.turn)
    if enemy.pokemon[enemy.active_pokemon].is_knocked_out:
        enemy.switch_to_not_knocked_out(player, True, False)
        switch_times += 1
    if enemy.turn >= 3 and is_1_weak_against_2(enemy.pokemon[enemy.active_pokemon].type, player.pokemon[
        player.active_pokemon].type) and switch_times == 0 and not len(enemy.alive_pokemon) == 1:
        enemy.switch_to_not_knocked_out(player, False, True)
    elif enemy.pokemon[enemy.active_pokemon].health <= (
    enemy.pokemon[enemy.active_pokemon].max_health) / 2 and enemy.potions >= 1:
        enemy.heal(1)
    else:
        enemy.attack_trainer(player)


def playerDecision(player, enemy, action_done):
    if not player.am_i_alive(enemy):
        player.switch_to_not_knocked_out(player, enemy, True, False)
    else:
        # if player.turn>3:
        #    player.turn=3
        while True:
            if player.pokemon[player.active_pokemon].is_knocked_out:
                while True:
                    try:
                        print(
                            'Your pokemon has been knocked out and you have to replace it, who is now going to be your active pokemon?\n')
                        player.print_alive_pokemon()
                        switch_to = input().strip().lower()
                        player.switch_active(switch_to, Forced=True)
                    except TypeError:
                        print("That wasn't one of the options")
            action = input(
                "What do you wanna do now?\nOptions:\n-Attack\n-Heal\n-Switch\n-Print Stats\n-Regret Life Decisions\n").lower().strip()
            if action == 'attack':
                player.attack_trainer(enemy)
                break
            elif action == 'heal':
                if player.potions >= 1:
                    while True:
                        try:
                            potions_used = int(input("How many potions would you like to use?\n"))
                            if potions_used > player.potions:
                                print("You can't use that many potions because you only have " + str(
                                    player.potions) + " potion(s)")
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
                #    print("You can only switch pokemon once every 3 turns, you'll have to try again later \nyou have "+3-self.turn+" turn(s) left until you can switch")
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
                    "whose stats do you want to print?\n-my stats\n-my pokemon's stats\n-enemy's stats\n-enemy's pokemon stats-\nall my stats\n-all my enemy's stats\n-all stats\n").lower().strip()
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
    return (insults[random.randint(0, 15)])


def encouragement_gen(self, other_player):
    encouragement = [
        "Nice job " + self.pokemon[
            self.active_pokemon].name + "\n hey " + other_player.name + "! next he's going to do that to you!",
        "Way to go " + self.pokemon[self.active_pokemon].name + "!", "god it HURTS to be this good",
        "AYYYYYYYYYYY", "Aw god " + other_player.name + " it must suck to suck huh?",
        "Hey " + other_player.name + "! when my " + self.pokemon[
            self.active_pokemon].name + " hit your pokemon I was imagining that its face was yours!",
        "HAHAHAHAHAHAHAHAHHA FEEL THE PAIN!!!",
        "GOD I CANNOT IMAGINE BEING AS BAD AS YOU " + other_player.name + "!" +
        "YES BEAT THAT M!&#*$#&@!", "SUCK IT " + other_player.name.upper() + "!",
        "Hey " + other_player.name + ' I bet you wish you were as good as me huh?\n keyword being "wish"',
        "LETS GOOOOOO!", "Bro when you run out of pokemon I'm going to feel SOOO good beating you up"
                         "Hey" + other_player.name + "I bet last time you got beat this bad it was with a belt right?"
                                                     "NICE, I only need to kill a few more pokemon until I can beat the crap out of " + other_player.name,
        "Hey " + other_player.name + "! I bet you regret messing with me now right?\n No? Well you're about to",
        "Yknow, I once had a nightmare where I was an absolute loser so I guess I know what it felt to be like you " + other_player.name,
        "Yknow they say that a pokemon represents their trainer I guess that's why your " + other_player.pokemon[
            other_player.active_pokemon].name + " took that punch like a little b&#@$",
        "Yknow " + other_player.name + "? You should actually feel privileged to fight someone as great as me",
        'GOD, I almost feel bad for you!\nKeyword "almost"',
        "Hey things are looking bad for you " + other_player.name + "! \nI guess I should ask now, do you wanna be punted to death or kicked to death?\nOh well I guess I'll do both",
        "*sigh* Yknow, it sucks that I'll only get to ABSOLUTELY destroy you once " + other_player.name + "\nActually yknow what?\nDoing it again would be REALLY easy",
        "Yknow Albert Einstein said that two things were infinite, the amount of times that I WIN and your stupidity",
        "UGH, this is actually boring now, its like beating up a toddler, but I guess as long as that toddler is you, it's fine",
        "When I'm done with you, homeless people will donate to you",
        "I guess the rumors are true " + other_player.name + ", you suck at everything"
    ]
    return (encouragement[random.randint(0, 21)])


# _________________________________________________________________________________________________________
choice = input("what kinda fight?\n")
if choice == 'real':
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
elif choice == "skip":
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
elif choice == "test":
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
