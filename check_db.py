import sqlite3

conn = sqlite3.connect("marketplace.db")
cursor = conn.cursor()

tables = ["users", "products", "orders", "order_items"]

for table in tables:
    print(f"\n--- {table.upper()} ---")
    cursor.execute(f"PRAGMA table_info({table})")

    for column in cursor.fetchall():
        print(column)

conn.close()