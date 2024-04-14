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
lineup_path = '../../data/lineups'

# SQL to query season_id and competition_id from Matches table
query_season_competition_sql = """
SELECT season_id, competition_id FROM Matches WHERE match_id = %s;
"""

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

# SQL to insert or update player data, managing num_matches_played
insert_player_sql = """
INSERT INTO Players (player_id, season_id, competition_id, player_name, player_nickname, jersey_number, country_id, team_id, position_id, num_matches_played)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (player_id, season_id, competition_id) DO UPDATE SET
num_matches_played = EXCLUDED.num_matches_played,
position_id = EXCLUDED.position_id
"""

# Loop through each JSON file in the lineup directory
for filename in os.listdir(lineup_path):
    if filename.endswith('.json'):
        match_id = filename.split('.')[0]  # Extract match_id from filename
        cursor.execute(query_season_competition_sql, (match_id,))
        result = cursor.fetchone()
        if result:
            season_id, competition_id = result
            file_path = os.path.join(lineup_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            all_positions = set()
            all_countries = set()
            all_teams = set()
            all_players = []
            for team in data:
                all_teams.add((team['team_id'], team['team_name']))
                for player in team['lineup']:
                    for position in player.get('positions', []):
                        all_positions.add((position['position_id'], position['position']))
                    if player.get('country'):
                        all_countries.add((player['country']['id'], player['country']['name']))

                    # Check current num_matches_played before inserting
                    check_matches_sql = """
                    SELECT num_matches_played FROM Players
                    WHERE player_id = %s AND season_id = %s AND competition_id = %s;
                    """
                    cursor.execute(check_matches_sql, (player['player_id'], season_id, competition_id))
                    matches_played = cursor.fetchone()
                    if matches_played:
                        num_matches = matches_played[0] + 1
                    else:
                        num_matches = 1  # No record found, initialize to 1

                    # Prepare player data including season_id and competition_id
                    player_tuple = (
                        player['player_id'],
                        season_id,
                        competition_id,
                        player['player_name'],
                        player.get('player_nickname', None),
                        player['jersey_number'],
                        player['country']['id'],
                        team['team_id'],
                        position['position_id'] if player.get('positions') else None,
                        num_matches  # Set num_matches_played based on the query/check above
                    )
                    all_players.append(player_tuple)

            # Perform bulk inserts
            execute_values(cursor, insert_position_sql, list(all_positions))
            execute_values(cursor, insert_country_sql, list(all_countries))
            execute_values(cursor, insert_team_sql, list(all_teams))
            for player in all_players:
                cursor.execute(insert_player_sql, player)

# Commit the transactions
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
