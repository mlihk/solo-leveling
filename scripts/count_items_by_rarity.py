import sqlite3
import os

# Use the same database path as the game
DB_PATH = os.path.join('data', 'game.db')

def count_items_by_rarity():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT rarity, COUNT(*) FROM items GROUP BY rarity")
    results = cursor.fetchall()
    
    print("Items by rarity:")
    for rarity, count in results:
        print(f"{rarity}: {count}")
    
    conn.close()

if __name__ == '__main__':
    count_items_by_rarity() 