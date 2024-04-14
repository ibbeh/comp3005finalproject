import json
import psycopg2
import os

host = "localhost"
database = input("DB Name: ")
user = input("DB User: ")
password = input("DB Password: ")
port = "5432"

conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
cursor = conn.cursor()

base_dir = '../json_loader'
events_path = os.path.join(base_dir, 'events')

for filename in os.listdir(events_path):
    if filename.endswith('.json'):
        file_path = os.path.join(events_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            events = json.load(file)
            for event in events:
                if event.get('type', {}).get('name') == 'Dribble':
                    event_id = event['id']
                    success = 'outcome' in event.get('dribble', {}) and event['dribble']['outcome'].get('name') != 'Incomplete'
                    
                    cursor.execute(
                        """
                        INSERT INTO Dribbles (event_id, success)
                        VALUES (%s, %s)
                        ON CONFLICT (event_id) DO NOTHING;
                        """,
                        (event_id, success)
                    )

conn.commit()
cursor.close()
conn.close()

print("Dribbles data successfully processed and inserted into the database.")
