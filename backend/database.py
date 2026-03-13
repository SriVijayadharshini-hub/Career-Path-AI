import sqlite3

conn = sqlite3.connect("career.db")

cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT
)
""")

# RIASEC ASSESSMENT TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS assessment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    R INTEGER,
    I INTEGER,
    A INTEGER,
    S INTEGER,
    E INTEGER,
    C INTEGER
)
""")

# CAREER PREDICTION TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS prediction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    engineering REAL,
    doctor REAL,
    lawyer REAL,
    arts REAL
)
""")

# PROGRESS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    study_hours INTEGER,
    skills TEXT
)
""")

conn.commit()
conn.close()

print("Database & Tables Created Successfully")