import os
import json
import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'FUTDB',
    'user': 'postgres',
    'password': 'Kuwait$22',
    'host': 'localhost'
}

# Connect to your PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Path to your events subfolder
events_path = 'C:/codeYearTwo/3005_final/data/events'

# Helper function to get player xG
def update_player_xg(player_id, xg_value):
    cursor.execute("SELECT total_xg FROM xGoals WHERE player_id = %s;", (player_id,))
    result = cursor.fetchone()
    if result:
        new_xg = result[0] + xg_value
        cursor.execute("UPDATE xGoals SET total_xg = %s WHERE player_id = %s;", (new_xg, player_id))
    else:
        cursor.execute("INSERT INTO xGoals (player_id, total_xg) VALUES (%s, %s);", (player_id, xg_value))

# Process each JSON file
for filename in os.listdir(events_path):
    if filename.endswith('.json'):
        file_path = os.path.join(events_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            events = json.load(file)
            for event in events:
                event_id = event['id']
                event_type = event.get('type', {}).get('name')
                
                # Handling xGoals within Shot events
                if event_type == 'Shot':
                    player_id = event.get('player', {}).get('id')
                    xg_value = event.get('shot', {}).get('statsbomb_xg', 0)
                    update_player_xg(player_id, xg_value)

                # Handling Goals
                if event_type == 'Goal':
                    goal_type = event.get('goal_type', {}).get('name', 'Regular')
                    assist_event_id = event.get('pass', {}).get('id')
                    shot_id = event.get('shot_id')
                    cursor.execute("INSERT INTO Goals (event_id, goal_type, assist_event_id, shot_id) VALUES (%s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING;", (event_id, goal_type, assist_event_id, shot_id))

                # Handling Penalties
                if event_type == 'Penalty':
                    goal_id = event.get('goal_id')
                    cursor.execute("INSERT INTO Penalties (event_id, goal_id) VALUES (%s, %s) ON CONFLICT (event_id) DO NOTHING;", (event_id, goal_id))

                # Handling Free Kicks
                if event_type == 'Free Kick':
                    goal_id = event.get('goal_id')
                    pass_id = event.get('pass_id')
                    body_part = event.get('body_part', {}).get('name')
                    cursor.execute("INSERT INTO Free_Kick (event_id, goal_id, pass_id, body_part) VALUES (%s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING;", (event_id, goal_id, pass_id, body_part))

                # Handling Corners
                if event_type == 'Corner':
                    technique = event.get('technique', {}).get('name')
                    body_part = event.get('body_part', {}).get('name')
                    outcome = event.get('outcome', {}).get('name')
                    cursor.execute("INSERT INTO Corners (event_id, technique, body_part, outcome) VALUES (%s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING;", (event_id, technique, body_part, outcome))

                # Handling Goal Kicks
                if event_type == 'Goal Kick':
                    pass_id = event.get('pass_id')
                    cursor.execute("INSERT INTO Goal_Kick (event_id, pass_id) VALUES (%s, %s) ON CONFLICT (event_id) DO NOTHING;", (event_id, pass_id))

# Commit the transactions
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Events data successfully parsed and database updated.")
