import sqlite3
import os
import random
from pathlib import Path
from models.items import ItemType, ItemSlot, ItemRarity
from models.effects import EffectType

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

DB_PATH = data_dir / "game.db"

def get_db_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def generate_random_stats(rarity, level_req):
    # Get the base stat range for the level
    min_stats = level_req * 10
    max_stats = level_req * 20
    
    # Apply rarity multiplier
    rarity_multipliers = {
        ItemRarity.COMMON: 1.0,
        ItemRarity.UNCOMMON: 1.5,
        ItemRarity.RARE: 2.0,
        ItemRarity.EPIC: 2.5,
        ItemRarity.LEGENDARY: 3.0,
        ItemRarity.MYTHIC: 4.0
    }
    multiplier = rarity_multipliers[rarity]
    
    min_stats = int(min_stats * multiplier)
    max_stats = int(max_stats * multiplier)
    
    # Generate total stats for the item
    total_stats = random.randint(min_stats, max_stats)
    
    # Distribute stats among different attributes
    stats = {
        'strength': 0,
        'agility': 0,
        'intelligence': 0,
        'vitality': 0,
        'defense': 0
    }
    
    # Distribute stats randomly
    remaining_stats = total_stats
    attributes = list(stats.keys())
    
    while remaining_stats > 0 and attributes:
        # Choose a random attribute
        attr = random.choice(attributes)
        # Calculate how much to add (at least 1, at most remaining_stats)
        amount = random.randint(1, max(1, remaining_stats // len(attributes)))
        stats[attr] += amount
        remaining_stats -= amount
        # Remove the attribute if it's received enough stats
        if stats[attr] >= total_stats * 0.4:  # No attribute should get more than 40% of total stats
            attributes.remove(attr)
    
    return stats

def generate_random_effect(rarity):
    if rarity == ItemRarity.COMMON:
        return None
    
    effect_chance = {
        ItemRarity.UNCOMMON: 0.3,
        ItemRarity.RARE: 0.5,
        ItemRarity.EPIC: 0.7,
        ItemRarity.LEGENDARY: 0.9,
        ItemRarity.MYTHIC: 1.0
    }
    
    if random.random() < effect_chance[rarity]:
        effect_type = random.choice(list(EffectType))
        duration = random.randint(2, 5)
        power = random.randint(1, 3)
        return {
            'type': effect_type.value,
            'duration': duration,
            'power': power
        }
    
    return None

def generate_special_bonus(rarity, level_req):
    # Special bonuses are only available for Epic and above items
    if rarity not in [ItemRarity.EPIC, ItemRarity.LEGENDARY, ItemRarity.MYTHIC]:
        return None
    
    # Higher level items have better chance for special bonuses
    bonus_chance = {
        ItemRarity.EPIC: 0.1 + (level_req / 1000),  # 10% at level 1, up to 20% at level 100
        ItemRarity.LEGENDARY: 0.2 + (level_req / 500),  # 20% at level 1, up to 40% at level 100
        ItemRarity.MYTHIC: 0.3 + (level_req / 333)  # 30% at level 1, up to 60% at level 100
    }
    
    if random.random() < bonus_chance[rarity]:
        special_bonuses = [
            {
                'type': 'stat_boost',
                'description': 'Increases all stats by 1%',
                'value': 0.01
            },
            {
                'type': 'portal_chance',
                'description': 'Increases chance for portals to spawn by 5%',
                'value': 0.05
            },
            {
                'type': 'instant_kill',
                'description': 'Has a 1% chance to instantly kill enemies below 1% health',
                'value': 0.01
            },
            {
                'type': 'exp_boost',
                'description': 'Increases experience gained by 5%',
                'value': 0.05
            },
            {
                'type': 'gold_boost',
                'description': 'Increases gold gained by 5%',
                'value': 0.05
            }
        ]
        
        # Higher rarity items can get multiple bonuses
        num_bonuses = {
            ItemRarity.EPIC: 1,
            ItemRarity.LEGENDARY: random.randint(1, 2),
            ItemRarity.MYTHIC: random.randint(1, 3)
        }
        
        selected_bonuses = random.sample(special_bonuses, num_bonuses[rarity])
        return selected_bonuses
    
    return None

def generate_items():
    """Generate random items and insert them into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Generate weapons
    for _ in range(50):
        rarity = random.choice(list(ItemRarity))
        level_req = random.randint(1, 100)
        stats = generate_random_stats(rarity, level_req)
        effect = generate_random_effect(rarity)
        special_bonus = generate_special_bonus(rarity, level_req)
        
        # Generate weapon name based on rarity
        prefixes = {
            ItemRarity.COMMON: ['Basic', 'Simple', 'Standard'],
            ItemRarity.UNCOMMON: ['Fine', 'Sturdy', 'Reinforced'],
            ItemRarity.RARE: ['Mighty', 'Powerful', 'Deadly'],
            ItemRarity.EPIC: ['Ancient', 'Mystic', 'Enchanted'],
            ItemRarity.LEGENDARY: ['Divine', 'Celestial', 'Eternal'],
            ItemRarity.MYTHIC: ['Cosmic', 'Primordial', 'Infinite']
        }
        weapons = ['Sword', 'Axe', 'Mace', 'Dagger', 'Staff', 'Bow', 'Spear', 'Hammer']
        name = f"{random.choice(prefixes[rarity])} {random.choice(weapons)}"
        
        cursor.execute('''
            INSERT INTO items (name, type, slot, rarity, level_req, stats, effect, special_bonus)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name,
            ItemType.WEAPON.value,
            ItemSlot.MAIN_HAND.value,
            rarity.value,
            level_req,
            str(stats),
            str(effect) if effect else None,
            str(special_bonus) if special_bonus else None
        ))
    
    # Generate armor
    for slot in [ItemSlot.HEAD, ItemSlot.SHOULDER, ItemSlot.CHEST, ItemSlot.WRIST,
                 ItemSlot.HANDS, ItemSlot.WAIST, ItemSlot.LEGS, ItemSlot.FEET]:
        for _ in range(30):
            rarity = random.choice(list(ItemRarity))
            level_req = random.randint(1, 100)
            stats = generate_random_stats(rarity, level_req)
            effect = generate_random_effect(rarity)
            special_bonus = generate_special_bonus(rarity, level_req)
            
            # Generate armor name based on rarity and slot
            prefixes = {
                ItemRarity.COMMON: ['Basic', 'Simple', 'Standard'],
                ItemRarity.UNCOMMON: ['Fine', 'Sturdy', 'Reinforced'],
                ItemRarity.RARE: ['Mighty', 'Powerful', 'Protected'],
                ItemRarity.EPIC: ['Ancient', 'Mystic', 'Enchanted'],
                ItemRarity.LEGENDARY: ['Divine', 'Celestial', 'Eternal'],
                ItemRarity.MYTHIC: ['Cosmic', 'Primordial', 'Infinite']
            }
            slot_names = {
                ItemSlot.HEAD: 'Helmet',
                ItemSlot.SHOULDER: 'Pauldrons',
                ItemSlot.CHEST: 'Chestplate',
                ItemSlot.WRIST: 'Bracers',
                ItemSlot.HANDS: 'Gauntlets',
                ItemSlot.WAIST: 'Belt',
                ItemSlot.LEGS: 'Greaves',
                ItemSlot.FEET: 'Boots'
            }
            name = f"{random.choice(prefixes[rarity])} {slot_names[slot]}"
            
            cursor.execute('''
                INSERT INTO items (name, type, slot, rarity, level_req, stats, effect, special_bonus)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                name,
                ItemType.ARMOR.value,
                slot.value,
                rarity.value,
                level_req,
                str(stats),
                str(effect) if effect else None,
                str(special_bonus) if special_bonus else None
            ))
    
    # Generate rings
    for _ in range(40):
        rarity = random.choice(list(ItemRarity))
        level_req = random.randint(1, 100)
        stats = generate_random_stats(rarity, level_req)
        effect = generate_random_effect(rarity)
        special_bonus = generate_special_bonus(rarity, level_req)
        
        # Generate ring name based on rarity
        prefixes = {
            ItemRarity.COMMON: ['Basic', 'Simple', 'Standard'],
            ItemRarity.UNCOMMON: ['Fine', 'Sturdy', 'Reinforced'],
            ItemRarity.RARE: ['Mighty', 'Powerful', 'Protected'],
            ItemRarity.EPIC: ['Ancient', 'Mystic', 'Enchanted'],
            ItemRarity.LEGENDARY: ['Divine', 'Celestial', 'Eternal'],
            ItemRarity.MYTHIC: ['Cosmic', 'Primordial', 'Infinite']
        }
        ring_types = ['Ring', 'Band', 'Signet', 'Seal']
        name = f"{random.choice(prefixes[rarity])} {random.choice(ring_types)}"
        
        cursor.execute('''
            INSERT INTO items (name, type, slot, rarity, level_req, stats, effect, special_bonus)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name,
            ItemType.ACCESSORY.value,
            ItemSlot.RING.value,
            rarity.value,
            level_req,
            str(stats),
            str(effect) if effect else None,
            str(special_bonus) if special_bonus else None
        ))
    
    # Generate consumables and special items
    consumables = [
        {
            'name': 'Health Potion',
            'type': ItemType.CONSUMABLE.value,
            'slot': ItemSlot.NONE.value,
            'rarity': ItemRarity.COMMON.value,
            'level_req': 1,
            'stats': str({'heal': 50}),
            'effect': None,
            'special_bonus': None
        },
        {
            'name': 'Greater Health Potion',
            'type': ItemType.CONSUMABLE.value,
            'slot': ItemSlot.NONE.value,
            'rarity': ItemRarity.UNCOMMON.value,
            'level_req': 10,
            'stats': str({'heal': 100}),
            'effect': None,
            'special_bonus': None
        },
        {
            'name': 'Mana Potion',
            'type': ItemType.CONSUMABLE.value,
            'slot': ItemSlot.NONE.value,
            'rarity': ItemRarity.COMMON.value,
            'level_req': 1,
            'stats': str({'mana': 50}),
            'effect': None,
            'special_bonus': None
        },
        {
            'name': 'Greater Mana Potion',
            'type': ItemType.CONSUMABLE.value,
            'slot': ItemSlot.NONE.value,
            'rarity': ItemRarity.UNCOMMON.value,
            'level_req': 10,
            'stats': str({'mana': 100}),
            'effect': None,
            'special_bonus': None
        },
        {
            'name': 'Awakening Stone',
            'type': ItemType.SPECIAL.value,
            'slot': ItemSlot.NONE.value,
            'rarity': ItemRarity.RARE.value,
            'level_req': 10,
            'stats': str({}),
            'effect': str({'type': 'awakening', 'description': 'Allows a level 10 player to awaken to a class'}),
            'special_bonus': None
        },
        {
            'name': 'Experience Scroll',
            'type': ItemType.CONSUMABLE.value,
            'slot': ItemSlot.NONE.value,
            'rarity': ItemRarity.UNCOMMON.value,
            'level_req': 1,
            'stats': str({'exp': 100}),
            'effect': None,
            'special_bonus': None
        },
        {
            'name': 'Greater Experience Scroll',
            'type': ItemType.CONSUMABLE.value,
            'slot': ItemSlot.NONE.value,
            'rarity': ItemRarity.RARE.value,
            'level_req': 20,
            'stats': str({'exp': 500}),
            'effect': None,
            'special_bonus': None
        }
    ]
    
    for item in consumables:
        cursor.execute('''
            INSERT INTO items (name, type, slot, rarity, level_req, stats, effect, special_bonus)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['name'],
            item['type'],
            item['slot'],
            item['rarity'],
            item['level_req'],
            item['stats'],
            item['effect'],
            item['special_bonus']
        ))
    
    conn.commit()
    conn.close()

def initialize_database():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Drop existing tables to ensure clean schema
    cursor.execute("DROP TABLE IF EXISTS items")
    cursor.execute("DROP TABLE IF EXISTS accounts")
    cursor.execute("DROP TABLE IF EXISTS players")
    cursor.execute("DROP TABLE IF EXISTS shadows")
    
    # Create items table
    cursor.execute("""
        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            slot TEXT NOT NULL,
            rarity TEXT NOT NULL,
            level_req INTEGER NOT NULL,
            stats TEXT NOT NULL,
            effect TEXT,
            special_bonus TEXT,
            set_name TEXT,
            set_bonus TEXT
        )
    """)
    
    # Create accounts table
    cursor.execute("""
        CREATE TABLE accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create players table
    cursor.execute("""
        CREATE TABLE players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            experience INTEGER DEFAULT 0,
            health INTEGER DEFAULT 100,
            max_health INTEGER DEFAULT 100,
            mana INTEGER DEFAULT 100,
            max_mana INTEGER DEFAULT 100,
            strength INTEGER DEFAULT 10,
            dexterity INTEGER DEFAULT 10,
            intelligence INTEGER DEFAULT 10,
            vitality INTEGER DEFAULT 10,
            gold INTEGER DEFAULT 0,
            inventory TEXT DEFAULT '[]',
            equipment TEXT DEFAULT '{}',
            rings TEXT DEFAULT '[]',
            shadows TEXT DEFAULT '[]',
            player_class TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_saved TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    """)
    
    # Create shadows table
    cursor.execute('''
        CREATE TABLE shadows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            shadow_name TEXT NOT NULL,
            shadow_type TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            strength INTEGER DEFAULT 10,
            defense INTEGER DEFAULT 10,
            agility INTEGER DEFAULT 10,
            mana_cost INTEGER DEFAULT 50,
            health INTEGER DEFAULT 100,
            max_health INTEGER DEFAULT 100,
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    # Generate items after creating the tables
    generate_items()
    
    print("Database initialized successfully") 