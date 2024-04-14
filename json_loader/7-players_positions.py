import os
import json
import psycopg2
from psycopg2.extras import execute_values

db_params = {
    'dbname': input('DB Name: '),
    'user': input('DB User: '),
    'password': input('DB Password: '),
    'host': 'localhost'
}

conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

lineup_path = '../json_loader/lineups'

query_season_competition_sql = """
SELECT season_id, competition_id FROM Matches WHERE match_id = %s;
"""

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

insert_player_sql = """
INSERT INTO Players (player_id, season_id, competition_id, player_name, player_nickname, jersey_number, country_id, team_id, position_id, num_matches_played)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (player_id, season_id, competition_id) DO UPDATE SET
num_matches_played = EXCLUDED.num_matches_played,
position_id = EXCLUDED.position_id
"""

for filename in os.listdir(lineup_path):
    if filename.endswith('.json'):
        match_id = filename.split('.')[0]
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
                        print(f"Adding position: {position['position']}")
                    if player.get('country'):
                        all_countries.add((player['country']['id'], player['country']['name']))

                    check_matches_sql = """
                    SELECT num_matches_played FROM Players
                    WHERE player_id = %s AND season_id = %s AND competition_id = %s;
                    """
                    cursor.execute(check_matches_sql, (player['player_id'], season_id, competition_id))
                    matches_played = cursor.fetchone()
                    if matches_played:
                        num_matches = matches_played[0] + 1
                    else:
                        num_matches = 1

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
                        num_matches
                    )
                    all_players.append(player_tuple)
                    print(f"Adding player: {player['player_name']}")

            execute_values(cursor, insert_position_sql, list(all_positions))
            execute_values(cursor, insert_country_sql, list(all_countries))
            execute_values(cursor, insert_team_sql, list(all_teams))
            for player in all_players:
                cursor.execute(insert_player_sql, player)

conn.commit()

cursor.close()
conn.close()

print("All data successfully processed and inserted.")
