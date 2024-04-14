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
INSERT INTO Referees (referee_id, referee_name, country_id)
VALUES (%s, %s, %s) ON CONFLICT (referee_id) DO NOTHING;
"""

base_dir = '../json_loader'
season_files = ['90.json', '44.json', '42.json', '4.json']  
seen_referees = {}  

for season_file in season_files:
    filepath = os.path.join(base_dir, season_file)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            matches = json.load(file)
            for match in matches:
                referee_info = match.get('referee', {})
                referee_id = referee_info.get('id')
                if referee_id and referee_id not in seen_referees:
                    referee_name = referee_info.get('name')
                    country_id = referee_info.get('country', {}).get('id')
                    cursor.execute(insert_sql, (referee_id, referee_name, country_id))
                    seen_referees[referee_id] = referee_name
                    print(f"Inserted referee: {referee_name}")

conn.commit()
cursor.close()
conn.close()

print("Referees data successfully inserted from all files.")
