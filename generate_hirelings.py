import random
import os
import struct
from typing import Tuple
import argparse
from collections import OrderedDict

D3 = (1,3)
D4 = (1,4)
D6 = (1,6)
D8 = (1,8)
D10 = (1,10)
D12 = (1,12)
D20 = (1,20)
D100 = (1,100)

class Config:
    LF = "Light Foot"
    HF = "Heavy Foot"
    BOW = "Bowman"
    XBOW = "Crossbowman"

    CHAIN = "chain mail"
    LEATHER = "leather"
    SHIELD = "shield"

HIRELING_TYPES = [
    {
        'chance': 90,
        'amount': D6,
        'name': "Non-combatant",
        'hp_die': D4,
        'base_wage': 1
    },
    {
        'chance': 80,
        'amount': D6,
        'name': Config.LF,
        'base_wage': 4
    },
    {
        'chance': 60,
        'amount': D6,
        'name': Config.HF,
        'base_wage': 7
    },
    {
        'chance': 30,
        'amount': D6,
        'name': Config.BOW,
        'base_wage': 10
    },
    {
        'chance': 20,
        'amount': D6,
        'name': Config.XBOW,
        'base_wage': 9
    },
]


NAMES = {
    'M': [
        "François", "Henri", "Louis", "Charles", "Tristan", "Pierre", "Antoine", "Théodore", "Jean", "Philippe",
        "Lionel", "Nicolas", "Michel", "Baptiste", "André", "René", "Gabriel", "Bernard", "Vincent", "Olivier",
        "Thibault", "Mathieu", "Denis", "Adrien", "Sébastien", "Martin", "Raphaël", "Jules", "Gaspard", "Laurent",
        "Hans", "Jakob", "Konrad", "Ulrich", "Matthias", "Heinrich", "Fritz", "Andreas", "Johann", "Peter",
        "Cosimo", "Bartolomeo", "Lorenzo", "Raffaello", "Niccolò", "Wolfgang", "Leopold", "Maximilian", "Ferdinand",
        "Hans-Jörg", "Alban", "Benoît", "Éric", "Gérard", "Hugo", "Yves", "Cédric", "Sylvain", "Julien", "Maurice",
        "Rémi", "Édouard", "Régis", "Théophile", "Auguste", "Emmanuel", "Victor", "Pascal", "Bastien", "Frédéric",
        "Gustave", "Michelangelo", "Armand", "Nicolas", "Raymond", "Léon", "Bertrand", "Gérald", "Antoine", "Henriette",
        "Blaise", "Serge", "Théo", "Quentin", "Julian", "Jérôme", "Olivier", "Lucien", "Émile", "Raoul", "Adrien",
        "Félix", "Damien", "Albert", "Clément", "Matteo", "Jules", "Maxence", "Clement", "Elliot", "Raphael", "Louis",
        "Gustave", "Michel", "Antoine", "Jean-Baptiste", "Claude", "Louis-Philippe", "Grégoire", "Emmanuel", "Franck",
        "Thierry", "Arthur"
    ],
    'F': [
        "Adrienne", "Blanche", "Perrine", "Mathilde", "Thérèse", "Geneviève", "Angélique", "Lucie", "Béatrice",
        "Isabeau", "Adelheid", "Brigitta", "Verena", "Elsbeth", "Magdalena", "Ursula", "Theresia", "Anna",
        "Margaretha", "Barbara", "Catherine", "Marie", "Marguerite", "Anne", "Jeanne", "Isabelle", "Louise",
        "Charlotte", "Élisabeth", "Françoise", "Madeleine", "Antoinette", "Jacqueline", "Renée", "Gabrielle",
        "Christine", "Margot", "Claudine", "Hélène", "Victoire", "Maddalena", "Lavinia", "Caterina", "Isabetta",
        "Lucrezia", "Amalia", "Eleonore", "Ottilie", "Walburga", "Rosalind", "Aline", "Solange", "Noémie", "Berthe",
        "Lucienne", "Vivienne", "Huguette", "Alphonsine", "Odile", "Mariette", "Renée", "Stéphanie", "Rosa",
        "Suzanne", "Florence", "Mathilde", "Odette", "Clarisse", "Lucille", "Eulalie", "Simone", "Rosalie", "Monique",
        "Valérie", "Isabelle", "Pauline", "Édith", "Laure", "Véronique", "Yvonne", "Annie", "Blandine", "Sylvie",
        "Ginette", "Dominique", "Nicole", "Élisabeth", "Emmanuelle", "Mireille", "Thérèse", "Marina", "Chantal",
        "Genevieve", "Martine", "Andrée", "Géraldine", "Caroline", "Sophie", "Amandine", "Mireille", "Emilie",
        "Gabrielle", "Jacinthe", "Ghislaine", "Bernadette", "Hortense", "Béatrice", "Laurence", "Odessa", "Solange",
        "Patricia", "Angèle", "Sonia", "Denise", "Christine", "Evelyne", "Julie", "Jeanne", "Alice", "Madeleine",
        "Violette", "Angélique"
    ]
}


QUIRKS = [
    "Has peg leg",
    "Owes 1d6*100 gp, tries to get sum by any means",
    "Drunkard",
    "Foul-mouthed",
    "Hunting dog: HD 1; AC 9 [10]; Atk bite 1d4; ML 9; AL N",
    "Pretends to know important secret",
    "Spy for Royal Tax Collectors",
    "Loyal to the last, ML +3",
    "Owns 1d3 potions",
    "Owns random magic item",
    "Shunned in civilisation",
    "Sharpshooter, +1 to ranged atk / damage",
    "Dishevelled appearance",
    "Picks teeth with dagger",
    "Uncanny talent for sniffing out alcohol",
    "Never surprised",
    "Can pick locks, has ring of false keys",
    "Shambling gait",
    "Unhealthy complexion",
    "Others have seen him die 1d3 times",
    "Cross-dresser",
    "Wears heirloom plate mail",
    "Very religious",
    "Never takes lead",
    "Has to be told everything twice",
    "Coward, ML -2",
    "Takes 'sick leave' every other expedition",
    "Contrarian",
    "Delves into battle with cheerful 'Huzzah!', +1 to hit in first round",
    "Landed gentry, owns estate and small chateau, invites company after he gets through 'these difficult times'",
    "Lackwit",
    "Always tries to press forward and pocket small valuables",
    "Steals from party if he can get away with it",
    "Spy for Royal Secret Police",
    "Good fashion-sense, spends all money on frivolities",
    "Gold teeth",
    "Golden heart",
    "Nervous, 1:6 of skipping first round",
    "Strong, +1 damage",
    "Gambler",
    "Escaped convict",
    "Escaped friar/nun",
    "Lovestruck",
    "Obsessed with the secrets of the Underworld",
    "Heavy sleeper, never agrees to go on watch",
    "Bluffs about special abilities",
    "Bluffs about experience",
    "Modest about experience (+1 LVL)",
    "Artful dodger, +1 AC",
    "Skilled pickpocket",
    "Pet crow",
    "Hacking cough",
    "Ex-miner, good sense of direction, senses closest exit",
    "Meticulous, finds things others miss",
    "Equipped with dungeoneering gear – lantern, oil, coil of rope, hammer, spikes, iron rations, pole, and waterskin",
    "Stays behind and tends to get separated from company",
    "Panics in stressful situations 1:6",
    "Constantly begs company for a little extra",
    "Leaves to join rival company after first 1d3 expeditions, spills all",
    "Wants to form own company, encourages companions to join",
    "Keeps on going, +1 HD (to Hp only)",
    "Paranoid",
    "Libertine and free-thinker",
    "Staunch teetotaller",
    "Has heard rumours about location",
    "Adventures to care for sick relative",
    "Pretends to listen to orders, but always does own thing",
    "Owns random magic item",
    "Has own retainer paid out of his own pocket",
    "Always demands extra share from loot",
    "Pockets valuables when nobody is looking",
    "Spreads rumours about other companions",
    "Fat",
    "Expert at appraisal",
    "Skirt-chaser",
    "Outlaw",
    "Strikes twice in first round",
    "Leaves company in hazardous situations",
    "Proactive, tries to second-guess companions and act before they ask",
    "Secret nemesis (1:2 follows, 1:2 followed by)",
    "Obsessed by appearance, carries around box of perfumes and make-up",
    "Pet hawk",
    "Under vampire’s charm",
    "Party animal",
    "Binge-drinking on duty, -1 penalty, cumulative",
    "Never leaves a companion in peril, ML +2",
    "1d6*400 gp from past jobs",
    "Grumbler",
    "At the end of his wits, 1:6 of berserk rage in critical situation, +2 to hit, but 1:3 attacks indiscriminately",
    "Escaped from the gallows",
    "Fencing instructor, 1d3*100 XP to one character on downtime after each expedition",
    "Wants to retire in style after pulling 'that one big job'",
    "Pursues sworn enemy",
    "Has already been down there and lost most of his companions, -2 ML but knows a few places",
    "Scrounger, collects low-value items",
    "Outstanding warrant at constable",
    "Cynic",
    "Accursed",
    "Fanatical, +2 ML and +1 damage",
    "Princeling travelling incognito, LVL +2, departs after 1d3 expeditions with parting gift of 1d6*200 gp per companion"
]


HAIR_COLOUR = [
    "black", "dark brown", "brown", "light brown", "blonde", "platinum blonde", "auburn", 
    "red", "copper", "gray", "silver", "white"
]


HAIR_STYLES = {
    "M": [
        "bushy sideburns", "slicked-back", "short with rolled bangs", "mutton chops", "quiff", 
        "full beard with mustache", "cowlick", "pompadour", "short and neat", "military style",
        "chin-length with side part", "sideburns and mustache", "top hat with coiled hair", 
        "close-cropped", "long side part", "french roll", "slicked-back with sideburns", "ruffled bangs",
        "tied back ponytail", "victorian side part", "wavy and long", "high curls", "genteel curls", 
        "wide-brimmed hat with tucked hair", "classic short curls", "loose curls with mustache"
    ],
    "F": [
        "victorian updo", "tight ringlets", "loose curls", "high bun", "swept back with curls", 
        "braided crown", "pageboy", "bowl cut", "soft finger waves", "chignon", "banged bob", 
        "classic bob", "side-swept curls", "pompadour", "beehive", "plaited bun", "curled fringe", 
        "low chignon", "frizzed curls", "slicked-back curls", "long with ringlet ends", "french twist", 
        "curls piled high", "parted in the middle with waves", "ruffled updo", "bobby pinned curls"
    ]
}


DESCRIPTOR = [
    "scarred", "freckled", "tattooed", "pockmarked", "weathered", "ruddy", "pale", "sallow",
    "piercing-eyed", "squinting", "one-eyed", "glassy-eyed", "sleepy-eyed", "hooded-eyed", "beady-eyed", "bloodshot-eyed",
    "toothy", "gap-toothed", "snaggle-toothed", "toothless", "gold-toothed", "fanged", "grinning", "tight-lipped",
    "stooped", "hunched", "rigid", "lumbering", "graceful", "nimble", "stiff", "twitchy",
    "booming-voiced", "gravelly-voiced", "whispery", "nasally", "lilting", "monotone", "stuttering", "mumbling",
    "smells of sweat", "smells of lavender", "smells of ale", "smells of fish", "smells of incense", "smells of damp earth", "smells of blood", "smells of perfume",
    "eager", "sullen", "cheerful", "brooding", "charming", "abrasive", "aloof", "melancholy",
    "fidgety", "stoic", "pompous", "soft-spoken", "loud", "suspicious", "absent-minded", "cunning",
    "meticulously dressed", "shabby", "threadbare", "filthy", "overdressed", "colorfully dressed", "uniformed", "heavily armored",
    "calloused hands", "ink-stained fingers", "trembling hands", "missing fingers", "clawed hands", "delicate hands", "burn-scarred hands", "heavily-ringed fingers",
    "missing an ear", "tattooed scalp", "hooked nose", "broken nose", "cleft chin", "lantern-jawed", "round-faced", "sunken-cheeked"
]


def true_random_between(low, high):
    random_bytes = os.urandom(4)
    rand_int = struct.unpack("I", random_bytes)[0] 
    val = low + (rand_int % (high - low + 1))
    return val


def roll_die(die: Tuple[int, int], amount: int = 1):
        min_roll = die[0]
        max_roll = die[1]
        rolled = 0
        total = 0
        while rolled < amount:
            total += true_random_between(min_roll, max_roll)
            rolled += 1
        
        return total


class HirelingSquad():
    def __init__(self, hireling_metadata: dict, style: str, separator: str):
        self.separator = separator
        self.style = style
        self.hireling_metadata = hireling_metadata
        self.chance = hireling_metadata['chance']
        self.amount = hireling_metadata['amount']
        self.hirelings = []
    
    def generate(self):
        self.roll = roll_die(D100)
        if self.roll <= self.chance:
            rolled_amount = roll_die(self.amount)
            created = 0
            while created < rolled_amount:
                self.hirelings.append(Hireling(self.hireling_metadata))
                created += 1

    def display(self):
        if self.hirelings:
            if self.style == "cli":
                print(f"---- {self.hireling_metadata['name']} ----")
            for hireling in self.hirelings:
                hireling.display(self.style, self.separator)


class Hireling():
    def __init__(self, hireling_metadata: dict):
        self.hireling_metadata = hireling_metadata
        self.gender = self.__gender()
        self.stats = self.__stats()
        self.hd = self.__hd()
        self.level = self.__level()
        self.hp = self.__hp()
        self.alignment = self.__alignment()
        self.equipment = self.__equipment()
        self.name = self.__name()
        self.quirks = self.__quirks()
        self.description = self.__description()
        self.daily_wage = self.__daily_wage()

    def __hd(self):
        return self.hireling_metadata['hp_die'] if 'hp_die' in self.hireling_metadata else D8
    
    def __level(self):
        level = 1
        if self.hd != D4:
            match roll_die(D6):
                case 6:
                    level = 1 + roll_die(D3)
        
        return level

    def __hp(self):
        return roll_die(self.hd, self.level)

    def __stats(self):
        self.str = roll_die(D6,3)
        self.dex = roll_die(D6,3)
        self.con = roll_die(D6,3)
        self.wis = roll_die(D6,3)
        self.int = roll_die(D6,3)
        self.cha = roll_die(D6,3)

        return f"STR:{self.str} DEX:{self.dex} CON:{self.con} WIS:{self.wis} INT:{self.int} CHA:{self.cha}"

    def __gender(self):
        gender_roll = roll_die(D6) % 2
        gender = "M" if gender_roll > 0 else "F"
        return gender

    def __alignment(self):
        alignment_roll = roll_die(D8)
        alignment = "N"
        match alignment_roll:
            case 1|2:
                alignment = "L"
            case 7|8:
                alignment = "C"
        
        return alignment

    def __weapon(self):
        roll = roll_die(D8)
        weapon = "spear"
        match roll:
            case 4|5:
                weapon = "mace"
            case 6|7:
                weapon = "axe"
            case 8:
                weapon = "sword"
        return weapon

    def __equipment(self):
        weapon = self.__weapon()
        match self.hireling_metadata['name']:
            case Config.LF:
                equipment = f"{Config.LEATHER}, {Config.SHIELD}, {weapon}"
            case Config.HF:
                equipment = f"{Config.CHAIN}, {Config.SHIELD}, {weapon}"
            case Config.BOW:
                equipment = f"{Config.LEATHER}, longbow, mace"
            case Config.XBOW:
                equipment = f"{Config.CHAIN}, crossbow, dagger"
            case _:
                equipment = "no equipment"

        return equipment

    def __name(self):
        return random.choice(NAMES[self.gender])
    
    def __quirks(self):
        match roll_die(D6):
            case 3|4|5:
                quirk_count = 1
            case 6:
                quirk_count = 2
            case _:
                return "No quirks"    
        
        return " | ".join(random.sample(QUIRKS, quirk_count))
    
    def __description(self):
        hair = " ".join(random.sample(HAIR_COLOUR, 1) + random.sample(HAIR_STYLES[self.gender], 1))
        desc = " | ".join([hair] + random.sample(DESCRIPTOR, 1))
        return desc

    def __daily_wage(self):
        return self.level * self.hireling_metadata['base_wage']

    def display(self, style: str, separator: str):
        display_dict = OrderedDict([
            ("name", self.name),
            ("type", self.hireling_metadata['name']),
            ("gender", self.gender),
            ("hd", f"{self.level}d{self.hd[1]}"),
            ("hp", self.hp),
            ("alignment", self.alignment),
            ("daily wage", self.daily_wage),
            ("stats", self.stats),
            ("equipment", self.equipment),
            ("quirks", self.quirks),
            ("description", self.description),
        ])

        match style:
            case 'cli':
                print(f"{separator}".join(f"{k}: {v}" for k, v in display_dict.items()))
            case 'sheets':
                print(separator.join(str(v) for v in list(display_dict.values())))

                    

parser = argparse.ArgumentParser(description="Hireling generator")
parser.add_argument("--display", "-d", choices=['cli','sheets'], default="cli", help="Choose display style")
parser.add_argument("--separator", "-s", default=";", help="Choose separator")
args = parser.parse_args()

for h in HIRELING_TYPES:
    squad = HirelingSquad(h, args.display, args.separator)
    squad.generate()
    squad.display()