import sys
import os
import ast
from models.player import Player
from models.location import LOCATIONS, GameTime
from models.enemy import EnemyFactory
from models.combat import Combat
from config.database import initialize_database
from models.items import ItemSlot
from models.classes import PlayerClass
from models.shop import Shop
from models.tower import Tower
from models.reward_manager import RewardManager
from models.dungeon import Dungeon
from models.dungeon_rewards import DungeonReward

class Game:
    def __init__(self):
        # Initialize database
        initialize_database()
        
        # Game state
        self.current_player = None
        self.current_location = None
        self.current_combat = None
        self.game_time = GameTime()
        self.game_state = 'login'  # login, playing, combat, menu, shop, tower, dungeon
        self.message_log = []
        self.max_messages = 20  # Increased to handle inventory display
        self.shop = Shop()
        self.tower = Tower()
        self.reward_manager = RewardManager()  # Add reward manager
        self.dungeon = Dungeon()  # Add dungeon instance
        self.dungeon_rewards = DungeonReward()  # Add dungeon rewards instance
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def add_message(self, message):
        # If the message is a list, add each message separately
        if isinstance(message, list):
            for msg in message:
                self.message_log.append(msg)
        else:
            # For regular messages, clear the log and add the new message
            if not message.startswith("=== Equipment ==="):
                self.message_log = []
            self.message_log.append(message)
        
        # Keep only the most recent message for regular commands
        if not any(msg.startswith("=== Equipment ===") for msg in self.message_log):
            if len(self.message_log) > 1:
                self.message_log = [self.message_log[-1]]
    
    def display_screen(self):
        self.clear_screen()
        
        if self.game_state == 'login':
            self.display_login_screen()
        elif self.game_state == 'playing':
            self.display_game_screen()
        elif self.game_state == 'combat':
            self.display_combat_screen()
        elif self.game_state == 'shop':
            self.display_shop_screen()
        elif self.game_state == 'tower':
            self.display_tower_screen()
        elif self.game_state == 'dungeon':
            self.display_dungeon_screen()
        elif self.game_state == 'guild':
            self.display_guild_screen()
    
    def display_login_screen(self):
        while True:
            self.clear_screen()
            print("=== Solo Leveling RPG ===")
            print("\n1. Login")
            print("2. Create Account")
            print("3. Exit")
            
            choice = input("\nEnter choice (1-3): ").strip()
            
            if choice == "3":
                sys.exit()
            elif choice == "1":
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                
                if not username or not password:
                    self.add_message("Username and password cannot be empty")
                    input("\nPress Enter to continue...")
                    continue
                
                # Verify account
                account_id = Player.verify_account(username, password)
                if account_id:
                    # Load player
                    player = Player.load(account_id)
                    if player:
                        self.current_player = player
                        self.game_state = 'playing'
                        self.current_location = LOCATIONS['home']
                        self.add_message(f"Welcome back, {player.name}!")
                        return
                    else:
                        # Create new player for existing account
                        self.current_player = Player(account_id, username)
                        self.current_player.save()
                        self.game_state = 'playing'
                        self.current_location = LOCATIONS['home']
                        self.add_message(f"Welcome, {username}! Your journey begins...")
                        return
                else:
                    self.add_message("Invalid username or password")
                    input("\nPress Enter to continue...")
                    continue
            elif choice == "2":
                username = input("Choose a username: ").strip()
                password = input("Choose a password: ").strip()
                
                if not username or not password:
                    self.add_message("Username and password cannot be empty")
                    input("\nPress Enter to continue...")
                    continue
                
                # Create new account
                account_id = Player.create_account(username, password)
                if account_id:
                    # Create new player
                    self.current_player = Player(account_id, username)
                    self.current_player.save()
                    self.game_state = 'playing'
                    self.current_location = LOCATIONS['home']
                    self.add_message(f"Welcome, {username}! Your journey begins...")
                    return
                else:
                    self.add_message("Username already exists")
                    input("\nPress Enter to continue...")
                    continue
            else:
                self.add_message("Invalid choice")
                input("\nPress Enter to continue...")
                continue
    
    def display_game_screen(self):
        # Display title and time
        print("=== Solo Leveling RPG ===")
        print(f"{self.game_time.get_day_string()} - {self.game_time.get_time_string()}")
        print(f"Remaining hours today: {self.game_time.get_remaining_hours()}")
        
        # Display current location
        print(f"\n=== Current Location: {self.current_location.name} ===")
        print(self.current_location.description)
        
        # Display player stats
        print("\n=== Character Stats ===")
        stats = self.current_player.get_stats()
        # Display stats in two columns
        stat_items = list(stats.items())
        for i in range(0, len(stat_items), 2):
            if i + 1 < len(stat_items):
                print(f"{stat_items[i][0]}: {stat_items[i][1]:<10} {stat_items[i+1][0]}: {stat_items[i+1][1]}")
            else:
                print(f"{stat_items[i][0]}: {stat_items[i][1]}")
        
        # Display messages
        if self.message_log:
            print("\n=== Latest Message ===")
            # If the first message is the inventory header, show all inventory messages
            if self.message_log[0].startswith("=== Equipment ==="):
                for message in self.message_log:
                    print(message)
            else:
                # Otherwise show only the last message
                print(self.message_log[-1])
        
        # Display available locations
        print("\n=== Available Locations ===")
        for key, location in LOCATIONS.items():
            print(f"- {location.name}")
        
        # Display command prompt
        print("\nEnter a command (type 'help' for available commands):")
        command = input("> ").lower().strip()
        self.process_command(command)
    
    def process_command(self, command):
        # Movement commands
        if command in ['home', 'h']:
            self.visit_location('home')
        elif command in ['supermarket', 's']:
            self.visit_location('supermarket')
        elif command in ['item store', 'i']:
            self.visit_location('item_store')
        elif command in ['park', 'p']:
            self.visit_location('park')
        elif command in ['dungeon', 'd']:
            self.visit_location('dungeon')
        elif command in ['guild', 'g']:
            self.visit_location('guild')
        elif command in ['tower', 't']:
            self.visit_location('tower_of_trial')
        # Other commands
        elif command in ['look', 'l']:
            self.show_location_description()
        elif command in ['inventory', 'inv']:
            self.show_inventory()
        elif command in ['shadows', 'shadow']:
            self.show_shadows()
        elif command in ['help', '?']:
            self.show_help()
        elif command in ['quit', 'q']:
            # Save before quitting
            if self.current_player:
                self.current_player.save()
            sys.exit()
        else:
            self.add_message(f"Unknown command: {command}")
        
        # Auto-save after any command
        if self.current_player:
            self.current_player.save()
    
    def visit_location(self, location_key):
        if self.game_time.get_remaining_hours() < 1:
            self.add_message("It's too late to go anywhere else today. You should rest.")
            return
        
        # Check if trying to travel to current location
        if self.current_location and location_key == self.current_location.name.lower().replace(" ", "_"):
            if location_key == 'item_store':
                self.game_state = 'shop'
                return
            elif location_key == 'tower_of_trial':
                self.game_state = 'tower'
                return
            elif location_key == 'guild':
                self.game_state = 'guild'
                return
            elif location_key == 'dungeon':
                self.game_state = 'dungeon'
                return
            else:
                self.add_message(f"You are already at {self.current_location.name}.")
                return
        
        location = LOCATIONS[location_key]
        self.current_location = location
        self.game_time.advance_time(1)  # Each movement takes 1 hour
        self.add_message(f"You travel to {location.name}.")
        
        # Force specific interfaces to open when visiting certain locations
        if location_key == 'item_store':
            self.game_state = 'shop'
            return
        elif location_key == 'tower_of_trial':
            self.game_state = 'tower'
            return
        elif location_key == 'guild':
            self.game_state = 'guild'
            return
        elif location_key == 'dungeon':
            self.game_state = 'dungeon'
            return
        
        # Trigger random event
        event = location.get_random_event(self.current_player.level)
        if event:
            self.add_message(f"\n{event.description}")
            self.handle_event(event)
    
    def handle_event(self, event):
        if event.event_type == 'combat':
            enemy = EnemyFactory.create_enemy(self.current_player.level)
            self.current_combat = Combat(self.current_player, enemy)
            self.game_state = 'combat'
        elif event.event_type == 'rest':
            self.current_player.heal(event.rewards.get('health', 0))
            self.current_player.restore_mana(event.rewards.get('mana', 0))
            self.add_message(f"Restored {event.rewards.get('health', 0)} health and {event.rewards.get('mana', 0)} mana.")
        elif event.event_type == 'training':
            self.current_player.gain_experience(event.rewards.get('experience', 0))
            if 'stats' in event.rewards:
                for stat, value in event.rewards['stats'].items():
                    setattr(self.current_player, stat, getattr(self.current_player, stat) + value)
            self.add_message(f"Gained {event.rewards.get('experience', 0)} experience from training.")
        elif event.event_type == 'shop':
            self.game_state = 'shop'
            self.display_shop_screen()
        elif event.event_type == 'quest':
            # TODO: Implement quest system
            self.add_message("Quest system coming soon!")
        elif event.event_type == 'portal':
            # TODO: Implement portal system
            self.add_message("Portal system coming soon!")
        elif event.event_type == 'treasure':
            self.current_player.gold += event.rewards.get('gold', 0)
            # TODO: Implement item rewards
            self.add_message(f"Found {event.rewards.get('gold', 0)} gold!")
    
    def show_help(self):
        # Clear any previous help messages from the log
        self.message_log = [msg for msg in self.message_log if not msg.startswith("Available Commands:")]
        
        help_text = """
Available Commands:
- Locations: home/h, supermarket/s, item store/i, park/p, dungeon/d, guild/g, tower/t
- Actions: look/l, inventory/inv, shadows/shadow
- System: help/?, quit/q

Each movement takes 1 hour of your day. Make sure to rest when needed!
        """
        self.add_message(help_text)
    
    def show_location_description(self):
        self.add_message(f"\n{self.current_location.name}: {self.current_location.description}")
    
    def show_inventory(self):
        """Display the inventory screen."""
        self.clear_screen()
        print("=== Inventory ===")
        print(f"Gold: {self.current_player.gold}")
        
        # Display latest message if any
        if self.message_log:
            print(f"\n=== Latest Message ===")
            print(self.message_log[-1])
        
        # Display equipped items
        print("\n=== Equipment ===")
        
        # Track equipped set items
        set_counts = {}  # set_name -> count
        set_items = {}   # set_name -> list of (slot, item)

        # Left side (Weapons and Armor)
        left_side = []
        left_side.append("\nWeapons:")
        main_hand = self.current_player.equipment[ItemSlot.MAIN_HAND]
        off_hand = self.current_player.equipment[ItemSlot.OFF_HAND]
        left_side.append(f"Main Hand: {main_hand.name if main_hand else 'None'}")
        left_side.append(f"Off Hand: {off_hand.name if off_hand else 'None'}")
        left_side.append("")  # Empty line for spacing

        left_side.append("Armor:                         Rings:")
        armor_slots = [
            ItemSlot.HEAD, ItemSlot.SHOULDER, ItemSlot.CHEST, ItemSlot.WRIST,
            ItemSlot.HANDS, ItemSlot.WAIST, ItemSlot.LEGS, ItemSlot.FEET
        ]
        for slot in armor_slots:
            item = self.current_player.equipment[slot]
            left_side.append(f"{slot.value.title()}: {item.name if item else 'None'}")
            # Track set items
            if item and hasattr(item, 'set_name') and item.set_name:
                set_counts.setdefault(item.set_name, 0)
                set_counts[item.set_name] += 1
                set_items.setdefault(item.set_name, []).append((slot, item))

        # Add empty lines for Ring 9 and 10
        left_side.append("")
        left_side.append("")

        # Right side (Rings)
        right_side = []
        right_side.append("")  # Empty line to align with Weapons
        right_side.append("")  # Empty line to align with Main Hand
        right_side.append("")  # Empty line to align with Off Hand
        right_side.append("")  # Empty line for spacing
        right_side.append("")  # Empty line for Rings header (now part of Armor line)
        # Show all 10 ring slots
        for i in range(10):
            ring = self.current_player.rings[i] if i < len(self.current_player.rings) else None
            right_side.append(f"Ring {i+1:2d}: {ring.name if ring else 'None'}")  # Use 2d for consistent spacing
            if ring and hasattr(ring, 'set_name') and ring.set_name:
                set_counts.setdefault(ring.set_name, 0)
                set_counts[ring.set_name] += 1
                set_items.setdefault(ring.set_name, []).append((f"Ring {i+1}", ring))

        # Combine left and right sides
        max_lines = max(len(left_side), len(right_side))
        for i in range(max_lines):
            left = left_side[i] if i < len(left_side) else ""
            right = right_side[i] if i < len(right_side) else ""
            if left and right:
                print(f"{left:<30} {right}")
            else:
                print(left or right)

        # Display set bonuses for each set
        if set_counts:
            print("\n=== Set Bonuses ===")
            for set_name, count in set_counts.items():
                # Get set_bonus from the first item in the set
                _, example_item = set_items[set_name][0]
                set_bonus = getattr(example_item, 'set_bonus', None)
                if isinstance(set_bonus, str):
                    try:
                        set_bonus = ast.literal_eval(set_bonus)
                    except Exception:
                        set_bonus = None
                print(f"{set_name} ({count}/{len(set_bonus) if set_bonus else '?'}) equipped:")
                if set_bonus:
                    for key in sorted(set_bonus.keys()):
                        desc = set_bonus[key]['description']
                        num_required = int(key.split('_')[0])
                        active = count >= num_required
                        status = '[ACTIVE]' if active else '[      ]'
                        print(f"  {status} {key.replace('_', ' ')}: {desc}")

        # Display inventory items
        print("\n=== Inventory Items ===")
        if self.current_player.inventory:
            for i, item in enumerate(self.current_player.inventory, 1):
                print(f"{i}. {item.name} ({item.rarity})")
                print(f"   Type: {item.type}")
                print(f"   Slot: {item.slot}")
                print(f"   Level Req: {item.level_req}")
                print(f"   Stats: {item.stats}")
                if item.get('effect'):
                    print(f"   Effect: {item['effect']}")
                if item.get('special_bonus'):
                    print(f"   Special Bonus: {item['special_bonus']}")
                if item.get('set_name'):
                    print(f"   Set: {item['set_name']}")
                print()
        else:
            print("Empty")

        print("\nCommands:")
        print("equip <number> - Equip an item from your inventory")
        print("unequip <slot> - Unequip an item (e.g., 'unequip main_hand')")
        print("back - Return to game")
        
        while True:
            command = input("\nEnter command: ").strip().lower()
            
            if command == "back":
                break
            elif command.startswith("equip "):
                try:
                    item_num = int(command.split()[1])
                    if 1 <= item_num <= len(self.current_player.inventory):
                        item = self.current_player.inventory[item_num - 1]
                        # Check if slot is occupied
                        if item.slot == ItemSlot.RING:
                            # For rings, find the first empty slot or use the last slot
                            empty_slot = None
                            for i in range(10):
                                if i >= len(self.current_player.rings) or self.current_player.rings[i] is None:
                                    empty_slot = i
                                    break
                            if empty_slot is None:
                                empty_slot = len(self.current_player.rings)
                            if empty_slot < 10:
                                success, message = self.current_player.equip_item(item, empty_slot)
                            else:
                                self.add_message("You can only equip up to 10 rings!")
                                continue
                        else:
                            # For other items, automatically unequip if slot is occupied
                            if item.slot in self.current_player.equipment and self.current_player.equipment[item.slot]:
                                old_item = self.current_player.equipment[item.slot]
                                self.current_player.unequip_item(item.slot)
                                self.add_message(f"Unequipped {old_item.name}")
                            success, message = self.current_player.equip_item(item)
                        
                        self.add_message(message)
                        if success:
                            self.current_player.save()
                            self.show_inventory()  # Refresh the display
                    else:
                        self.add_message("Invalid item number")
                except (ValueError, IndexError):
                    self.add_message("Invalid command format")
            elif command.startswith("unequip "):
                try:
                    slot_name = command.split()[1].upper()
                    if slot_name in [slot.name for slot in ItemSlot]:
                        slot = ItemSlot[slot_name]
                        success, message = self.current_player.unequip_item(slot)
                        self.add_message(message)
                        if success:
                            self.current_player.save()
                            self.show_inventory()  # Refresh the display
                    else:
                        self.add_message("Invalid slot name")
                except (ValueError, IndexError):
                    self.add_message("Invalid command format")
            else:
                self.add_message("Invalid command")
            
            # Clear screen and redisplay after each command
            self.clear_screen()
            self.show_inventory()
    
    def show_shadows(self):
        if not self.current_player.shadows:
            self.add_message("You have no shadows yet.")
        else:
            self.add_message("=== Your Shadows ===")
            for shadow in self.current_player.shadows:
                self.add_message(f"- {shadow.name} (Level {shadow.level})")
    
    def display_combat_screen(self):
        """Display the combat screen."""
        self.clear_screen()
        print("=== Combat ===")
        
        # Display combat status
        print(f"\n{self.current_combat.player.name} (HP: {self.current_combat.player.health}/{self.current_combat.player.max_health})")
        print(f"vs")
        print(f"{self.current_combat.enemy.name} (HP: {self.current_combat.enemy.health}/{self.current_combat.enemy.max_health})")
        
        # Display combat log
        if self.combat_log:
            print("\n=== Combat Log ===")
            for message in self.combat_log[-5:]:  # Show last 5 messages
                print(message)
        
        print("\nCommands:")
        print("attack - Attack the enemy")
        print("skill - Use a skill")
        print("item - Use an item")
        print("flee - Try to flee (not available in dungeons)")
        
        command = input("\nEnter command: ").strip().lower()
        
        if command == "attack":
            result = self.current_combat.player_attack()
            self.combat_log.append(result)
            
            if not self.current_combat.is_enemy_defeated():
                result = self.current_combat.enemy_attack()
                self.combat_log.append(result)
            
            if self.current_combat.is_player_defeated():
                self.add_message("You have been defeated!")
                if self.game_state == 'dungeon':
                    # In dungeon, reset the run on defeat
                    self.dungeon.reset_difficulty()
                    self.game_state = 'dungeon'
                else:
                    self.game_state = 'playing'
                return
            elif self.current_combat.is_enemy_defeated():
                self.add_message(f"You defeated {self.current_combat.enemy.name}!")
                if self.game_state == 'dungeon':
                    # In dungeon, advance to next room
                    self.dungeon.advance_encounter(self.current_player.level)
                    self.game_state = 'dungeon'
                else:
                    self.game_state = 'playing'
                return
        elif command == "skill":
            # TODO: Implement skill system
            self.add_message("Skills not implemented yet!")
        elif command == "item":
            # TODO: Implement item system
            self.add_message("Items not implemented yet!")
        elif command == "flee":
            if self.game_state == 'dungeon':
                self.add_message("You cannot flee in a dungeon!")
            else:
                if self.current_combat.try_flee():
                    self.add_message("You successfully fled!")
                    self.game_state = 'playing'
                else:
                    self.add_message("Failed to flee!")
                    result = self.current_combat.enemy_attack()
                    self.combat_log.append(result)
        else:
            self.add_message("Invalid command")
    
    def display_shop_screen(self):
        """Display the shop screen with available items."""
        self.clear_screen()
        print("=== Item Store ===")
        print(f"Gold: {self.current_player.gold}")
        
        # Display latest message if any
        if self.message_log:
            print(f"\n=== Latest Message ===")
            print(self.message_log[-1])
        
        # Get time until next refresh
        time_until_refresh = self.shop.get_time_until_refresh()
        days = time_until_refresh.days
        hours = time_until_refresh.seconds // 3600
        minutes = (time_until_refresh.seconds % 3600) // 60
        
        if days > 0:
            print(f"\nNext shop refresh in: {days} days, {hours} hours")
        else:
            print(f"\nNext shop refresh in: {hours} hours, {minutes} minutes")
        
        print("\nAvailable Items:")
        items = self.shop.get_items()
        if not items:
            print("No items available at the moment.")
        else:
            for i, item in enumerate(items, 1):
                print(f"\n{i}. {item['name']} ({item['rarity']})")
                print(f"   Type: {item['type']}")
                print(f"   Slot: {item['slot']}")
                print(f"   Level Req: {item['level_req']}")
                print(f"   Stats: {item['stats']}")
                if item.get('effect'):
                    print(f"   Effect: {item['effect']}")
                if item.get('special_bonus'):
                    print(f"   Special Bonus: {item['special_bonus']}")
                if item.get('set_name'):
                    print(f"   Set: {item['set_name']}")
                print(f"   Price: {item['price']} gold")
        
        print("\nCommands:")
        print("buy <number> - Buy an item")
        print("refresh - Refresh shop inventory (1000 gold)")
        print("back - Return to game")
        
        command = input("\nEnter command: ").strip().lower()
        
        if command == "back":
            self.game_state = 'playing'
            return
        elif command.startswith("buy "):
            try:
                item_num = int(command.split()[1])
                if 1 <= item_num <= len(items):
                    success, message = self.shop.buy_item(items[item_num - 1]['id'], self.current_player)
                    self.add_message(message)
                    if success:
                        self.display_shop_screen()
                else:
                    self.add_message("Invalid item number")
            except (ValueError, IndexError):
                self.add_message("Invalid command format")
        elif command == "refresh":
            if self.current_player.gold >= 1000:
                self.current_player.gold -= 1000
                self.shop.refresh_shop()
                self.add_message("Shop refreshed!")
                self.display_shop_screen()
            else:
                self.add_message("Not enough gold to refresh shop")
        else:
            self.add_message("Invalid command")
    
    def display_tower_screen(self):
        """Display the tower screen."""
        self.clear_screen()
        print("=== Tower of Trial ===")
        print(f"Current Floor: {self.tower.current_floor}")
        print(f"Max Floor: {self.tower.max_floor}")
        print(f"\n{self.tower.get_floor_description()}")
        
        # Display player stats
        print("\n=== Character Stats ===")
        stats = self.current_player.get_stats()
        # Display stats in two columns
        stat_items = list(stats.items())
        for i in range(0, len(stat_items), 2):
            if i + 1 < len(stat_items):
                print(f"{stat_items[i][0]}: {stat_items[i][1]:<10} {stat_items[i+1][0]}: {stat_items[i+1][1]}")
            else:
                print(f"{stat_items[i][0]}: {stat_items[i][1]}")
        
        # Display messages
        if self.message_log:
            print("\n=== Latest Message ===")
            print(self.message_log[-1])
        
        print("\nCommands:")
        print("challenge - Challenge the current floor")
        print("leave - Leave the tower")
        
        command = input("\nEnter command: ").strip().lower()
        
        if command == "leave":
            self.game_state = 'playing'
            return
        elif command == "challenge":
            if self.tower.current_floor == 0:
                self.tower.advance_floor()
            
            enemy = self.tower.generate_floor_enemy(self.current_player.level)
            self.current_combat = Combat(self.current_player, enemy)
            self.game_state = 'combat'
            return
        else:
            self.add_message("Invalid command")
    
    def display_guild_screen(self):
        """Display the guild screen."""
        self.clear_screen()
        print("=== Guild Hall ===")
        print(f"Gold: {self.current_player.gold}")
        
        # Display latest message if any
        if self.message_log:
            print(f"\n=== Latest Message ===")
            print(self.message_log[-1])
        
        print("\nAvailable Services:")
        print("1. Guild Master")
        print("   - Take on quests")
        print("   - Learn about the guild")
        print("   - Get training")
        print("\n2. Reward Manager")
        print("   - Redeem special codes")
        print("   - Claim rewards")
        print("\n3. Return to Town")
        
        choice = input("\nWhat would you like to do? ")
        
        if choice == '1':
            self.display_guild_master_dialogue()
        elif choice == '2':
            self.display_reward_manager_screen()
        elif choice == '3':
            self.game_state = 'playing'
        else:
            self.add_message("Invalid choice!")
    
    def display_reward_manager_screen(self):
        """Display the reward manager screen."""
        self.clear_screen()
        print("=== Reward Manager ===")
        print(f"Gold: {self.current_player.gold}")
        
        # Display latest message if any
        if self.message_log:
            print(f"\n=== Latest Message ===")
            print(self.message_log[-1])
        
        dialogue = self.reward_manager.get_dialogue()
        print(f"\n{dialogue['greeting']}")
        print(dialogue['help'])
        
        while True:
            print("\nCommands:")
            print("redeem <code> - Redeem a code")
            print("back - Return to Guild Hall")
            
            command = input("\nEnter command: ").strip().lower()
            
            if command == "back":
                break
            elif command.startswith("redeem "):
                code = command.split(" ", 1)[1]
                success, message = self.reward_manager.redeem_code(self.current_player, code)
                self.add_message(message)
                
                if success:
                    self.add_message(dialogue['success'])
                    self.current_player.save()  # Save after successful redemption
                
                # Clear screen and redisplay the interface
                self.clear_screen()
                print("=== Reward Manager ===")
                print(f"Gold: {self.current_player.gold}")
                
                # Display latest message
                if self.message_log:
                    print(f"\n=== Latest Message ===")
                    print(self.message_log[-1])
                
                print(f"\n{dialogue['greeting']}")
                print(dialogue['help'])
            else:
                self.add_message("Invalid command!")
                # Clear screen and redisplay the interface
                self.clear_screen()
                print("=== Reward Manager ===")
                print(f"Gold: {self.current_player.gold}")
                
                # Display latest message
                if self.message_log:
                    print(f"\n=== Latest Message ===")
                    print(self.message_log[-1])
                
                print(f"\n{dialogue['greeting']}")
                print(dialogue['help'])
    
    def display_dungeon_screen(self):
        """Display the dungeon screen."""
        self.clear_screen()
        print("=== Dungeon System ===")
        print(f"Current Dungeon: {self.dungeon.get_dungeon_name()}")
        print(f"Difficulty Level: {self.dungeon.current_difficulty}")
        
        # Only show room information if a run has started
        if self.dungeon.encounters_completed > 0:
            print(f"Rooms Completed: {self.dungeon.encounters_completed}/{self.dungeon.total_encounters}")
            print(f"\n{self.dungeon.get_story_progress()}")
            
            # Display current room description if in a room
            if self.dungeon.current_room_type:
                print(f"\n=== Current Room ===")
                print(self.dungeon.get_room_description())
                
                # Display puzzle if in a puzzle room
                if self.dungeon.current_room_type == 'puzzle':
                    puzzle = self.dungeon.get_current_puzzle()
                    if puzzle:
                        print(f"\n=== Puzzle ===")
                        print(puzzle.question)
                        print(f"\nAttempts remaining: {puzzle.get_remaining_attempts()}")
        else:
            print("\nA dangerous place filled with monsters. The deeper you go, the stronger they become.")
            print("Complete all rooms to claim rewards and increase difficulty.")
        
        # Display player stats
        print("\n=== Character Stats ===")
        stats = self.current_player.get_stats()
        # Display stats in two columns
        stat_items = list(stats.items())
        for i in range(0, len(stat_items), 2):
            if i + 1 < len(stat_items):
                print(f"{stat_items[i][0]}: {stat_items[i][1]:<10} {stat_items[i+1][0]}: {stat_items[i+1][1]}")
            else:
                print(f"{stat_items[i][0]}: {stat_items[i][1]}")
        
        # Display messages
        if self.message_log:
            print("\n=== Latest Message ===")
            print(self.message_log[-1])
        
        print("\nCommands:")
        if self.dungeon.encounters_completed == 0:
            print("start - Start a new dungeon run")
            print("leave - Leave the dungeon")
        elif self.dungeon.encounters_completed < self.dungeon.total_encounters:
            if self.dungeon.current_room_type == 'combat':
                print("fight - Engage in combat")
            elif self.dungeon.current_room_type == 'puzzle':
                print("answer <text> - Submit your answer to the puzzle")
                print("hint - Get a hint for the puzzle")
            elif self.dungeon.current_room_type == 'trap':
                print("disarm - Try to disarm the trap")
            elif self.dungeon.current_room_type == 'treasure':
                print("loot - Collect the treasure")
            print("skip - Skip this room (with penalty)")
            print("surrender - Give up and return to town (with penalty)")
        else:
            print("claim - Claim rewards and increase difficulty")
            print("reset - Reset difficulty and start over")
            print("leave - Leave the dungeon")
        
        command = input("\nEnter command: ").strip().lower()
        
        if command == "leave":
            if self.dungeon.encounters_completed == 0 or self.dungeon.encounters_completed >= self.dungeon.total_encounters:
                self.game_state = 'playing'
                return
            else:
                self.add_message("You cannot leave during an active dungeon run! Use 'surrender' to give up.")
                return
        elif command == "surrender" and 0 < self.dungeon.encounters_completed < self.dungeon.total_encounters:
            # Apply surrender penalty
            self.current_player.take_damage(20)  # Take significant damage
            self.current_player.gold = max(0, self.current_player.gold - 100)  # Lose some gold
            self.add_message("You surrender and flee the dungeon, taking heavy penalties!")
            self.dungeon.reset_difficulty()  # Reset the dungeon
            self.game_state = 'playing'
            return
        elif command == "start" and self.dungeon.encounters_completed == 0:
            # Start new run and generate first room
            self.dungeon.start_new_run()
            self.dungeon.advance_encounter(self.current_player.level)
            self.add_message("Starting new dungeon run...")
            return
        elif command == "fight" and self.dungeon.current_room_type == 'combat':
            enemy = self.dungeon.generate_enemy(self.current_player.level)
            if enemy:
                self.current_combat = Combat(self.current_player, enemy)
                self.game_state = 'combat'
            return
        elif command.startswith("answer ") and self.dungeon.current_room_type == 'puzzle':
            answer = command[7:].strip()  # Remove "answer " from the command
            puzzle = self.dungeon.get_current_puzzle()
            if puzzle:
                if puzzle.check_answer(answer):
                    self.add_message("Correct! The puzzle is solved!")
                    puzzle.solved = True
                    self.dungeon.advance_encounter(self.current_player.level)
                else:
                    self.add_message("Incorrect answer!")
                    if puzzle.get_remaining_attempts() <= 0:
                        self.add_message("You've run out of attempts! Taking damage...")
                        self.current_player.take_damage(15)  # Take damage for failing
                        self.dungeon.advance_encounter(self.current_player.level)
            return
        elif command == "hint" and self.dungeon.current_room_type == 'puzzle':
            puzzle = self.dungeon.get_current_puzzle()
            if puzzle:
                self.add_message(puzzle.get_hint())
            return
        elif command == "disarm" and self.dungeon.current_room_type == 'trap':
            # TODO: Implement trap disarming
            self.add_message("You successfully disarm the trap!")
            self.dungeon.advance_encounter(self.current_player.level)
            return
        elif command == "loot" and self.dungeon.current_room_type == 'treasure':
            # TODO: Implement treasure collection
            self.add_message("You collect valuable treasures!")
            self.dungeon.advance_encounter(self.current_player.level)
            return
        elif command == "skip" and self.dungeon.encounters_completed < self.dungeon.total_encounters:
            # Apply penalty for skipping
            self.current_player.take_damage(10)  # Take some damage
            self.add_message("You take damage while trying to skip the room!")
            self.dungeon.advance_encounter(self.current_player.level)
            return
        elif command == "claim" and self.dungeon.encounters_completed >= self.dungeon.total_encounters:
            if not self.dungeon.rewards_claimed:
                rewards = self.dungeon_rewards.generate_rewards(self.dungeon.current_difficulty)
                self.current_player.gold += rewards['gold']
                self.current_player.gain_experience(rewards['experience'])
                
                # Add items to player's inventory
                for item in rewards['items']:
                    # TODO: Implement adding items to inventory
                    self.add_message(f"Received {item['name']}!")
                
                self.add_message(f"Claimed rewards: {rewards['gold']} gold, {rewards['experience']} experience!")
                self.dungeon.rewards_claimed = True
                
                if self.dungeon.increase_difficulty():
                    self.add_message(f"Increased difficulty to {self.dungeon.current_difficulty}!")
                else:
                    self.add_message("You've reached the maximum difficulty!")
            else:
                self.add_message("You've already claimed the rewards for this difficulty!")
            return
        elif command == "reset":
            self.dungeon.reset_difficulty()
            self.add_message("Dungeon difficulty has been reset!")
            return
        else:
            self.add_message("Invalid command")
    
    def display_playing_screen(self):
        """Display the main playing screen."""
        self.clear_screen()
        print("=== Solo Leveling RPG ===")
        print(f"{self.game_time.get_day_string()} - {self.game_time.get_time_string()}")
        print(f"Remaining hours today: {self.game_time.get_remaining_hours()}")
        
        # Display current location
        print(f"\n=== Current Location: {self.current_location.name} ===")
        print(self.current_location.description)
        
        # Display player stats
        print("\n=== Character Stats ===")
        stats = self.current_player.get_stats()
        # Display stats in two columns
        stat_items = list(stats.items())
        for i in range(0, len(stat_items), 2):
            if i + 1 < len(stat_items):
                print(f"{stat_items[i][0]}: {stat_items[i][1]:<10} {stat_items[i+1][0]}: {stat_items[i+1][1]}")
            else:
                print(f"{stat_items[i][0]}: {stat_items[i][1]}")
        
        # Display messages
        if self.message_log:
            print("\n=== Latest Message ===")
            print(self.message_log[-1])
        
        # Display available locations
        print("\n=== Available Locations ===")
        for key, location in LOCATIONS.items():
            print(f"- {location.name}")
        
        # Display command prompt
        print("\nEnter a command (type 'help' for available commands):")
        command = input("> ").lower().strip()
        self.process_command(command)
    
    def run(self):
        while True:
            try:
                if self.game_state == 'login':
                    self.display_login_screen()
                elif self.game_state == 'playing':
                    self.display_playing_screen()
                elif self.game_state == 'combat':
                    self.display_combat_screen()
                elif self.game_state == 'menu':
                    self.display_menu_screen()
                elif self.game_state == 'shop':
                    self.display_shop_screen()
                elif self.game_state == 'tower':
                    self.display_tower_screen()
                elif self.game_state == 'dungeon':
                    self.display_dungeon_screen()
                elif self.game_state == 'guild':
                    self.display_guild_screen()
                else:
                    print("Invalid game state!")
                    break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

if __name__ == "__main__":
    game = Game()
    game.run() 