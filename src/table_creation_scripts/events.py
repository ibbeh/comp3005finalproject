import os
import json
import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'FUTSTATS',
    'user': 'postgres',
    'password': 'Kuwait$22',
    'host': 'localhost'
}

# Connect to your PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Path to your events subfolder within the data directory
events_path = 'C:/codeYearTwo/3005_final/data/events'

# Prepare SQL for fetching competition_id and season_id based on match_id
query_match_details_sql = """
SELECT competition_id, season_id FROM Matches WHERE match_id = %s;
"""

# Prepare SQL for inserting events
insert_event_sql = """
INSERT INTO Events (event_id, match_id, type, period, timestamp, minute, second, team_id, player_id, location_x, location_y, competition_id, season_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING;
"""

# Process each JSON file in the events directory
for filename in os.listdir(events_path):
    if filename.endswith('.json'):
        match_id = int(filename.split('.')[0])  # Extract match_id from filename
        cursor.execute(query_match_details_sql, (match_id,))
        match_details = cursor.fetchone()
        if match_details:
            competition_id, season_id = match_details

            # Load the JSON data from the file
            file_path = os.path.join(events_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                events = json.load(file)

            # Extract data from each event and insert it into the database
            for event in events:
                event_id = event['id']
                event_type = event.get('type', {}).get('name')
                period = event.get('period')
                timestamp = event.get('timestamp')
                minute = event.get('minute')
                second = event.get('second')
                team_id = event.get('team', {}).get('id')
                player_id = event.get('player', {}).get('id')
                location = event.get('location', [None, None])
                location_x, location_y = location if location != [None, None] else (None, None)

                # Prepare data tuple for insertion
                data_tuple = (event_id, match_id, event_type, period, timestamp, minute, second, team_id, player_id, location_x, location_y, competition_id, season_id)

                # Execute the insertion command
                cursor.execute(insert_event_sql, data_tuple)

# Commit the transactions to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Events data successfully initialized into the database.")
