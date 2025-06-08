from config.database import get_db_connection
import random
import json

class Shadow:
    def __init__(self, name, shadow_type, level=1):
        self.id = None
        self.name = name
        self.shadow_type = shadow_type
        self.level = level
        self.strength = 10 + (level * 2)
        self.defense = 10 + (level * 2)
        self.agility = 10 + (level * 2)
        self.mana_cost = 50 + (level * 10)
        self.health = 100 + (level * 10)
        self.max_health = self.health
    
    def save(self, player_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            # New shadow
            cursor.execute("""
                INSERT INTO shadows (player_id, shadow_name, shadow_type, level, 
                                   strength, defense, agility, mana_cost)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                player_id, self.name, self.shadow_type, self.level,
                self.strength, self.defense, self.agility, self.mana_cost
            ))
            self.id = cursor.lastrowid
        else:
            # Update existing shadow
            cursor.execute("""
                UPDATE shadows SET
                    shadow_name = ?,
                    shadow_type = ?,
                    level = ?,
                    strength = ?,
                    defense = ?,
                    agility = ?,
                    mana_cost = ?
                WHERE id = ?
            """, (
                self.name, self.shadow_type, self.level,
                self.strength, self.defense, self.agility,
                self.mana_cost, self.id
            ))
        
        conn.commit()
        conn.close()
    
    @classmethod
    def load(cls, shadow_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM shadows WHERE id = ?", (shadow_id,))
        shadow_data = cursor.fetchone()
        
        if not shadow_data:
            conn.close()
            return None
        
        shadow = cls(
            shadow_data['shadow_name'],
            shadow_data['shadow_type'],
            shadow_data['level']
        )
        shadow.id = shadow_data['id']
        shadow.strength = shadow_data['strength']
        shadow.defense = shadow_data['defense']
        shadow.agility = shadow_data['agility']
        shadow.mana_cost = shadow_data['mana_cost']
        
        conn.close()
        return shadow
    
    def level_up(self):
        self.level += 1
        self.strength += 2
        self.defense += 2
        self.agility += 2
        self.mana_cost += 10
        self.max_health += 10
        self.health = self.max_health
    
    def take_damage(self, amount):
        actual_damage = max(1, amount - self.defense // 2)
        self.health = max(0, self.health - actual_damage)
        return actual_damage
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
    
    def get_stats(self):
        return {
            'name': self.name,
            'type': self.shadow_type,
            'level': self.level,
            'strength': self.strength,
            'defense': self.defense,
            'agility': self.agility,
            'mana_cost': self.mana_cost,
            'health': self.health,
            'max_health': self.max_health
        }
    
    def is_alive(self):
        return self.health > 0
    
    def __str__(self):
        return f"{self.name} (Level {self.level})" 