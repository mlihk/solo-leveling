import bcrypt
from config.database import get_db_connection
import sqlite3
from models.items import ItemSlot, ItemType
from models.classes import PlayerClass, CLASSES, get_random_class
import json
import hashlib
from datetime import datetime

class Player:
    def __init__(self, account_id, name):
        self.account_id = account_id
        self.name = name
        self.level = 1
        self.experience = 0
        self.health = 100
        self.max_health = 100
        self.mana = 100
        self.max_mana = 100
        self.strength = 10
        self.dexterity = 10
        self.intelligence = 10
        self.vitality = 10
        self.gold = 0
        self.inventory = []
        self.equipment = {slot: None for slot in ItemSlot}
        self.rings = [None, None]
        self.shadows = []
        self.player_class = None
        self.abilities = []
    
    @staticmethod
    def create_account(username, password):
        """Create a new account and return the account ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Hash the password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            cursor.execute(
                "INSERT INTO accounts (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            account_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return account_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    @staticmethod
    def verify_account(username, password):
        """Verify account credentials and return the account ID if valid."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Hash the password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute(
            "SELECT id FROM accounts WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        result = cursor.fetchone()
        
        if result:
            # Update last login time
            cursor.execute(
                "UPDATE accounts SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                (result[0],)
            )
            conn.commit()
            account_id = result[0]
            conn.close()
            return account_id
        
        conn.close()
        return None
    
    @staticmethod
    def load(account_id):
        """Load a player from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM players WHERE account_id = ?", (account_id,))
        player_data = cursor.fetchone()
        
        if player_data:
            # Convert row to dictionary
            columns = [description[0] for description in cursor.description]
            player_data = dict(zip(columns, player_data))
            
            player = Player(account_id, player_data['name'])
            player.level = player_data['level']
            player.experience = player_data['experience']
            player.health = player_data['health']
            player.max_health = player_data['max_health']
            player.mana = player_data['mana']
            player.max_mana = player_data['max_mana']
            player.strength = player_data['strength']
            player.dexterity = player_data['dexterity']
            player.intelligence = player_data['intelligence']
            player.vitality = player_data['vitality']
            player.gold = player_data['gold']
            
            # Load inventory
            try:
                player.inventory = json.loads(player_data['inventory'])
            except:
                player.inventory = []
            
            # Load equipment
            try:
                equipment_data = json.loads(player_data['equipment'])
                player.equipment = {ItemSlot(slot): item for slot, item in equipment_data.items()}
            except:
                player.equipment = {slot: None for slot in ItemSlot}
            
            # Load rings
            try:
                player.rings = json.loads(player_data['rings'])
            except:
                player.rings = [None, None]
            
            # Load shadows
            try:
                player.shadows = json.loads(player_data['shadows'])
            except:
                player.shadows = []
            
            # Load player class
            player.player_class = player_data['player_class']
            
            conn.close()
            return player
        
        conn.close()
        return None
    
    def save(self):
        """Save the player to the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if player exists
        cursor.execute("SELECT id FROM players WHERE account_id = ?", (self.account_id,))
        player_exists = cursor.fetchone()
        
        # Convert equipment dictionary to use string keys
        equipment_dict = {slot.value: item for slot, item in self.equipment.items()}
        
        if player_exists:
            # Update existing player
            cursor.execute("""
                UPDATE players SET
                    level = ?, experience = ?, health = ?, max_health = ?,
                    mana = ?, max_mana = ?, strength = ?, dexterity = ?,
                    intelligence = ?, vitality = ?, gold = ?, inventory = ?,
                    equipment = ?, rings = ?, shadows = ?, player_class = ?,
                    last_saved = CURRENT_TIMESTAMP
                WHERE account_id = ?
            """, (
                self.level, self.experience, self.health, self.max_health,
                self.mana, self.max_mana, self.strength, self.dexterity,
                self.intelligence, self.vitality, self.gold,
                json.dumps(self.inventory), json.dumps(equipment_dict),
                json.dumps(self.rings), json.dumps(self.shadows),
                self.player_class, self.account_id
            ))
        else:
            # Create new player
            cursor.execute("""
                INSERT INTO players (
                    account_id, name, level, experience, health, max_health,
                    mana, max_mana, strength, dexterity, intelligence,
                    vitality, gold, inventory, equipment, rings, shadows,
                    player_class, created_at, last_saved
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """, (
                self.account_id, self.name, self.level, self.experience,
                self.health, self.max_health, self.mana, self.max_mana,
                self.strength, self.dexterity, self.intelligence,
                self.vitality, self.gold, json.dumps(self.inventory),
                json.dumps(equipment_dict), json.dumps(self.rings),
                json.dumps(self.shadows), self.player_class
            ))
        
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """Get player stats as a dictionary."""
        stats = {
            "Level": self.level,
            "Experience": self.experience,
            "Health": f"{self.health}/{self.max_health}",
            "Mana": f"{self.mana}/{self.max_mana}",
            "Strength": self.strength,
            "Dexterity": self.dexterity,
            "Intelligence": self.intelligence,
            "Vitality": self.vitality,
            "Gold": self.gold
        }
        
        # Add class info if awakened
        if self.player_class:
            stats['Class'] = self.player_class.value
        
        return stats
    
    def gain_experience(self, amount):
        """Gain experience and level up if necessary."""
        self.experience += amount
        while self.experience >= self.get_next_level_exp():
            self.level_up()
    
    def get_next_level_exp(self):
        """Calculate experience needed for next level."""
        return self.level * 100
    
    def level_up(self):
        """Level up the player."""
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.max_mana += 10
        self.mana = self.max_mana
        self.strength += 2
        self.dexterity += 2
        self.intelligence += 2
        self.vitality += 2
    
    def heal(self, amount):
        """Heal the player."""
        self.health = min(self.health + amount, self.max_health)
    
    def restore_mana(self, amount):
        """Restore mana."""
        self.mana = min(self.mana + amount, self.max_mana)
    
    def add_shadow(self, shadow):
        if len(self.shadows) < 3:
            self.shadows.append(shadow)
            return True
        return False
    
    def remove_shadow(self, shadow_id):
        self.shadows = [s for s in self.shadows if s.id != shadow_id]
    
    def get_magical_power(self):
        """Calculate magical power based on intelligence."""
        return self.intelligence
    
    def get_spell_power_multiplier(self):
        """Calculate spell power multiplier based on magical power."""
        return 1.0 + (self.get_magical_power() / 100.0)  # 1% increase per point of magical power
    
    def awaken(self):
        if self.level < 10:
            return False, "You need to be level 10 to awaken!"
        
        if self.player_class:
            return False, "You are already awakened!"
        
        # Check if player has an awakening stone in inventory
        has_stone = any(item.name == "Awakening Stone" for item in self.inventory)
        if not has_stone:
            return False, "You need an Awakening Stone to awaken!"
        
        # Get random class
        self.player_class = get_random_class()
        class_def = CLASSES[self.player_class]
        
        # Apply class base stats
        self.strength += class_def.base_stats.strength
        self.dexterity += class_def.base_stats.dexterity
        self.intelligence += class_def.base_stats.intelligence
        self.vitality += class_def.base_stats.vitality
        
        # Add class abilities
        self.abilities = class_def.abilities
        
        # Remove awakening stone from inventory
        self.inventory = [item for item in self.inventory if item.name != "Awakening Stone"]
        
        return True, f"You have awakened as a {self.player_class.value}!"
    
    def equip_item(self, item):
        if item.level_req > self.level:
            return False, "You don't meet the level requirement!"
        
        if item.classes and self.player_class and self.player_class not in item.classes:
            return False, "This item is not suitable for your class!"
        
        if item.item_type == ItemType.WEAPON or item.item_type == ItemType.ARMOR:
            # Unequip current item in slot if any
            if self.equipment[item.slot]:
                self.unequip_item(self.equipment[item.slot])
            
            # Equip new item
            self.equipment[item.slot] = item
            self.apply_item_stats(item)
            return True, f"Equipped {item.name}"
        
        elif item.item_type == ItemType.ACCESSORY and item.slot == ItemSlot.RING:
            # Find first empty ring slot
            for i, ring in enumerate(self.rings):
                if ring is None:
                    self.rings[i] = item
                    self.apply_item_stats(item)
                    return True, f"Equipped {item.name} in ring slot {i+1}"
            return False, "No empty ring slots available!"
        
        return False, "Cannot equip this item!"
    
    def unequip_item(self, item):
        if item.item_type == ItemType.WEAPON or item.item_type == ItemType.ARMOR:
            if self.equipment[item.slot] == item:
                self.remove_item_stats(item)
                self.equipment[item.slot] = None
                self.inventory.append(item)
                return True, f"Unequipped {item.name}"
        
        elif item.item_type == ItemType.ACCESSORY and item.slot == ItemSlot.RING:
            for i, ring in enumerate(self.rings):
                if ring == item:
                    self.remove_item_stats(item)
                    self.rings[i] = None
                    self.inventory.append(item)
                    return True, f"Unequipped {item.name} from ring slot {i+1}"
        
        return False, "Item not equipped!"
    
    def apply_item_stats(self, item):
        for stat, value in item.stats.items():
            setattr(self, stat, getattr(self, stat) + value)
    
    def remove_item_stats(self, item):
        for stat, value in item.stats.items():
            setattr(self, stat, getattr(self, stat) - value)
    
    def get_equipped_items(self):
        equipped = []
        for slot, item in self.equipment.items():
            if item:
                equipped.append(f"{slot.value}: {item.name}")
        
        for i, ring in enumerate(self.rings):
            if ring:
                equipped.append(f"Ring {i+1}: {ring.name}")
        
        return equipped
    
    def get_inventory(self):
        return [str(item) for item in self.inventory]
    
    def use_item(self, item_name):
        """Use an item from inventory. Returns (success, message)."""
        # Find the item in inventory
        item = next((item for item in self.inventory if item.name == item_name), None)
        if not item:
            return False, "Item not found in inventory!"
        
        # Try to use the item
        success, message = item.use(self)
        if success:
            # Remove the item from inventory if it's a consumable
            if item.item_type == ItemType.CONSUMABLE:
                self.inventory.remove(item)
        return success, message 