import sqlite3

def init_database():
    conn = sqlite3.connect("portal.db")
    cursor = conn.cursor()
    
    # Drops old table if you had one, to apply new schema structures smoothly
    cursor.execute("DROP TABLE IF EXISTS users")
    
    # Create complete production schema
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL UNIQUE,
        dob TEXT NOT NULL,
        subscription_status TEXT DEFAULT 'Pending',
        payment_id TEXT UNIQUE,
        expiry_date TEXT
    )
    """)
    conn.commit()
    conn.close()
    print("Production subscriber database updated successfully!")

if __name__ == "__main__":
    init_database()