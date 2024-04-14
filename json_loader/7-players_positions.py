import json
import psycopg2
import os

# Database connection setup
host = "localhost"
database = input("DB Name: ")
user = input("DB User: ")
password = input("DB Password: ")
port = "5432"

conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
cursor = conn.cursor()

# SQL commands
insert_position_sql = """
INSERT INTO Positions (position_id, position_name) VALUES (%s, %s) ON CONFLICT (position_id) DO NOTHING;
"""
insert_player_sql = """
INSERT INTO Players (player_id, season_id, competition_id, player_name, player_nickname, jersey_number, country_id, team_id, position_id, num_matches_played) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (player_id, season_id, competition_id) DO UPDATE SET num_matches_played = Players.num_matches_played + 1;
"""
insert_country_sql = """
INSERT INTO Countries (country_id, country_name) VALUES (%s, %s) ON CONFLICT (country_id) DO NOTHING;
"""

# Directory and file handling
base_dir = '../json_loader'
season_files = ['4.json', '42.json', '44.json', '90.json']
lineup_dir = os.path.join(base_dir, 'lineups')

# Process each specified season file for matches
for season_file in season_files:
    filepath = os.path.join(base_dir, season_file)
    with open(filepath, 'r', encoding='utf-8') as file:
        matches = json.load(file)
        for match in matches:
            competition_id = match['competition']['competition_id']
            season_id = match['season']['season_id']
            match_id = match['match_id']

            # Load lineup for the current match
            lineup_path = os.path.join(lineup_dir, f"{match_id}.json")
            if os.path.exists(lineup_path):
                with open(lineup_path, 'r', encoding='utf-8') as lineup_file:
                    lineup_data = json.load(lineup_file)
                    for team in lineup_data:
                        team_id = team['team_id']
                        for player in team['lineup']:
                            player_id = player['player_id']
                            player_name = player['player_name']
                            player_nickname = player.get('player_nickname')
                            jersey_number = player['jersey_number']
                            country_id = player['country']['id']
                            country_name = player['country']['name']
                            
                            # Insert or update country information
                            cursor.execute(insert_country_sql, (country_id, country_name))
                            
                            # Initialize matches played as this is the first appearance in this loop
                            num_matches_played = 1
                            
                            # Track all positions for the player
                            for position in player.get('positions', []):
                                position_id = position['position_id']
                                position_name = position['position']
                                cursor.execute(insert_position_sql, (position_id, position_name))
                            
                            # Insert or update player data
                            cursor.execute(insert_player_sql, (player_id, season_id, competition_id, player_name, player_nickname, jersey_number, country_id, team_id, position_id, num_matches_played))
                    
# Commit changes and close the database connection
conn.commit()
cursor.close()
conn.close()

print("Positions and Players data successfully processed and inserted.")
