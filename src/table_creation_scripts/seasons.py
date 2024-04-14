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
INSERT INTO Seasons (competition_id, season_id, competition_name, season_name, country_name, competition_gender, competition_youth, competition_international)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (competition_id, season_id) DO NOTHING;
"""

target_pairs = {(11, 4), (11, 42), (2, 44), (11, 90)}

with open('../../data/competitions.json', 'r', encoding='utf-8') as file:
    competitions = json.load(file)
    for entry in competitions:
        comp_id = entry['competition_id']
        season_id = entry['season_id']
        if (comp_id, season_id) in target_pairs:
            data = (
                comp_id,
                season_id,
                entry['competition_name'],
                entry['season_name'],
                entry['country_name'],
                entry['competition_gender'],
                entry['competition_youth'],
                entry['competition_international']
            )
            cursor.execute(insert_sql, data)

conn.commit()
cursor.close()
conn.close()

print("Data successfully inserted.")
