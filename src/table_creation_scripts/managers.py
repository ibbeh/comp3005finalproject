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

# SQL to insert countries if not exists
insert_country_sql = """
INSERT INTO Countries (country_id, country_name)
VALUES %s ON CONFLICT (country_id) DO NOTHING;
"""

insert_manager_sql = """
INSERT INTO Managers (manager_id, manager_name, manager_nickname, dob, country_id)
VALUES %s
ON CONFLICT (manager_id) DO UPDATE SET
manager_name = EXCLUDED.manager_name,
manager_nickname = EXCLUDED.manager_nickname,
dob = EXCLUDED.dob,
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
    all_managers = set()
    for match in data:
        for team_key in ['home_team', 'away_team']:
            team = match.get(team_key, {})
            country = team.get('country', {})
            if country:
                all_countries.add((country['id'], country['name']))
            for manager in team.get('managers', []):
                if manager.get('id') and manager.get('country'):
                    all_managers.add((manager['id'], manager['name'], manager.get('nickname'), manager['dob'], manager['country']['id']))

    # Bulk insert countries and managers
    execute_values(cursor, insert_country_sql, list(all_countries))
    execute_values(cursor, insert_manager_sql, list(all_managers))

# Commit the transactions
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Data successfully initialized.")
