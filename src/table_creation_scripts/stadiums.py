import json
import os
import psycopg2
from psycopg2.extras import execute_values

# Database connection parameters
db_params = {
    'dbname': 'FUTSTATS',
    'user': 'postgres',
    'password': 'Kuwait$22',
    'host': 'localhost'
}

# Connect to your PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Path to your JSON files
json_directory = '../../data'

# SQL to insert or update countries
insert_country_sql = """
INSERT INTO Countries (country_id, country_name)
VALUES %s ON CONFLICT (country_id) DO NOTHING;
"""

# SQL to insert or update stadiums
insert_stadium_sql = """
INSERT INTO Stadiums (stadium_id, stadium_name, country_id)
VALUES %s ON CONFLICT (stadium_id) DO UPDATE SET
stadium_name = EXCLUDED.stadium_name,
country_id = EXCLUDED.country_id;
"""

# Process each JSON file in the specified directory
json_files = [f for f in os.listdir(json_directory) if f.endswith('.json') and f not in ['competitions.json']]
for filename in json_files:
    file_path = os.path.join(json_directory, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Prepare data for bulk inserts
    all_countries = set()
    all_stadiums = set()
    for match in data:
        stadium = match.get('stadium', {})
        if stadium and stadium.get('id') and stadium.get('country'):
            country = stadium['country']
            all_countries.add((country['id'], country['name']))
            all_stadiums.add((stadium['id'], stadium['name'], country['id']))

    # Bulk insert countries and stadiums
    execute_values(cursor, insert_country_sql, list(all_countries))
    execute_values(cursor, insert_stadium_sql, list(all_stadiums))

# Commit the transactions
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Stadium data successfully initialized.")
