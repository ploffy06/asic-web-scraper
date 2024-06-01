import sqlite3

def clear_database():
    conn = sqlite3.connect('liquidations.db')
    c = conn.cursor()
    c.execute('DELETE FROM liquidations')  # Delete all records from the table
    conn.commit()
    conn.close()

# Call the function to clear the database
clear_database()
