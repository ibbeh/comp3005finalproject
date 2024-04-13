import os
import json
import psycopg2
from psycopg2.extras import execute_values

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

# Path to your lineup subfolder
lineup_path = 'C:/codeYearTwo/3005_final/data/lineups'

# SQL to insert positions, countries, and teams if not exists
insert_position_sql = """
INSERT INTO Positions (position_id, position_name)
VALUES %s ON CONFLICT (position_id) DO NOTHING;
"""

insert_country_sql = """
INSERT INTO Countries (country_id, country_name)
VALUES %s ON CONFLICT (country_id) DO NOTHING;
"""

insert_team_sql = """
INSERT INTO Teams (team_id, team_name)
VALUES %s ON CONFLICT (team_id) DO NOTHING;
"""

# Loop through each JSON file in the lineup directory
for filename in os.listdir(lineup_path):
    if filename.endswith('.json'):
        file_path = os.path.join(lineup_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:  # specify UTF-8 encoding
            data = json.load(file)
        
        # Prepare data for bulk inserts
        all_positions = set()
        all_countries = set()
        all_teams = set()
        for team in data:
            all_teams.add((team['team_id'], team['team_name']))  # Collect team data
            for player in team['lineup']:
                for position in player.get('positions', []):
                    all_positions.add((position['position_id'], position['position']))
                if player.get('country'):
                    all_countries.add((player['country']['id'], player['country']['name']))

        # Bulk insert positions, countries, and teams
        execute_values(cursor, insert_position_sql, list(all_positions))
        execute_values(cursor, insert_country_sql, list(all_countries))
        execute_values(cursor, insert_team_sql, list(all_teams))

        # Insert or update player data
        for team in data:
            team_id = team['team_id']
            for player in team['lineup']:
                position_id = player['positions'][0]['position_id'] if player['positions'] else None
                player_data = (
                    player['player_id'],
                    player['player_name'],
                    player.get('player_nickname', None),
                    player['jersey_number'],
                    player['country']['id'],
                    team_id,
                    position_id
                )
                
                # Insert or update player
                insert_player_sql = """
                INSERT INTO Players (player_id, player_name, player_nickname, jersey_number, country_id, team_id, position_id, num_matches_played)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
                ON CONFLICT (player_id) DO UPDATE SET
                    num_matches_played = Players.num_matches_played + 1,
                    position_id = EXCLUDED.position_id
                """
                cursor.execute(insert_player_sql, player_data)

# Commit the transactions
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
