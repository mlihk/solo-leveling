import random
from models.items import ItemRarity

class DungeonReward:
    def __init__(self):
        # Drop rates for different rarities based on difficulty tier
        self.drop_rates = {
            (0, 20): {  # Tier 1
                ItemRarity.COMMON: 1.0,
                ItemRarity.UNCOMMON: 0.0,
                ItemRarity.RARE: 0.0,
                ItemRarity.EPIC: 0.0,
                ItemRarity.LEGENDARY: 0.0,
                ItemRarity.MYTHIC: 0.0
            },
            (21, 40): {  # Tier 2
                ItemRarity.COMMON: 0.7,
                ItemRarity.UNCOMMON: 0.25,
                ItemRarity.RARE: 0.05,
                ItemRarity.EPIC: 0.0,
                ItemRarity.LEGENDARY: 0.0,
                ItemRarity.MYTHIC: 0.0
            },
            (41, 60): {  # Tier 3
                ItemRarity.COMMON: 0.6,
                ItemRarity.UNCOMMON: 0.25,
                ItemRarity.RARE: 0.1,
                ItemRarity.EPIC: 0.05,
                ItemRarity.LEGENDARY: 0.0,
                ItemRarity.MYTHIC: 0.0
            },
            (61, 80): {  # Tier 4
                ItemRarity.COMMON: 0.5,
                ItemRarity.UNCOMMON: 0.25,
                ItemRarity.RARE: 0.15,
                ItemRarity.EPIC: 0.08,
                ItemRarity.LEGENDARY: 0.02,
                ItemRarity.MYTHIC: 0.0
            },
            (81, 100): {  # Tier 5
                ItemRarity.COMMON: 0.4,
                ItemRarity.UNCOMMON: 0.25,
                ItemRarity.RARE: 0.2,
                ItemRarity.EPIC: 0.1,
                ItemRarity.LEGENDARY: 0.04,
                ItemRarity.MYTHIC: 0.01
            }
        }
        
        # Base rewards for each difficulty tier
        self.base_rewards = {
            (0, 20): {
                'gold': 100,
                'experience': 50
            },
            (21, 40): {
                'gold': 200,
                'experience': 100
            },
            (41, 60): {
                'gold': 400,
                'experience': 200
            },
            (61, 80): {
                'gold': 800,
                'experience': 400
            },
            (81, 100): {
                'gold': 1600,
                'experience': 800
            }
        }
    
    def get_tier(self, difficulty):
        """Get the current tier based on difficulty."""
        for (min_difficulty, max_difficulty) in self.drop_rates.keys():
            if min_difficulty <= difficulty <= max_difficulty:
                return (min_difficulty, max_difficulty)
        return (0, 20)  # Default tier
    
    def generate_rewards(self, difficulty):
        """Generate rewards based on difficulty."""
        tier = self.get_tier(difficulty)
        rewards = {
            'items': [],
            'gold': 0,
            'experience': 0
        }
        
        # Generate base rewards
        base = self.base_rewards[tier]
        difficulty_multiplier = 1 + (difficulty * 0.3)  # 30% increase per difficulty level
        rewards['gold'] = int(base['gold'] * difficulty_multiplier)
        rewards['experience'] = int(base['experience'] * difficulty_multiplier)
        
        # Generate items based on drop rates
        drop_rates = self.drop_rates[tier]
        for rarity, rate in drop_rates.items():
            if random.random() < rate:
                # Generate an item of this rarity
                item = self.generate_item(rarity, difficulty)
                if item:
                    rewards['items'].append(item)
        
        return rewards
    
    def generate_item(self, rarity, difficulty):
        """Generate an item of the specified rarity."""
        # This is a placeholder - you'll need to implement actual item generation
        # based on your item system
        return {
            'rarity': rarity,
            'level': difficulty,
            'name': f"{rarity.value} Item",
            'description': f"A {rarity.value.lower()} item from difficulty {difficulty}"
        }
    
    def get_drop_chance(self, rarity, difficulty):
        """Get the drop chance for a specific rarity at the current difficulty."""
        tier = self.get_tier(difficulty)
        return self.drop_rates[tier].get(rarity, 0.0) 