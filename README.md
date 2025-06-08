# Solo Leveling RPG Game

A text-based RPG game inspired by the popular anime/manga "Solo Leveling". This game features:
- Character progression and leveling system
- Multiple stats (Strength, Defense, Agility, Intelligence)
- Shadow Summoning system (3 chances to tame defeated enemies)
- 2D map visualization
- Combat mechanics
- Equipment and inventory system
- MySQL database integration for saving progress

## Setup Instructions

1. Install Python 3.8 or higher
2. Install MySQL Server
3. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```
4. Create a MySQL database named 'solo_leveling_game'
5. Configure your database credentials in the .env file
6. Run the game:
   ```
   python main.py
   ```

## Game Features

- **Character System**: Create and customize your character with unique stats
- **Combat System**: Turn-based combat with various skills and abilities
- **Shadow Summoning**: Tame defeated enemies to fight alongside you
- **Map System**: 2D visualization of different zones and dungeons
- **Equipment System**: Various weapons and armor with different attributes
- **Quest System**: Complete quests to gain experience and rewards
- **Save System**: Progress is automatically saved to MySQL database

## Controls

- Arrow keys: Move character
- Space: Interact/Confirm
- I: Open inventory
- M: Open map
- C: Open character stats
- ESC: Pause menu 