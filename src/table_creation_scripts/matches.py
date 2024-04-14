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

        insert_query = sql.SQL("""
            INSERT INTO Matches (match_id, match_date, kick_off, season_id, competition_id, home_team_id, home_manager_id, away_team_id, away_manager_id, home_score, away_score, match_week, competition_stage_id, stadium_id, referee_id)
            VALUES %s
            ON CONFLICT (match_id) DO UPDATE SET
            match_date = EXCLUDED.match_date,
            kick_off = EXCLUDED.kick_off,
            season_id = EXCLUDED.season_id,
            competition_id = EXCLUDED.competition_id,
            home_team_id = EXCLUDED.home_team_id,
            home_manager_id = EXCLUDED.home_manager_id,
            away_team_id = EXCLUDED.away_team_id,
            away_manager_id = EXCLUDED.away_manager_id,
            home_score = EXCLUDED.home_score,
            away_score = EXCLUDED.away_score,
            match_week = EXCLUDED.match_week,
            competition_stage_id = EXCLUDED.competition_stage_id,
            stadium_id = EXCLUDED.stadium_id,
            referee_id = EXCLUDED.referee_id
        """)

        execute_values(cursor, insert_query, matches)
        conn.commit()

json_files = [f for f in os.listdir(json_directory) if f.endswith('.json') and f != 'competitions.json']

for json_file in json_files:
    process_json(json_file)

cursor.close()
conn.close()
