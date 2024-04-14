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

xg_data = {}

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
                competition_id = match['competition']['competition_id']
                season_id = match['season']['season_id']
                event_file_path = os.path.join(events_path, f'{match_id}.json')
                if os.path.exists(event_file_path):
                    with open(event_file_path, 'r', encoding='utf-8') as event_file:
                        events = json.load(event_file)
                        for event in events:
                            if event.get('type', {}).get('name') == 'Shot' and 'statsbomb_xg' in event.get('shot', {}):
                                player_id = event.get('player', {}).get('id')
                                xg_value = event['shot']['statsbomb_xg']
                                key = (player_id, season_id, competition_id)

                                if key not in xg_data:
                                    xg_data[key] = xg_value
                                else:
                                    xg_data[key] += xg_value

for (player_id, season_id, competition_id), total_xg in xg_data.items():
    cursor.execute(
        """
        INSERT INTO xGoals (player_id, total_xg, competition_id, season_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (player_id, season_id, competition_id)
        DO UPDATE SET total_xg = EXCLUDED.total_xg;
        """,
        (player_id, total_xg, competition_id, season_id)
    )

conn.commit()
cursor.close()
conn.close()

print("xGoals data successfully processed and inserted into the database.")
