import json
import psycopg2

#Database connection parameters
host = "localhost"
database = "FUT"
user = input("DB User: ")
password = input("DB Password: ")
port = "5432"

# Connection to PostgreSQL
conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
cursor = conn.cursor()

# SQL for inserting data
insert_sql = """
INSERT INTO Competitions (competition_id, season_id, country_name, competition_name, competition_gender, competition_youth, competition_international, season_name)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (competition_id, season_id) DO NOTHING;
"""

# Load and parse competitions.json
with open('data/competitions.json', 'r') as file:
    competitions = json.load(file)

# Filtered competition and season pairs
target_competitions = [(11, 4), (11, 42), (2, 44), (11, 90)]

# Process each competition
for competition in competitions:
    comp_id = competition['competition_id']
    season_id = competition['season_id']
    if (comp_id, season_id) in target_competitions:
        data = (
            comp_id,
            season_id,
            competition['country_name'],
            competition['competition_name'],
            competition['competition_gender'],
            competition['competition_youth'],
            competition['competition_international'],
            competition['season_name']
        )
        cursor.execute(insert_sql, data)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

print("Data successfully inserted.")