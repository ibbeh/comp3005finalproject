import json
import psycopg2
import os

# Database connection setup
host = "localhost"
database = input("DB Name: ")
user = input("DB User: ")
password = input("DB Password: ")
port = "5432"

# Connect to PostgreSQL database
conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
cursor = conn.cursor()

# SQL command to insert matches
insert_match_sql = """
INSERT INTO Matches (match_id, match_date, kick_off, season_id, competition_id, home_team_id, home_manager_id, away_team_id, away_manager_id, home_score, away_score, match_week, competition_stage_id, stadium_id, referee_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (match_id) DO NOTHING;
"""

# Function to process each season's JSON file for matches
def process_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        matches = []
        for match in data:
            stadium_id = match.get('stadium', {}).get('id')
            referee_id = match.get('referee', {}).get('id')

            match_data = (
                match['match_id'],
                match['match_date'],
                match['kick_off'],
                match['season']['season_id'],
                match['competition']['competition_id'],
                match['home_team']['home_team_id'],
                match['home_team'].get('managers', [{}])[0].get('id'),
                match['away_team']['away_team_id'],
                match['away_team'].get('managers', [{}])[0].get('id'),
                match['home_score'],
                match['away_score'],
                match['match_week'],
                match['competition_stage']['id'],
                stadium_id,
                referee_id
            )
            matches.append(match_data)
        return matches

# Directory and file handling
base_dir = '../json_loader'
season_files = ['4.json', '42.json', '44.json', '90.json']  # Specific season JSON files

# Process each specified season file for matches
for season_file in season_files:
    filepath = os.path.join(base_dir, season_file)
    if os.path.exists(filepath):
        match_entries = process_json(filepath)
        for entry in match_entries:
            cursor.execute(insert_match_sql, entry)

# Commit changes and close the database connection
conn.commit()
cursor.close()
conn.close()

print("Matches data successfully processed and inserted.")
