import random

class Enemy:
    def __init__(self, name, enemy_type, level=1):
        self.name = name
        self.type = enemy_type
        self.level = level
        self.strength = 10 + (level * 2)
        self.defense = 10 + (level * 2)
        self.agility = 10 + (level * 2)
        self.health = 100 + (level * 10)
        self.max_health = self.health
        self.experience_reward = 50 + (level * 20)
        self.gold_reward = 20 + (level * 10)
    
    def take_damage(self, amount):
        actual_damage = max(1, amount - self.defense // 2)
        self.health = max(0, self.health - actual_damage)
        return actual_damage
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
    
    def is_alive(self):
        return self.health > 0
    
    def get_stats(self):
        return {
            'name': self.name,
            'type': self.type,
            'level': self.level,
            'strength': self.strength,
            'defense': self.defense,
            'agility': self.agility,
            'health': self.health,
            'max_health': self.max_health,
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