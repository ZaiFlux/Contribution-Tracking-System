import sqlite3

conn = sqlite3.connect("contribution.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS programs (
    name TEXT,
    purpose TEXT,
    target REAL,
    due TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS contributors (
    program_name TEXT,
    name TEXT,
    category TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    current REAL,
    target REAL
)
""")

conn.commit()
conn.close()