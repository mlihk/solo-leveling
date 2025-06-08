from models.enemy import EnemyFactory
import random

class Tower:
    def __init__(self):
        self.current_floor = 0
        self.max_floor = 100
        self.floor_rewards = {
            'gold': lambda floor: floor * 100,  # 100 gold per floor
            'experience': lambda floor: floor * 50,  # 50 exp per floor
        }
    
    def get_next_floor(self):
        """Get the next floor number."""
        return self.current_floor + 1
    
    def advance_floor(self):
        """Advance to the next floor."""
        if self.current_floor < self.max_floor:
            self.current_floor += 1
            return True
        return False
    
    def get_floor_rewards(self):
        """Get rewards for the current floor."""
        return {
            'gold': self.floor_rewards['gold'](self.current_floor),
            'experience': self.floor_rewards['experience'](self.current_floor)
        }
    
    def generate_floor_enemy(self, player_level):
        """Generate an enemy for the current floor."""
        # Base enemy level increases with floor number
        base_level = player_level + (self.current_floor // 10)
        
        # Add some randomness to the level
        level_variation = random.randint(-2, 2)
        enemy_level = max(1, base_level + level_variation)
        
        # Create a special tower enemy
        enemy = EnemyFactory.create_enemy(enemy_level)
        enemy.name = f"Floor {self.current_floor} Guardian"
        
        # Scale enemy stats based on floor
        scale_factor = 1 + (self.current_floor * 0.1)  # 10% increase per floor
        enemy.health = int(enemy.health * scale_factor)
        enemy.max_health = enemy.health
        enemy.strength = int(enemy.strength * scale_factor)
        enemy.defense = int(enemy.defense * scale_factor)
        enemy.agility = int(enemy.agility * scale_factor)
        
        # Increase rewards
        enemy.experience_reward = int(enemy.experience_reward * scale_factor)
        enemy.gold_reward = int(enemy.gold_reward * scale_factor)
        
        return enemy
    
    def get_floor_description(self):
        """Get a description of the current floor."""
        if self.current_floor == 0:
            return "You stand before the Tower of Trial. Are you ready to begin your ascent?"
        elif self.current_floor == self.max_floor:
            return "You have reached the final floor! Defeat the ultimate guardian to claim your victory!"
        else:
            return f"You are on floor {self.current_floor} of the Tower of Trial. The next challenge awaits..." 