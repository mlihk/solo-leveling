import random
from enum import Enum
import ast

class ItemType(Enum):
    WEAPON = "Weapon"
    ARMOR = "Armor"
    ACCESSORY = "Accessory"
    CONSUMABLE = "Consumable"
    SPECIAL = "Special"

class ItemSlot(Enum):
    NONE = "None"  # For consumables and special items
    HEAD = "Head"
    SHOULDER = "Shoulder"
    CHEST = "Chest"
    WRIST = "Wrist"
    HANDS = "Hands"
    WAIST = "Waist"
    LEGS = "Legs"
    FEET = "Feet"
    MAIN_HAND = "Main Hand"
    OFF_HAND = "Off Hand"
    RING = "Ring"

class ItemRarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
    MYTHIC = "Mythic"

class Item:
    def __init__(self, name, item_type, slot, rarity, level_req, stats=None, effect=None):
        self.name = name
        self.item_type = item_type
        self.slot = slot
        self.rarity = rarity
        self.level_req = level_req
        self.stats = stats or {}
        self.effect = effect
        self.classes = []  # List of classes that can use this item
    
    def __str__(self):
        stats_str = ", ".join([f"{stat}: {value}" for stat, value in self.stats.items()])
        effect_str = f"\nEffect: {self.effect}" if self.effect else ""
        return f"{self.name} ({self.rarity.value})\nLevel Required: {self.level_req}\nStats: {stats_str}{effect_str}"
    
    def use(self, player):
        """Use the item on a player. Returns (success, message)."""
        if self.item_type == ItemType.CONSUMABLE:
            if 'heal' in self.stats:
                player.heal(self.stats['heal'])
                return True, f"Restored {self.stats['heal']} health!"
            elif 'mana' in self.stats:
                player.restore_mana(self.stats['mana'])
                return True, f"Restored {self.stats['mana']} mana!"
            elif 'exp' in self.stats:
                player.gain_experience(self.stats['exp'])
                return True, f"Gained {self.stats['exp']} experience!"
        elif self.item_type == ItemType.SPECIAL:
            if self.effect and self.effect.get('type') == 'awakening':
                success, message = player.awaken()
                return success, message
        return False, "This item cannot be used!"
    
    @classmethod
    def from_db_row(cls, row):
        name, item_type, slot, rarity, level_req, stats_str, effect_str = row
        stats = ast.literal_eval(stats_str) if stats_str else {}
        effect = ast.literal_eval(effect_str) if effect_str else None
        return cls(
            name=name,
            item_type=ItemType(item_type),
            slot=ItemSlot(slot),
            rarity=ItemRarity(rarity),
            level_req=level_req,
            stats=stats,
            effect=effect
        )

class Equipment(Item):
    def __init__(self, name, slot, rarity, level_req, stats=None, abilities=None, classes=None):
        super().__init__(name, ItemType.ARMOR, slot, rarity, level_req, stats, None)
        self.abilities = abilities or []
        self.classes = classes or []  # Empty list means all classes can use it
        
        # Apply rarity multiplier to stats
        for stat in self.stats:
            self.stats[stat] = int(self.stats[stat] * rarity.stat_multiplier)

class Weapon(Item):
    def __init__(self, name, slot, rarity, level_req, damage, stats=None, abilities=None, classes=None):
        super().__init__(name, ItemType.WEAPON, slot, rarity, level_req, stats, None)
        self.damage = int(damage * rarity.stat_multiplier)
        self.abilities = abilities or []
        self.classes = classes or []  # Empty list means all classes can use it

class Ring(Item):
    def __init__(self, name, rarity, level_req, stats=None, abilities=None, classes=None):
        super().__init__(name, ItemType.ACCESSORY, ItemSlot.RING, rarity, level_req, stats, None)
        self.abilities = abilities or []
        self.classes = classes or []  # Empty list means all classes can use it

# Item Factory for generating random items
class ItemFactory:
    @staticmethod
    def generate_random_item(level, rarity=None):
        if rarity is None:
            rarity = random.choices(list(ItemRarity), weights=[50, 30, 15, 4, 0.9, 0.1])[0]
        
        # Base stats based on level
        base_stats = {
            'strength': level * 2,
            'agility': level * 2,
            'intelligence': level * 2,
            'vitality': level * 2,
            'defense': level
        }
        
        # Randomly select stats to include
        num_stats = random.randint(1, 3)
        selected_stats = dict(random.sample(base_stats.items(), num_stats))
        
        # Generate random abilities (chance increases with rarity)
        abilities = []
        if random.random() < (rarity.value * 0.1):
            abilities.append("Random ability")  # TODO: Implement actual abilities
        
        # Create item based on type
        item_type = random.choice([ItemType.WEAPON, ItemType.ARMOR, ItemType.ACCESSORY])
        
        if item_type == ItemType.WEAPON:
            slot = random.choice([ItemSlot.MAIN_HAND, ItemSlot.OFF_HAND])
            return Weapon(
                name=f"Random {slot.value} weapon",
                slot=slot,
                rarity=rarity,
                level_req=level,
                damage=level * 5,
                stats=selected_stats,
                abilities=abilities
            )
        elif item_type == ItemType.ARMOR:
            slot = random.choice(list(ItemSlot)[:8])  # First 8 slots are armor
            return Equipment(
                name=f"Random {slot.value} armor",
                slot=slot,
                rarity=rarity,
                level_req=level,
                stats=selected_stats,
                abilities=abilities
            )
        else:  # Accessory (Ring)
            return Ring(
                name="Random ring",
                rarity=rarity,
                level_req=level,
                stats=selected_stats,
                abilities=abilities
            ) 