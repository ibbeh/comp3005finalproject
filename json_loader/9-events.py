import json
import psycopg2
import os
from datetime import datetime

# Database connection setup
host = "localhost"
database = input("DB Name: ")
user = input("DB User: ")
password = input("DB Password: ")
port = "5432"

# Connect to PostgreSQL database
conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
cursor = conn.cursor()

# Prepare the SQL statement for inserting event data
insert_event_sql = """
INSERT INTO Events (event_id, match_id, type, period, timestamp, minute, second, team_id, player_id, location_x, location_y, competition_id, season_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING;
"""

# Paths configuration
base_dir = '../json_loader'
season_files = ['90.json', '44.json', '42.json', '4.json']
events_path = os.path.join(base_dir, 'events')

# Extract match_ids from season files and process corresponding events
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
                            event_id = event['id']
                            event_type = event.get('type', {}).get('name')
                            period = event.get('period')
                            timestamp = datetime.strptime(event.get('timestamp'), '%H:%M:%S.%f').time() if event.get('timestamp') else None
                            minute = event.get('minute')
                            second = event.get('second')
                            team_id = event.get('team', {}).get('id')
                            player_id = event.get('player', {}).get('id')
                            location = event.get('location', [None, None])
                            location_x, location_y = location if location != [None, None] else (None, None)

                            data_tuple = (event_id, match_id, event_type, period, timestamp, minute, second, team_id, player_id, location_x, location_y, competition_id, season_id)
                            cursor.execute(insert_event_sql, data_tuple)
                            
# Commit changes and close the database connection
conn.commit()
cursor.close()
conn.close()
print("Events data successfully processed and inserted.")
