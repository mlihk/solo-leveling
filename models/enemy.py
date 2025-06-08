import random

class Enemy:
    def __init__(self, name, enemy_type, level=1):
        self.name = name
        self.type = enemy_type
        self.level = level
        
        # Core Stats
        self.strength = 10 + (level * 2)
        self.dexterity = 10 + (level * 2)
        self.intelligence = 10 + (level * 2)
        self.vitality = 10 + (level * 2)
        
        # Combat Stats
        self.health = 100 + (level * 10)
        self.max_health = self.health
        self.mana = 50 + (level * 5)
        self.max_mana = self.mana
        self.defense = 5 + (level * 1)
        self.agility = 10 + (level * 2)
        self.crit_chance = 5
        self.dodge_chance = 5
        
        # Rewards
        self.experience_reward = 50 + (level * 20)
        self.gold_reward = 20 + (level * 10)
        
        # Status Effects
        self.frozen = False
        self.blinded = False
        self.silenced = False
        self.confused = False
        self.feared = False
        self.marked = False
        self.doomed = False
        self.fire_immunity = False
        self.curse_immunity = False
    
    def take_damage(self, amount):
        """Take damage and return actual damage dealt."""
        # Apply defense reduction
        actual_damage = max(1, amount - (self.defense // 2))
        self.health = max(0, self.health - actual_damage)
        return actual_damage
    
    def heal(self, amount):
        """Heal the enemy."""
        self.health = min(self.max_health, self.health + amount)
    
    def is_alive(self):
        """Check if the enemy is alive."""
        return self.health > 0
    
    def get_stats(self):
        """Get enemy stats as a dictionary."""
        return {
            'name': self.name,
            'type': self.type,
            'level': self.level,
            'strength': self.strength,
            'dexterity': self.dexterity,
            'intelligence': self.intelligence,
            'vitality': self.vitality,
            'defense': self.defense,
            'agility': self.agility,
            'health': self.health,
            'max_health': self.max_health,
            'mana': self.mana,
            'max_mana': self.max_mana,
            'crit_chance': self.crit_chance,
            'dodge_chance': self.dodge_chance,
            'experience_reward': self.experience_reward,
            'gold_reward': self.gold_reward
        }

class EnemyFactory:
    @staticmethod
    def create_enemy(level):
        enemy_types = [
            ('Goblin', 'normal'),
            ('Orc', 'normal'),
            ('Skeleton', 'undead'),
            ('Wolf', 'beast'),
            ('Bandit', 'human'),
            ('Slime', 'elemental'),
            ('Spider', 'beast'),
            ('Zombie', 'undead'),
            ('Troll', 'normal'),
            ('Ghost', 'undead')
        ]
        
        name, enemy_type = random.choice(enemy_types)
        return Enemy(name, enemy_type, level)
    
    @staticmethod
    def create_boss(level):
        boss_types = [
            ('Dragon', 'dragon'),
            ('Lich', 'undead'),
            ('Giant', 'normal'),
            ('Demon', 'demon'),
            ('Ancient Golem', 'elemental')
        ]
        
        name, enemy_type = random.choice(boss_types)
        boss = Enemy(name, enemy_type, level)
        
        # Bosses are stronger than regular enemies
        boss.strength *= 1.5
        boss.defense *= 1.5
        boss.agility *= 1.5
        boss.health *= 2
        boss.max_health = boss.health
        boss.experience_reward *= 3
        boss.gold_reward *= 3
        
        return boss 