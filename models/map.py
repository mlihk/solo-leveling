import pygame
import random

class GameMap:
    # Reduced map size to fit in command window
    MAP_WIDTH = 20
    MAP_HEIGHT = 15
    
    # Tile types
    EMPTY = 0
    WALL = 1
    ENEMY = 2
    TREASURE = 3
    NPC = 4
    PORTAL = 5
    PLAYER = 6
    
    def __init__(self):
        self.map_data = [[self.EMPTY for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]
        self.player_pos = [self.MAP_HEIGHT // 2, self.MAP_WIDTH // 2]
        self.enemies = []
        self.treasures = []
        self.npcs = []
        self.portals = []
        
        # Colors for different tile types
        self.colors = {
            self.EMPTY: (100, 100, 100),    # Gray
            self.WALL: (50, 50, 50),        # Dark Gray
            self.ENEMY: (255, 0, 0),        # Red
            self.TREASURE: (255, 255, 0),   # Yellow
            self.NPC: (0, 255, 0),          # Green
            self.PORTAL: (0, 0, 255),       # Blue
            self.PLAYER: (255, 255, 255)    # White
        }
    
    def generate_map(self):
        # Clear the map
        self.map_data = [[self.EMPTY for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]
        
        # Add walls around the edges
        for x in range(self.MAP_WIDTH):
            self.map_data[0][x] = self.WALL
            self.map_data[self.MAP_HEIGHT-1][x] = self.WALL
        for y in range(self.MAP_HEIGHT):
            self.map_data[y][0] = self.WALL
            self.map_data[y][self.MAP_WIDTH-1] = self.WALL
        
        # Add random walls (reduced number)
        for _ in range(self.MAP_WIDTH * self.MAP_HEIGHT // 15):
            x = random.randint(1, self.MAP_WIDTH-2)
            y = random.randint(1, self.MAP_HEIGHT-2)
            self.map_data[y][x] = self.WALL
        
        # Add random enemies (reduced number)
        for _ in range(self.MAP_WIDTH * self.MAP_HEIGHT // 30):
            x = random.randint(1, self.MAP_WIDTH-2)
            y = random.randint(1, self.MAP_HEIGHT-2)
            if self.map_data[y][x] == self.EMPTY:
                self.map_data[y][x] = self.ENEMY
        
        # Add random treasures (reduced number)
        for _ in range(self.MAP_WIDTH * self.MAP_HEIGHT // 40):
            x = random.randint(1, self.MAP_WIDTH-2)
            y = random.randint(1, self.MAP_HEIGHT-2)
            if self.map_data[y][x] == self.EMPTY:
                self.map_data[y][x] = self.TREASURE
        
        # Add random NPCs (reduced number)
        for _ in range(self.MAP_WIDTH * self.MAP_HEIGHT // 50):
            x = random.randint(1, self.MAP_WIDTH-2)
            y = random.randint(1, self.MAP_HEIGHT-2)
            if self.map_data[y][x] == self.EMPTY:
                self.map_data[y][x] = self.NPC
        
        # Add random portals (reduced number)
        for _ in range(self.MAP_WIDTH * self.MAP_HEIGHT // 60):
            x = random.randint(1, self.MAP_WIDTH-2)
            y = random.randint(1, self.MAP_HEIGHT-2)
            if self.map_data[y][x] == self.EMPTY:
                self.map_data[y][x] = self.PORTAL
        
        # Place player in a random empty spot
        while True:
            x = random.randint(1, self.MAP_WIDTH-2)
            y = random.randint(1, self.MAP_HEIGHT-2)
            if self.map_data[y][x] == self.EMPTY:
                self.player_pos = [y, x]
                break
    
    def get_random_empty_position(self):
        while True:
            x = random.randint(0, self.MAP_WIDTH - 1)
            y = random.randint(0, self.MAP_HEIGHT - 1)
            if self.map_data[x][y] == self.EMPTY:
                return x, y
    
    def move_player(self, dx, dy):
        new_x = self.player_pos[1] + dx
        new_y = self.player_pos[0] + dy
        
        # Check if the new position is valid
        if 0 <= new_x < self.MAP_WIDTH and 0 <= new_y < self.MAP_HEIGHT:
            # Check if the new position is not a wall
            if self.map_data[new_y][new_x] != self.WALL:
                # Store the tile type before moving
                tile_type = self.map_data[new_y][new_x]
                
                # Move the player
                self.map_data[self.player_pos[0]][self.player_pos[1]] = self.EMPTY
                self.player_pos = [new_y, new_x]
                self.map_data[new_y][new_x] = self.EMPTY
                
                return tile_type
        
        return None
    
    def draw(self, screen):
        # Draw the map
        for i in range(self.MAP_WIDTH):
            for j in range(self.MAP_HEIGHT):
                color = self.colors[self.map_data[i][j]]
                pygame.draw.rect(screen, color,
                               (j * self.TILE_SIZE, i * self.TILE_SIZE,
                                self.TILE_SIZE, self.TILE_SIZE))
        
        # Draw player
        pygame.draw.rect(screen, self.colors[self.PLAYER],
                        (self.player_pos[1] * self.TILE_SIZE,
                         self.player_pos[0] * self.TILE_SIZE,
                         self.TILE_SIZE, self.TILE_SIZE))
    
    def get_tile_type(self, x, y):
        if 0 <= x < self.MAP_WIDTH and 0 <= y < self.MAP_HEIGHT:
            return self.map_data[x][y]
        return None
    
    def remove_enemy(self, x, y):
        if [x, y] in self.enemies:
            self.enemies.remove([x, y])
            self.map_data[x][y] = self.EMPTY
    
    def remove_treasure(self, x, y):
        if [x, y] in self.treasures:
            self.treasures.remove([x, y])
            self.map_data[x][y] = self.EMPTY
    
    def draw_text(self):
        # Create a copy of the map for display
        display_map = [row[:] for row in self.map_data]
        display_map[self.player_pos[0]][self.player_pos[1]] = self.PLAYER
        
        # Convert map to text representation
        symbols = {
            self.EMPTY: '·',  # Using a centered dot for empty space
            self.WALL: '█',   # Using a solid block for walls
            self.ENEMY: 'E',
            self.TREASURE: 'T',
            self.NPC: 'N',
            self.PORTAL: 'P',
            self.PLAYER: '@'
        }
        
        # Print the map with a border
        print('╔' + '═' * self.MAP_WIDTH + '╗')
        for row in display_map:
            print('║' + ''.join(symbols[tile] for tile in row) + '║')
        print('╚' + '═' * self.MAP_WIDTH + '╝')
        
        # Print compact legend
        print("Legend: @(You) ·(Empty) █(Wall) E(Enemy) T(Treasure) N(NPC) P(Portal)") 