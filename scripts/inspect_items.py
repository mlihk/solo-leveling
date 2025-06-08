import sqlite3
import os

DB_PATH = os.path.join('data', 'game.db')

def inspect_items():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, rarity FROM items LIMIT 10")
    results = cursor.fetchall()
    print("First 10 items:")
    for row in results:
        print(f"ID: {row[0]}, Name: {row[1]}, Rarity: {row[2]}")
    conn.close()

if __name__ == '__main__':
    inspect_items() 