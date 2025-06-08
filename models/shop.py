import random
import sqlite3
from datetime import datetime, timedelta
from config.database import get_db_connection

class Shop:
    def __init__(self):
        self.items = []
        self.last_refresh = None
        self.refresh_shop()
    
    def get_base_price(self, rarity):
        base_prices = {
            'Common': 1000,
            'Uncommon': 10000,
            'Rare': 100000,
            'Epic': 1000000,
            'Legendary': 10000000,
            'Mythic': 100000000
        }
        return base_prices.get(rarity, 1000)
    
    def get_rarity_chance(self, rarity):
        chances = {
            'Common': 0.6,      # 60% chance
            'Uncommon': 0.3,    # 30% chance
            'Rare': 0.0899,     # 8.99% chance
            'Epic': 0.01,       # 1% chance
            'Legendary': 0.001, # 0.1% chance
            'Mythic': 0.0001    # 0.01% chance
        }
        return chances.get(rarity, 0)
    
    def generate_price(self, base_price):
        # Generate a price within ±20% of the base price
        variation = random.uniform(0.8, 1.2)
        price = int(base_price * variation)
        # Round to nearest 100 for cleaner numbers
        return round(price / 100) * 100
    
    def should_refresh(self):
        # If no last refresh time, we need to refresh
        if self.last_refresh is None:
            return True
        
        # Check if 7 in-game days have passed
        # Assuming 1 in-game day = 24 hours
        seven_days = timedelta(days=7)
        return datetime.now() - self.last_refresh >= seven_days
    
    def get_time_until_refresh(self):
        if self.last_refresh is None:
            return timedelta(0)
        
        seven_days = timedelta(days=7)
        time_passed = datetime.now() - self.last_refresh
        time_remaining = seven_days - time_passed
        
        # If time has passed, return 0
        if time_remaining.total_seconds() <= 0:
            return timedelta(0)
        
        return time_remaining
    
    def refresh_shop(self):
        if not self.should_refresh():
            return
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Clear current items
        self.items = []
        
        # Generate 6 random items
        for _ in range(6):
            # Determine rarity based on chances
            rarity_roll = random.random()
            cumulative_chance = 0
            selected_rarity = 'Common'  # Default
            
            # Get rarity chances and iterate through them
            rarity_chances = {
                'Common': 0.6,      # 60% chance
                'Uncommon': 0.3,    # 30% chance
                'Rare': 0.0899,     # 8.99% chance
                'Epic': 0.01,       # 1% chance
                'Legendary': 0.001, # 0.1% chance
                'Mythic': 0.0001    # 0.01% chance
            }
            
            for rarity, chance in rarity_chances.items():
                cumulative_chance += chance
                if rarity_roll <= cumulative_chance:
                    selected_rarity = rarity
                    break
            
            # Get base price for the rarity
            base_price = self.get_base_price(selected_rarity)
            price = self.generate_price(base_price)
            
            # Get random item of selected rarity
            cursor.execute("SELECT * FROM items WHERE rarity = ? ORDER BY RANDOM() LIMIT 1", (selected_rarity,))
            item = cursor.fetchone()
            
            if item:
                # Add price to item data
                item_dict = dict(item)
                item_dict['price'] = price
                self.items.append(item_dict)
        
        conn.close()
        self.last_refresh = datetime.now()
    
    def get_items(self):
        if self.should_refresh():
            self.refresh_shop()
        return self.items
    
    def buy_item(self, item_id, player):
        # Find the item in the shop
        item = next((item for item in self.items if item['id'] == item_id), None)
        if not item:
            return False, "Item not found in shop"
        
        # Check if player has enough gold
        if player.gold < item['price']:
            return False, "Not enough gold"
        
        # Add item to player's inventory and deduct gold
        player.gold -= item['price']
        player.inventory.append(item)
        
        # Remove item from shop
        self.items.remove(item)
        
        return True, f"Successfully purchased {item['name']} for {item['price']} gold"