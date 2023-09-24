import sqlite3
from pathlib import Path

# connect to database
conn = sqlite3.connect("user.db")

# create a cursor
c = conn.cursor()

# create a table
db_path = Path(__file__).parents[1].resolve() / "user.db"
if not db_path.exists():
    c.execute("""CREATE TABLE users (
        first_name text,
        last_name text,
        email text
    )""")

# insert single entry
# c.execute("INSERT INTO users VALUES ('Yang', 'Liu', 'liuyang@gmail.com')")

# insert multiple entries
# many_users = [('Bach', 'Nostal', 'nostalbach@hotmail.com'),
#          ('Jingyi', 'Wang', 'jingyiwang@gmail.com'),
#          ]
# c.executemany("INSERT INTO users VALUES (?,?,?)", many_users)

# query database and search with WHERE clause
#c.execute("SELECT rowid, * FROM users WHERE first_name = 'Yang'")
c.execute("SELECT rowid, * FROM users WHERE email LIKE '%gmail%'")

# c.fetchone()
# c.fetchmany(5)

entries = c.fetchall()

for entry in entries:
    print(entry)

# commit our command
conn.commit()

# close connection
conn.close()