from threading import Timer
import random
import time
import os

FULL_MOVE_LIST = {"Jab Left":1, "Jab Right":1, "Overhand Left":2, "Overhand Right":2, "Roundhouse Kick":2, "Low Kick":3, "Takedown":4}
AVOID_TAKEDOWN_LIST = ["AVOID", "DODGE", "FIGHT", "REACT", "BLOCK", "PARRY", "SHIFT", "EVADE", "ELUDE", "GUARD",
                       "WEAVE", "BRACE"]

def type_sentence(sentence, delay=0.02):
    for letter in sentence:
        print(letter, end='', flush=True)
        time.sleep(delay)
    print()

class Player(object):

    MAX_STAMINA = 5
    MAX_HEALTH = 10

    def __init__(self, name:str) -> None:
        self.name = name
        self._health = 10
        self._strength = 1
        self._stamina = 3

    def __str__(self) -> str:
        return f"{self.name} has {self.health} health and {self.stamina} stamina!"

    def check_stamina(self, val)->bool:
        if val <= self._stamina:
            return True
        else:
            return False

    def get_health(self):
        return self._health
    
    def set_health(self, val):
        if val > self.MAX_HEALTH:
            self._health = self.MAX_HEALTH
            print("You are fully healed.")            
        else:
            self._health = val
    
    def get_strength(self):
        return self._strength
    
    def set_strength(self, val):
        self._strength = val

    def get_stamina(self):
        return self._stamina
    
    def set_stamina(self, val):
        if val > self.MAX_STAMINA:
            self._stamina = self.MAX_STAMINA
            print("You are fully rested.")      
        elif val < 0:
            self._stamina = 0
            print("You are exhaused!")
        else:
            self._stamina = val

    health = property(get_health, set_health)
    strength = property(get_strength, set_strength)
    stamina = property(get_stamina, set_stamina)

class Enemy(object):

    def __init__(self, name:str, move_list:list) -> None:
        self.name = name
        self.mL = move_list
        self._health = 10

    def __str__(self) -> str:
        return f"{self.name} has {self.health} health!"
    
    def get_health(self):
        return self._health
    
    def set_health(self, val):
        self._health = val

    health = property(get_health, set_health)

def hit_or_miss(p:Player, attack:str, decision:str)->bool:
    match decision.upper():
        case "SLIP LEFT":
            if attack != "Jab Right" and attack != "Overhand Right":
                return True
            else:
                return False
        case "SLIP RIGHT":
            if attack != "Jab Left" and attack != "Overhand Left":
                return True
            else:
                return False
        case "BACKSTEP":
            if p.check_stamina(1):
                p.stamina = p.stamina - 1
                if attack == "Overhand Left" or attack == "Overhand Right" or attack == "Roundhouse Kick":
                    return True
                else:
                    return False
            else:
                type_sentence("You try to backstep.. but don't have enough energy.")
                return True
        case "DUCK":
            if p.check_stamina(2):
                p.stamina = p.stamina - 2
                if attack == "Low Kick":
                    return True
                else:
                    return False
            else:
                type_sentence("You try to duck.. but don't have enough energy.")
                return True
        case _:
            return True
        
def quick_time_event(timeout:int = 3)->bool:
    type_sentence("He's going for a takedown!")
    word = random.choice(AVOID_TAKEDOWN_LIST)

    start_time = time.time()
    prompt = f"You have {timeout} seconds to dodge: Type {word} now! "
    answer = input(prompt)
    end_time = time.time()

    reaction_time = end_time - start_time
    if reaction_time > timeout:
        type_sentence("You didn't move in time!")
        return True
    else:
        if answer != word:
            type_sentence("You try to move but he still cathces you!")
            return True
        else:
            type_sentence("You managed to avoid the takedown")
            return False


def attack_dialogue(attack:str):
    match attack:
        case "Jab Left":
            return "He throws a simple left jab"
        case "Jab Right":
            return "He throws a simple right jab"
        case "Overhand Left":
            return "Look out! He throws a mean overhand left hook."
        case "Overhand Right":   
            return "Look out! He throws a mean overhand left hook."
        case "Low Kick":   
            return "Watch out! He goes for a low kick!"
        case "Roundhouse Kick":
            return "Aw crap! A huge roundhouse kick is coming your way!"
        case "Takedown":   
            return "He's preparing for something big..."
        case _:
            return "Bow bow bow"
        
def player_choice(move:str):
    match move.upper():
        case "JAB":
            return 0
        case "KICK":
            return 1
        case "REST":
            return 2
        case "STATS":
            return 3
        case _:
            return -1

def next_round(round:int) -> Enemy:
    round1_list = ["Jab Left", "Jab Right", "Low Kick"]
    round2_list = ["Jab Left", "Jab Right", "Overhand Left", "Overhand Right", "Roundhouse Kick"]
    round3_list = ["Overhand Left", "Overhand Right", "Low Kick", "Roundhouse Kick", "Takedown"]

    if round == 1:
        e = Enemy("Nathan", round1_list)
        e.health = 5
        type_sentence("Nathan enters the ring. He looks weak.")
    elif round == 2:
        e = Enemy("Tyrone", round2_list)
        e.health = 8
        type_sentence("Tyrone confidently enters the ring! It's time to lock in.")
    else:
        e = Enemy("Jon Jones", round3_list)
        e.health = 10
        type_sentence("Good luck. Jon 'Bones' Jones stares into your soul.")
    return e

def enemy_turn(p:Player, e:Enemy):
    type_sentence("It is now " + e.name + "'s turn to strike!")
    enemy_attack = random.choice(e.mL)
    dodge = input("How will you move?: ")

    type_sentence(attack_dialogue(enemy_attack))

    if enemy_attack == "Takedown":
        if quick_time_event():
            type_sentence("He lands some extra hits while you're down.")
            p.health = p.health - FULL_MOVE_LIST[enemy_attack]
        else:
            p.stamina = p.stamina + 1
        print()
    else:
        if hit_or_miss(p, enemy_attack, dodge):
            type_sentence("OUCH! You've been hit!")
            type_sentence("You've taken " + str(FULL_MOVE_LIST[enemy_attack]) + " damage.")
            p.health = p.health - FULL_MOVE_LIST[enemy_attack]
        else:
            type_sentence("You succesfully dodged his attack.")
            p.stamina = p.stamina + 1
        print()

def player_turn(p:Player, e:Enemy):
    type_sentence("Time to get on the offensive " + p.name + "!")
    move = input("What will you do?: ")

    if player_choice(move) == 0:
        if p.check_stamina(1):
            p.stamina = p.stamina - 1
            hit = random.randint(0,1)
            if hit == 1:
                type_sentence(e.name + " got hit with the jab!")
                type_sentence("He's taken " + str(p.strength) + " damage.")
                e.health = e.health - p.strength
            else:
                type_sentence(e.name + " avoided your punch.")
            print()
        else:
            type_sentence("Not enough energy to perform this action.")
            player_turn(p, e)
    elif player_choice(move) == 1:
        if p.check_stamina(2):
            p.stamina = p.stamina - 2
            type_sentence(e.name + " is stunned by your kick!")
            type_sentence("He's taken " + str(p.strength + 1) + " damage.")
            e.health = e.health - (p.strength + 1)
            print()
        else:
            type_sentence("Not enough energy to perform this action.")
            player_turn(p, e)
    elif player_choice(move) == 2:
        type_sentence("You decide to rest and recover stamina.")
        p.stamina = p.stamina + 1
        print(p)
        print()
    elif player_choice(move) == 3:
        print(p)
        player_turn(p, e)
    else:
        type_sentence("Waste of a turn, you bum.")
        print()

def check_health(p:Player, e:Enemy):
    if p.health <= 0:
        return 0
    if e.health <= 0:
        return 1
    return -1

def level_up(p:Player):
    type_sentence("What would you like to upgrade?")
    choice = input("Health:H / Strength:Str / Stamina:S ")

    if choice.upper() == "H":
        type_sentence("You feel more durable than ever!")
        p.MAX_HEALTH = p.MAX_HEALTH + 2
        print()
    elif choice.upper() == "Str":
        type_sentence("You feel stronger than ever!")
        p.strength = p.strength + 1
        print()
    elif choice.upper() == "S":
        type_sentence("You're in the best shape of your life!")
        p.MAX_STAMINA = p.MAX_STAMINA + 1
        print()
    else:
        print("Invalid input. Try again.")
        level_up(p)

def end_game():
    print("You lose. Boo hoo.")

def win_game():
    print("You win! Hurray!")

def init() -> str:
    type_sentence("Welcome to the text based MMA Fight!")
    type_sentence("You will face off against three opponents... do you have what it takes?!?\n")
    choice = input("Do you want to read the tutorial? Y/N ")

    if choice == "Y":
        print_tut()

    name = input("Time to get started! What's your name? ")
    type_sentence("Let the fights begin!")
    print()
    return name

def print_tut():
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'tut.txt')

    tutorial = open(filename, "r")
    info = tutorial.readlines()

    type_sentence(info)
    tutorial.close()
    print()

def main(p:Player):
    round = 1
    e = next_round(round)
    while True:        
        while p.health >= 0 and e.health >= 0:
            enemy_turn(p, e)
            match check_health(p, e):
                #Player lost
                case 0:
                    break
                #Player won
                case 1:
                    type_sentence(e.name + " has been defeated!")
                    break
                case _:
                    pass

            player_turn(p, e)
            match check_health(p, e):
                #Player lost
                case 0:
                    break
                #Player won
                case 1:
                    type_sentence(e.name + " has been defeated!")
                    break
                case _:
                    pass
        
        #Confirm if player or enemy won the fight
        if p.health > 0:
            del e
            if round < 3:
                level_up(p)
                p.health = p.MAX_HEALTH
                p.stamina = p.MAX_STAMINA

                round += 1
                e = next_round(round)
            else:
                win_game()
                break
        else:
            end_game()
            break

p = Player(init())
main(p)