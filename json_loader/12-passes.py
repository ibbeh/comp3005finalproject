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

insert_pass_sql = """
INSERT INTO Passes (event_id, pass_technique, successful, length, angle, height, end_location_x, end_location_y, body_part)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING;
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
                            if event.get('type', {}).get('name') == 'Pass':
                                event_id = event['id']
                                pass_info = event['pass']
                                pass_technique = pass_info.get('technique', {}).get('name', 'Regular Pass')
                                successful = 'Incomplete' not in pass_info.get('outcome', {}).get('name', 'Complete')
                                length = pass_info['length']
                                angle = pass_info['angle']
                                height = pass_info['height']['name']
                                end_location_x = pass_info['end_location'][0]
                                end_location_y = pass_info['end_location'][1]
                                body_part = pass_info.get('body_part', {}).get('name', 'Unknown') 
                                
                                data_tuple = (event_id, pass_technique, successful, length, angle, height, end_location_x, end_location_y, body_part)
                                cursor.execute(insert_pass_sql, data_tuple)

conn.commit()
cursor.close()
conn.close()

print("Pass data successfully processed and inserted into the database.")
