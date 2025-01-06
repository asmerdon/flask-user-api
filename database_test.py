import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Insert data into the table
cursor.execute('''
INSERT INTO users (name, email)
VALUES ('Alice', 'alice@example.com')
''')

# Fetch all data from the users table
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Commit and close
conn.commit()
conn.close()
