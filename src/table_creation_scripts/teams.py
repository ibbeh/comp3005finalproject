import json
import os
import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import sql

db_params = {
    'dbname': 'FUTSTATS',
    'user': 'postgres',
    'password': 'Kuwait$22',
    'host': 'localhost'
}

conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

json_directory = '../../data'

def process_json(file_name):
    with open(os.path.join(json_directory, file_name), 'r', encoding='utf-8') as file:
        data = json.load(file)
        team_dict = {}
        for match in data:
            home_team = match['home_team']
            away_team = match['away_team']
            stadium_info = match.get('stadium')
            
            if home_team and stadium_info:
                home_team_id = home_team['home_team_id']
                home_stadium_id = stadium_info['id']
                team_data = (
                    home_team_id,
                    home_team['home_team_name'],
                    home_team.get('managers', [{}])[0].get('id'),
                    home_stadium_id,
                    match['competition']['competition_id'],
                    match['season']['season_id'],
                    home_team['home_team_gender']
                )
                team_dict[home_team_id] = team_data

            if away_team:
                away_team_id = away_team['away_team_id']
                team_data = (
                    away_team_id,
                    away_team['away_team_name'],
                    away_team.get('managers', [{}])[0].get('id'),
                    None,
                    match['competition']['competition_id'],
                    match['season']['season_id'],
                    away_team['away_team_gender']
                )
                if away_team_id not in team_dict or not team_dict[away_team_id][3]:
                    team_dict[away_team_id] = team_data

        teams = list(team_dict.values())

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

json_files = [f for f in os.listdir(json_directory) if f.endswith('.json') and f != 'competitions.json']

for json_file in json_files:
    process_json(json_file)

cursor.close()
conn.close()
