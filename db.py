import sqlite3

# Connect to the database 'mydatabase.db'. If it doesn't exist, it will be created.
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# SQL command to create the 'users' table
create_table_query = '''
CREATE TABLE IF NOT EXISTS users(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   username TEXT NOT NULL UNIQUE,
   name TEXT NOT NULL,
   password_hash TEXT NOT NULL
);
'''

# Execute the command
cursor.execute(create_table_query)

# Commit the changes
conn.commit()

# Close the connection
conn.close()
