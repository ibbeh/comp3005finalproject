import json
import psycopg2
import os

host = "localhost"
database = input("DB Name: ")
user = input("DB User: ")
password = input("DB Password: ")
port = "5432"

conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
cursor = conn.cursor()

insert_sql = """
INSERT INTO Teams (team_id, team_name, manager_id, home_stadium_id, competition_id, season_id, team_gender)
VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (team_id) DO NOTHING;
"""

base_dir = '../json_loader'
season_files = ['90.json', '44.json', '42.json', '4.json'] 

for season_file in season_files:
    filepath = os.path.join(base_dir, season_file)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            matches = json.load(file)
            for match in matches:
                competition_id = match['competition']['competition_id']
                season_id = match['season']['season_id']

                teams_info = [('home_team', match['home_team']), ('away_team', match['away_team'])]
                for team_key, team_data in teams_info:
                    team_id = team_data[team_key+'_id']
                    team_name = team_data[team_key+'_name']
                    team_gender = team_data[team_key+'_gender']
                    manager_id = team_data.get('managers',[{}])[0].get('id', None)
                    
                    stadium_id = match.get('stadium', {}).get('id') if team_key == 'home_team' else None

                    cursor.execute(insert_sql, (team_id, team_name, manager_id, stadium_id, competition_id, season_id, team_gender))
                    print(f"Processed {team_key}: {team_name}")

conn.commit()
cursor.close()
conn.close()

print("Teams data successfully processed and inserted.")
