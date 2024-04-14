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
INSERT INTO Countries (country_id, country_name)
VALUES (%s, %s) ON CONFLICT (country_id) DO NOTHING;
"""

base_dir = '../json_loader'
season_files = ['90.json', '44.json', '42.json', '4.json']  
seen_countries = {}  

for season_file in season_files:
    filepath = os.path.join(base_dir, season_file)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            matches = json.load(file)
            for match in matches:
                teams = [match.get('home_team'), match.get('away_team')]
                for team in teams:
                    if team and 'managers' in team:
                        for manager in team['managers']:
                            if 'country' in manager:
                                country = manager['country']
                                country_id = country.get('id')
                                country_name = country.get('name')
                                if country_id and country_id not in seen_countries:
                                    cursor.execute(insert_sql, (country_id, country_name))
                                    seen_countries[country_id] = country_name
                                    print(f"Inserted country: {country_name}")

conn.commit()
cursor.close()
conn.close()

print("Manager country data successfully inserted from all files.")
