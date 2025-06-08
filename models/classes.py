from enum import Enum
import random

class PlayerClass(Enum):
    WARRIOR = "Warrior"
    MAGE = "Mage"
    ROGUE = "Rogue"
    PRIEST = "Priest"
    HUNTER = "Hunter"
    PALADIN = "Paladin"
    NECROMANCER = "Necromancer"
    BERSERKER = "Berserker"
    ASSASSIN = "Assassin"
    SHADOW_KNIGHT = "Shadow Knight"

class ClassAbility:
    def __init__(self, name, description, damage_multiplier, mana_cost, cooldown, effects=None):
        self.name = name
        self.description = description
        self.damage_multiplier = damage_multiplier
        self.mana_cost = mana_cost
        self.cooldown = cooldown
        self.effects = effects or {}

class ClassStats:
    def __init__(self, strength, agility, intelligence, vitality, defense):
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.vitality = vitality
        self.defense = defense

class ClassDefinition:
    def __init__(self, player_class, base_stats, abilities, description, strengths, weaknesses):
        self.player_class = player_class
        self.base_stats = base_stats
        self.abilities = abilities
        self.description = description
        self.strengths = strengths
        self.weaknesses = weaknesses

# Define all classes
CLASSES = {
    PlayerClass.WARRIOR: ClassDefinition(
        player_class=PlayerClass.WARRIOR,
        base_stats=ClassStats(
            strength=10,
            agility=5,
            intelligence=3,
            vitality=8,
            defense=7
        ),
        abilities=[
            ClassAbility("Whirlwind", "Spin attack hitting all enemies", 1.5, 20, 3),
            ClassAbility("Battle Cry", "Increases attack power", 0, 15, 5, {"attack_boost": 1.5}),
            ClassAbility("Shield Wall", "Reduces incoming damage", 0, 25, 8, {"damage_reduction": 0.5})
        ],
        description="A master of weapons and combat, specializing in close-quarters combat.",
        strengths=["High physical damage", "Good defense", "Strong melee abilities"],
        weaknesses=["Low magic resistance", "Limited range", "High mana costs"]
    ),
    PlayerClass.MAGE: ClassDefinition(
        player_class=PlayerClass.MAGE,
        base_stats=ClassStats(
            strength=3,
            agility=4,
            intelligence=12,
            vitality=5,
            defense=4
        ),
        abilities=[
            ClassAbility("Fireball", "Launches a ball of fire", 2.0, 15, 2),
            ClassAbility("Ice Shield", "Creates a protective ice barrier", 0, 20, 6, {"defense_boost": 1.5}),
            ClassAbility("Arcane Explosion", "Area damage spell", 1.8, 30, 5)
        ],
        description="A wielder of arcane magic, capable of devastating spells.",
        strengths=["High magic damage", "Area effects", "Strong crowd control"],
        weaknesses=["Low health", "Weak defense", "Long cooldowns"]
    ),
    PlayerClass.ROGUE: ClassDefinition(
        player_class=PlayerClass.ROGUE,
        base_stats=ClassStats(
            strength=6,
            agility=12,
            intelligence=5,
            vitality=6,
            defense=5
        ),
        abilities=[
            ClassAbility("Backstab", "High damage from behind", 2.5, 10, 3),
            ClassAbility("Stealth", "Become invisible", 0, 15, 8, {"invisibility": True}),
            ClassAbility("Poison Strike", "Apply poison damage over time", 1.2, 20, 4, {"poison": True})
        ],
        description="A master of stealth and precision strikes.",
        strengths=["High critical damage", "Stealth abilities", "Fast attacks"],
        weaknesses=["Low defense", "Limited AoE", "Position dependent"]
    ),
    PlayerClass.PRIEST: ClassDefinition(
        player_class=PlayerClass.PRIEST,
        base_stats=ClassStats(
            strength=4,
            agility=4,
            intelligence=10,
            vitality=7,
            defense=5
        ),
        abilities=[
            ClassAbility("Heal", "Restore health to target", 0, 20, 3, {"healing": 1.5}),
            ClassAbility("Holy Shield", "Protective barrier", 0, 25, 6, {"damage_reduction": 0.7}),
            ClassAbility("Smite", "Holy damage spell", 1.5, 15, 2)
        ],
        description="A divine spellcaster focused on healing and support.",
        strengths=["Healing abilities", "Support spells", "Good survivability"],
        weaknesses=["Low damage", "Limited offensive abilities", "Mana dependent"]
    ),
    PlayerClass.HUNTER: ClassDefinition(
        player_class=PlayerClass.HUNTER,
        base_stats=ClassStats(
            strength=7,
            agility=10,
            intelligence=6,
            vitality=6,
            defense=5
        ),
        abilities=[
            ClassAbility("Precise Shot", "High damage single target", 2.0, 15, 3),
            ClassAbility("Trap", "Immobilize target", 0, 20, 5, {"immobilize": True}),
            ClassAbility("Multi-Shot", "Hit multiple targets", 1.5, 25, 4)
        ],
        description="A master of ranged combat and tracking.",
        strengths=["Long range", "High accuracy", "Good mobility"],
        weaknesses=["Close combat weakness", "Limited defense", "Ammo dependent"]
    ),
    PlayerClass.PALADIN: ClassDefinition(
        player_class=PlayerClass.PALADIN,
        base_stats=ClassStats(
            strength=8,
            agility=5,
            intelligence=7,
            vitality=9,
            defense=8
        ),
        abilities=[
            ClassAbility("Holy Strike", "Holy-infused attack", 1.8, 20, 3),
            ClassAbility("Divine Shield", "Invulnerability", 0, 30, 10, {"invulnerable": True}),
            ClassAbility("Consecration", "Area holy damage", 1.2, 25, 5)
        ],
        description="A holy warrior combining combat and divine magic.",
        strengths=["Balanced stats", "Good defense", "Healing abilities"],
        weaknesses=["Average damage", "High cooldowns", "Mana management"]
    ),
    PlayerClass.NECROMANCER: ClassDefinition(
        player_class=PlayerClass.NECROMANCER,
        base_stats=ClassStats(
            strength=4,
            agility=5,
            intelligence=11,
            vitality=6,
            defense=4
        ),
        abilities=[
            ClassAbility("Raise Dead", "Summon undead minion", 0, 30, 8, {"summon": True}),
            ClassAbility("Death Bolt", "Dark damage spell", 1.8, 20, 3),
            ClassAbility("Life Drain", "Steal life from target", 1.2, 25, 5, {"life_steal": True})
        ],
        description="A master of death magic and undead minions.",
        strengths=["Summoning", "Life steal", "Dark magic"],
        weaknesses=["Low defense", "Minion dependent", "Complex mechanics"]
    ),
    PlayerClass.BERSERKER: ClassDefinition(
        player_class=PlayerClass.BERSERKER,
        base_stats=ClassStats(
            strength=12,
            agility=8,
            intelligence=3,
            vitality=10,
            defense=6
        ),
        abilities=[
            ClassAbility("Rage", "Increase damage and speed", 0, 20, 6, {"damage_boost": 2.0, "speed_boost": 1.5}),
            ClassAbility("Whirlwind", "Spin attack", 1.5, 25, 4),
            ClassAbility("Berserk", "Sacrifice defense for damage", 0, 30, 8, {"defense_reduction": 0.5, "damage_boost": 2.5})
        ],
        description="A fierce warrior who grows stronger in battle.",
        strengths=["High damage", "Rage mechanics", "Good health"],
        weaknesses=["Low defense when enraged", "Mana dependent", "Self-damage"]
    ),
    PlayerClass.ASSASSIN: ClassDefinition(
        player_class=PlayerClass.ASSASSIN,
        base_stats=ClassStats(
            strength=7,
            agility=11,
            intelligence=6,
            vitality=5,
            defense=5
        ),
        abilities=[
            ClassAbility("Shadow Strike", "Teleport and attack", 2.2, 20, 4),
            ClassAbility("Poison Cloud", "Area poison damage", 1.3, 25, 6, {"poison": True}),
            ClassAbility("Death Mark", "Mark target for increased damage", 0, 30, 8, {"damage_boost": 2.0})
        ],
        description="A deadly warrior specializing in quick, fatal strikes.",
        strengths=["High burst damage", "Mobility", "Poison effects"],
        weaknesses=["Low health", "Position dependent", "Complex combos"]
    ),
    PlayerClass.SHADOW_KNIGHT: ClassDefinition(
        player_class=PlayerClass.SHADOW_KNIGHT,
        base_stats=ClassStats(
            strength=9,
            agility=7,
            intelligence=8,
            vitality=8,
            defense=7
        ),
        abilities=[
            ClassAbility("Shadow Slash", "Dark-infused attack", 1.8, 20, 3),
            ClassAbility("Dark Shield", "Shadow barrier", 0, 25, 6, {"damage_reduction": 0.6}),
            ClassAbility("Shadow Clone", "Create a shadow copy", 0, 30, 8, {"clone": True})
        ],
        description="A warrior wielding both physical and shadow powers.",
        strengths=["Balanced abilities", "Shadow powers", "Good defense"],
        weaknesses=["Complex mechanics", "Mana management", "Cooldown dependent"]
    )
}

def get_random_class():
    return random.choice(list(PlayerClass)) 