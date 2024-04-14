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

base_dir = '../../data'

for dirpath, dirnames, filenames in os.walk(base_dir):
    if 'competitions.json' in filenames:
        filepath = os.path.join(dirpath, 'competitions.json')
        with open(filepath, 'r', encoding='utf-8') as file:
            competitions = json.load(file)
            seen_countries = {}
            for entry in competitions:
                country_id = entry['competition_id']
                country_name = entry['country_name']
                if country_id not in seen_countries:
                    seen_countries[country_id] = country_name
                    data = (country_id, country_name)
                    cursor.execute(insert_sql, data)
                    
conn.commit()
cursor.close()
conn.close()

print("Countries data successfully inserted from all files.")
