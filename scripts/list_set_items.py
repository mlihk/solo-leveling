import sqlite3

conn = sqlite3.connect('game.db')
cursor = conn.cursor()

cursor.execute("SELECT id, name, type, slot, rarity, level_req, stats, effect, special_bonus, set_name, set_bonus FROM items WHERE set_name IS NOT NULL")
items = cursor.fetchall()

if not items:
    print("No set items found.")
else:
    for item in items:
        print(f"ID: {item[0]}")
        print(f"Name: {item[1]}")
        print(f"Type: {item[2]}")
        print(f"Slot: {item[3]}")
        print(f"Rarity: {item[4]}")
        print(f"Level Req: {item[5]}")
        print(f"Stats: {item[6]}")
        print(f"Effect: {item[7]}")
        print(f"Special Bonus: {item[8]}")
        print(f"Set Name: {item[9]}")
        print(f"Set Bonus: {item[10]}")
        print("-"*40)

conn.close() 