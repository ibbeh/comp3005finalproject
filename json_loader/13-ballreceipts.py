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

insert_ball_receipt_sql = """
INSERT INTO Ball_Receipts (event_id, successful, location_x, location_y)
VALUES (%s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING;
"""

base_dir = '../json_loader'
season_files = ['90.json', '44.json', '42.json', '4.json'] 
events_path = os.path.join(base_dir, 'events')

for season_file in season_files:
    filepath = os.path.join(base_dir, season_file)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            matches = json.load(file)
            for match in matches:
                match_id = match['match_id']
                event_file_path = os.path.join(events_path, f'{match_id}.json')
                if os.path.exists(event_file_path):
                    with open(event_file_path, 'r', encoding='utf-8') as event_file:
                        events = json.load(event_file)
                        for event in events:
                            if event.get('type', {}).get('name') == 'Ball Receipt*':
                                event_id = event['id']
                                location = event.get('location', [None, None])
                                location_x, location_y = location if location is not None else (None, None)
                                successful = not event.get('ball_receipt', {}).get('outcome', {}).get('name') == 'Incomplete'

                                data_tuple = (event_id, successful, location_x, location_y)
                                cursor.execute(insert_ball_receipt_sql, data_tuple)

conn.commit()
cursor.close()
conn.close()

print("Ball receipt data successfully processed and inserted into the database.")
