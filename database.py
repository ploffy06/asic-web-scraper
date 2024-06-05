import sqlite3
from notifier import send_email_notification

def create_database():
    conn = sqlite3.connect('liquidations.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS liquidations (
            id INTEGER PRIMARY KEY,
            company_name TEXT,
            acn TEXT,
            date_published TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_liquidation_data(liquidation):
    conn = sqlite3.connect('liquidations.db')
    c = conn.cursor()
    company_name = liquidation['company_name']
    acn = liquidation['acn']
    date_published = liquidation['date_published']
    c.execute('''
        INSERT INTO liquidations (company_name, acn, date_published)
        VALUES (?, ?, ?)
    ''', [company_name, acn, date_published])

    print(f'stored | company_name: {liquidation["company_name"]}, acn: {liquidation["acn"]}, date published: {liquidation["date_published"]}')
    conn.commit()
    conn.close()

def check_for_new_entries(liquidations):
    conn = sqlite3.connect('liquidations.db')
    c = conn.cursor()
    c.execute('SELECT company_name, acn, date_published FROM liquidations')
    existing_data = c.fetchall()
    existing_set = set(existing_data)

    for liquidation in liquidations:
        liquidation_tuple = (liquidation['company_name'], liquidation['acn'], liquidation['date_published'])
        if liquidation_tuple not in existing_set:
            store_liquidation_data(liquidation)
            send_email_notification(liquidation)

    conn.close()
