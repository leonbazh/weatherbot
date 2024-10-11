import psycopg2
from datetime import datetime

# Connect to the PostgreSQL database
def get_connection():
    return psycopg2.connect(
        host="localhost",      # Host where the DB is deployed
        database="postgres",    # Database name
        user="postgres",      # Username
        password="your_passw"   # User password
    )

# Function to create a table (once, if the table does not exist)
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create a table for request logs
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                      id SERIAL PRIMARY KEY,
                      user_id BIGINT,
                      command TEXT,
                      timestamp TIMESTAMP,
                      response TEXT
                      )''')
    conn.commit()
    cursor.close()
    conn.close()

# Logging requests to the database
def log_request(user_id, command, response):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Request time
    timestamp = datetime.now()

    # SQL query to insert data
    cursor.execute('INSERT INTO logs (user_id, command, timestamp, response) VALUES (%s, %s, %s, %s)',
                   (user_id, command, timestamp, response))
    
    # Save changes to the database
    conn.commit()
    
    cursor.close()
    conn.close()
