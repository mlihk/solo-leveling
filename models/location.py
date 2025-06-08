import random
from models.enemy import EnemyFactory
from models.effects import EffectType

class GameTime:
    def __init__(self):
        self.hours = 0
        self.days = 1
    
    def advance_time(self, hours):
        self.hours += hours
        if self.hours >= 24:
            self.days += 1
            self.hours = 0
    
    def get_time_string(self):
        return f"{self.hours:02d}:00"
    
    def get_day_string(self):
        return f"Day {self.days}"
    
    def get_remaining_hours(self):
        return 24 - self.hours

class Location:
    def __init__(self, name, description, events=None):
        self.name = name
        self.description = description
        self.events = events or []
    
    def get_random_event(self, player_level):
        # Filter events based on player level and random chance
        available_events = [event for event in self.events 
                          if event.min_level <= player_level and random.random() < event.trigger_chance]
        return random.choice(available_events) if available_events else None

class Event:
    def __init__(self, description, min_level, trigger_chance, event_type, rewards=None):
        self.description = description
        self.min_level = min_level
        self.trigger_chance = trigger_chance
        self.event_type = event_type
        self.rewards = rewards or {}

# Define locations
LOCATIONS = {
    'home': Location(
        "Home",
        "Your safe haven. Here you can rest and recover your health and mana.",
        [
            Event("You rest and recover your strength.", 1, 1.0, 'rest', {'health': 50, 'mana': 50}),
            Event("You practice your skills.", 1, 1.0, 'training', {'experience': 10})
        ]
    ),
    'supermarket': Location(
        "Supermarket",
        "A place to buy food and supplies. You might find some useful items here.",
        [
            Event("You browse the shelves for items.", 1, 1.0, 'shop', {}),
            Event("A thief tries to steal from you!", 1, 0.3, 'combat', {})
        ]
    ),
    'item_store': Location(
        "Item Store",
        "A shop that sells various equipment and items. The inventory refreshes daily.",
        [
            Event("You browse the available items.", 1, 1.0, 'shop', {})
        ]
    ),
    'park': Location(
        "Park",
        "A peaceful place where you can train and encounter weak monsters.",
        [
            Event("A wild animal attacks!", 1, 0.4, 'combat', {}),
            Event("You practice your combat skills.", 1, 0.6, 'training', {'experience': 20}),
            Event("You take a short rest.", 1, 0.5, 'rest', {'health': 20, 'mana': 20})
        ]
    ),
    'dungeon': Location(
        "Dungeon",
        "A dangerous place filled with monsters. The deeper you go, the stronger they become.",
        [
            Event("A monster appears!", 1, 0.7, 'combat', {}),
            Event("You find a treasure chest!", 1, 0.3, 'treasure', {'gold': 100}),
            Event("You discover a mysterious portal.", 1, 0.1, 'portal', {})
        ]
    ),
    'guild': Location(
        "Guild",
        "A place where hunters gather. You can take on quests and meet other hunters.",
        [
            Event("A new quest is available!", 1, 0.4, 'quest', {}),
            Event("You learn from other hunters.", 1, 0.6, 'training', {'experience': 30})
        ]
    ),
    'tower_of_trial': Location(
        "Tower of Trial",
        "A mysterious tower with 100 floors. Each floor presents a stronger challenge. Clear all floors to become the strongest!",
        [
            Event("A trial guardian appears!", 1, 1.0, 'combat', {}),
            Event("You find a trial reward!", 1, 0.3, 'treasure', {'gold': 200}),
            Event("The trial strengthens you!", 1, 0.5, 'training', {'experience': 50})
        ]
    )
} 