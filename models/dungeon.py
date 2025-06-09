import random
from models.enemy import EnemyFactory
from models.effects import EffectType
from .enemy import Enemy
from .puzzle import Puzzle

class Dungeon:
    def __init__(self):
        self.current_difficulty = 1
        self.max_difficulty = 100
        self.current_encounter = 0
        self.total_encounters = 5  # Number of rooms per dungeon run
        self.encounters_completed = 0
        self.rewards_claimed = False
        self.current_enemy = None
        self.story_progress = 0
        self.current_room_type = None
        self.current_puzzle = None
        
        # Room types and their probabilities
        self.room_types = {
            'combat': 0.4,      # 40% chance for combat
            'puzzle': 0.25,     # 25% chance for puzzle
            'trap': 0.2,        # 20% chance for trap
            'treasure': 0.15    # 15% chance for treasure
        }
        
        # Story elements for different difficulty tiers
        self.story_tiers = {
            (0, 20): "The Abandoned Mine",
            (21, 40): "The Cursed Forest",
            (41, 60): "The Ancient Ruins",
            (61, 80): "The Demon's Lair",
            (81, 100): "The Void Realm"
        }
        
        # Story progression for each tier
        self.story_progression = {
            (0, 20): [
                "You enter the abandoned mine, its dark tunnels stretching endlessly...",
                "The sound of pickaxes echoes through the tunnels...",
                "You discover an ancient mining cart filled with strange artifacts...",
                "The mine's guardian appears, corrupted by dark energy...",
                "The mine's core chamber reveals a powerful crystal..."
            ],
            (21, 40): [
                "The cursed forest's trees whisper dark secrets...",
                "Ancient spirits manifest from the twisted branches...",
                "A sacred grove reveals itself, protected by nature's guardians...",
                "The forest's heart pulses with corrupted energy...",
                "The source of the curse reveals itself..."
            ],
            (41, 60): [
                "The ancient ruins stand as a testament to a forgotten civilization...",
                "Guardian constructs awaken from their slumber...",
                "Ancient magic still flows through the ruins...",
                "The ruins' central chamber holds powerful artifacts...",
                "The ruins' master awakens from its eternal rest..."
            ],
            (61, 80): [
                "The demon's lair reeks of sulfur and death...",
                "Lesser demons patrol the corrupted halls...",
                "The lair's power source pulses with demonic energy...",
                "A demonic ritual is in progress...",
                "The demon lord reveals itself..."
            ],
            (81, 100): [
                "The void realm exists between dimensions...",
                "Reality itself warps and twists...",
                "Void creatures manifest from the darkness...",
                "The fabric of space-time weakens...",
                "The void lord emerges from the darkness..."
            ]
        }
        
        # Room descriptions for each type
        self.room_descriptions = {
            'combat': [
                "A group of monsters blocks your path.",
                "A powerful enemy stands before you.",
                "The room is filled with hostile creatures.",
                "A boss monster awaits your challenge."
            ],
            'puzzle': [
                "Ancient runes glow on the walls. Decipher them to continue.",
                "A complex mechanism blocks the way forward.",
                "Mysterious symbols float in the air.",
                "A magical barrier requires solving a puzzle to pass."
            ],
            'trap': [
                "Pressure plates cover the floor.",
                "Poisonous darts line the walls.",
                "A pit of spikes lies ahead.",
                "Magical traps are scattered throughout."
            ],
            'treasure': [
                "A chest of gold gleams in the corner.",
                "Valuable artifacts are scattered about.",
                "A magical treasure chest awaits.",
                "Rare items are protected by a simple lock."
            ]
        }
    
    def get_current_tier(self):
        """Get the current difficulty tier."""
        for (min_difficulty, max_difficulty) in self.story_tiers.keys():
            if min_difficulty <= self.current_difficulty <= max_difficulty:
                return (min_difficulty, max_difficulty)
        return (0, 20)  # Default tier
    
    def get_dungeon_name(self):
        """Get the name of the current dungeon based on difficulty."""
        if self.current_difficulty <= 20:
            return "Tier 1 Dungeon"
        elif self.current_difficulty <= 40:
            return "Tier 2 Dungeon"
        elif self.current_difficulty <= 60:
            return "Tier 3 Dungeon"
        elif self.current_difficulty <= 80:
            return "Tier 4 Dungeon"
        else:
            return "Tier 5 Dungeon"
    
    def get_story_progress(self):
        """Get the story progress based on completed encounters."""
        if self.encounters_completed == 0:
            return "You stand at the entrance of the dungeon, ready to begin your journey."
        elif self.encounters_completed < self.total_encounters:
            return f"You have completed {self.encounters_completed} out of {self.total_encounters} rooms."
        else:
            return "You have reached the end of the dungeon. Claim your rewards!"
    
    def get_room_description(self):
        """Get a random description for the current room type."""
        if self.current_room_type in self.room_descriptions:
            return random.choice(self.room_descriptions[self.current_room_type])
        return "An empty room."
    
    def generate_enemy(self, player_level):
        """Generate an enemy for the current encounter."""
        # Base enemy level increases with difficulty
        base_level = player_level + (self.current_difficulty // 10)
        
        # Add some randomness to the level
        level_variation = random.randint(-2, 2)
        enemy_level = max(1, base_level + level_variation)
        
        # Create the enemy
        enemy = EnemyFactory.create_enemy(enemy_level)
        
        # Scale enemy stats based on difficulty
        scale_factor = 1 + (self.current_difficulty * 0.3)  # 30% increase per difficulty level
        enemy.health = int(enemy.health * scale_factor)
        enemy.max_health = enemy.health
        enemy.strength = int(enemy.strength * scale_factor)
        enemy.defense = int(enemy.defense * scale_factor)
        enemy.agility = int(enemy.agility * scale_factor)
        
        # Increase rewards
        enemy.experience_reward = int(enemy.experience_reward * scale_factor)
        enemy.gold_reward = int(enemy.gold_reward * scale_factor)
        
        # Add special effects based on difficulty tier
        tier = self.get_current_tier()
        if tier == (21, 40):  # Cursed Forest
            enemy.curse_immunity = True
        elif tier == (41, 60):  # Ancient Ruins
            enemy.fire_immunity = True
        elif tier == (61, 80):  # Demon's Lair
            enemy.fire_immunity = True
            enemy.curse_immunity = True
        elif tier == (81, 100):  # Void Realm
            enemy.fire_immunity = True
            enemy.curse_immunity = True
            enemy.strength *= 1.2
            enemy.health *= 1.2
        
        return enemy
    
    def start_new_run(self):
        """Start a new dungeon run."""
        self.current_encounter = 0
        self.encounters_completed = 0
        self.rewards_claimed = False
        self.story_progress = 0
        self.current_room_type = None
        self.current_puzzle = None
        return self.advance_encounter(1)  # Start with level 1
    
    def select_room_type(self):
        """Select a random room type based on probabilities."""
        room_types = list(self.room_types.keys())
        probabilities = list(self.room_types.values())
        return random.choices(room_types, probabilities)[0]
    
    def advance_encounter(self, player_level):
        """Advance to the next encounter."""
        if self.encounters_completed >= self.total_encounters:
            return None
        
        self.encounters_completed += 1
        self.current_room_type = self.select_room_type()
        
        if self.current_room_type == 'combat':
            return self.generate_enemy(player_level)
        elif self.current_room_type == 'puzzle':
            self.current_puzzle = Puzzle(self.current_difficulty)
            return None
        return None
    
    def increase_difficulty(self):
        """Increase the dungeon difficulty."""
        if self.current_difficulty < self.max_difficulty:
            self.current_difficulty += 1
            return True
        return False
    
    def reset_difficulty(self):
        """Reset the dungeon difficulty to 1."""
        self.current_difficulty = 1
        self.encounters_completed = 0
        self.rewards_claimed = False
        self.current_room_type = None
        self.current_puzzle = None
    
    def get_difficulty_multiplier(self):
        """Get the current difficulty multiplier for rewards."""
        return 1 + (self.current_difficulty * 0.3)  # 30% increase per difficulty level
    
    def get_current_puzzle(self):
        """Get the current puzzle if in a puzzle room."""
        if self.current_room_type == 'puzzle' and self.current_puzzle:
            return self.current_puzzle
        return None 