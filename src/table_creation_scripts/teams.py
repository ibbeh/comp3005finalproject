import json
import os
import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import sql

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

# Path to your JSON files
json_directory = '../../data'

# Function to process each JSON file and update the Teams table
def process_json(file_name):
    with open(os.path.join(json_directory, file_name), 'r', encoding='utf-8') as file:
        data = json.load(file)
        team_dict = {}
        for match in data:
            home_team = match['home_team']
            away_team = match['away_team']
            stadium_info = match.get('stadium')
            
            # Process home team with stadium
            if home_team and stadium_info:
                home_team_id = home_team['home_team_id']
                home_stadium_id = stadium_info['id']
                team_data = (
                    home_team_id,
                    home_team['home_team_name'],
                    home_team.get('managers', [{}])[0].get('id'),  # Safe access for managers
                    home_stadium_id,
                    match['competition']['competition_id'],
                    match['season']['season_id'],
                    home_team['home_team_gender']
                )
                team_dict[home_team_id] = team_data

            # Process away team without stadium
            if away_team:
                away_team_id = away_team['away_team_id']
                team_data = (
                    away_team_id,
                    away_team['away_team_name'],
                    away_team.get('managers', [{}])[0].get('id'),  # Safe access for managers
                    None,  # No stadium for away team
                    match['competition']['competition_id'],
                    match['season']['season_id'],
                    away_team['away_team_gender']
                )
                # Only update if not in dict or no stadium info yet
                if away_team_id not in team_dict or not team_dict[away_team_id][3]:
                    team_dict[away_team_id] = team_data

        # Prepare list of teams from the dictionary
        teams = list(team_dict.values())

        # Insert/update query
        insert_query = sql.SQL("""
            INSERT INTO Teams (team_id, team_name, manager_id, home_stadium_id, competition_id, season_id, team_gender)
            VALUES %s
            ON CONFLICT (team_id) DO UPDATE SET
            manager_id = COALESCE(EXCLUDED.manager_id, Teams.manager_id),
            home_stadium_id = COALESCE(EXCLUDED.home_stadium_id, Teams.home_stadium_id),
            competition_id = COALESCE(EXCLUDED.competition_id, Teams.competition_id),
            season_id = COALESCE(EXCLUDED.season_id, Teams.season_id),
            team_gender = EXCLUDED.team_gender
        """)

        execute_values(cursor, insert_query, teams)
        conn.commit()

# List JSON files excluding 'competitions.json'
json_files = [f for f in os.listdir(json_directory) if f.endswith('.json') and f != 'competitions.json']

# Process each file
for json_file in json_files:
    process_json(json_file)

# Close the database connection
cursor.close()
conn.close()
