import json
import psycopg2
import os

# Database connection setup
host = "localhost"
database = input("DB Name: ")
user = input("DB User: ")
password = input("DB Password: ")
port = "5432"

# Connect to PostgreSQL database
conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
cursor = conn.cursor()

# SQL to insert unique stadiums
insert_sql = """
INSERT INTO Stadiums (stadium_id, stadium_name, country_id)
VALUES (%s, %s, %s) ON CONFLICT (stadium_id) DO NOTHING;
"""

base_dir = '../json_loader'
season_files = ['90.json', '44.json', '42.json', '4.json']  # Specific season JSON files
seen_stadiums = {}  # To track unique stadiums

# Process each specified season file
for season_file in season_files:
    filepath = os.path.join(base_dir, season_file)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            matches = json.load(file)
            for match in matches:
                stadium_info = match.get('stadium', {})
                stadium_id = stadium_info.get('id')
                if stadium_id and stadium_id not in seen_stadiums:
                    stadium_name = stadium_info.get('name')
                    country_id = stadium_info.get('country', {}).get('id')
                    # Insert unique stadium into the database
                    cursor.execute(insert_sql, (stadium_id, stadium_name, country_id))
                    seen_stadiums[stadium_id] = stadium_name
                    print(f"Inserted stadium: {stadium_name}")

# Commit changes and close the database connection
conn.commit()
cursor.close()
conn.close()

print("Stadiums data successfully inserted from all files.")
