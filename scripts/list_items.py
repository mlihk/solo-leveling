import sqlite3

def list_items():
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, slot, rarity, level_req, stats, effect FROM items")
    items = cursor.fetchall()
    for item in items:
        print(f"ID: {item[0]}")
        print(f"Name: {item[1]}")
        print(f"Type: {item[2]}")
        print(f"Slot: {item[3]}")
        print(f"Rarity: {item[4]}")
        print(f"Level Req: {item[5]}")
        print(f"Stats: {item[6]}")
        print(f"Effect: {item[7]}")
        print("-" * 40)
    conn.close()

if __name__ == "__main__":
    list_items() 