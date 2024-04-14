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

insert_goal_sql = """
INSERT INTO Goals (event_id, goal_type, assist_event_id, shot_id)
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
                            try:
                                if event.get('type', {}).get('name') == 'Goal':
                                    event_id = event['id']
                                    goal_type = event['type']['name']
                                    assist_event_id = event.get('assist', {}).get('id')
                                    shot_id = event.get('shot', {}).get('id')
                                    
                                    data_tuple = (event_id, goal_type, assist_event_id, shot_id)
                                    cursor.execute(insert_goal_sql, data_tuple)
                            except Exception as e:
                                print("Failed to insert data:", e)
                                continue

# Commit changes and close the connection
try:
    conn.commit()
    cursor.close()
    conn.close()
    print("Goal data successfully processed and inserted into the database.")
except Exception as e:
    print("Error during commit or connection close:", e)