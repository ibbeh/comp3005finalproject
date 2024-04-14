import json
import psycopg2
import os
from datetime import datetime

# Database connection setup
host = "localhost"
database = input("DB Name: ")
user = input("DB User: ")
password = input("DB Password: ")
port = "5432"

# Connect to PostgreSQL database
conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
cursor = conn.cursor()

# SQL to insert manager data, avoiding duplicates with the manager_id primary key
insert_sql = """
INSERT INTO Managers (manager_id, manager_name, manager_nickname, dob, country_id)
VALUES (%s, %s, %s, %s, %s) ON CONFLICT (manager_id) DO NOTHING;
"""

base_dir = '../json_loader'
season_files = ['90.json', '44.json', '42.json', '4.json']  # List of specific season JSON files

# Process each specified season file
for season_file in season_files:
    filepath = os.path.join(base_dir, season_file)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            matches = json.load(file)
            for match in matches:
                # Process both home and away team managers
                teams = ['home_team', 'away_team']
                for team in teams:
                    managers = match.get(team, {}).get('managers', [])
                    for manager in managers:
                        manager_id = manager.get('id')
                        manager_name = manager.get('name')
                        manager_nickname = manager.get('nickname', None)  # Default None if nickname is not provided
                        dob = manager.get('dob', None)
                        country_id = manager.get('country', {}).get('id', None)
                        
                        # Convert date of birth to appropriate format
                        dob_date = None
                        if dob:
                            try:
                                dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
                            except ValueError:
                                print(f"Date format error for manager {manager_name}")

                        # Insert manager data into the database
                        data = (manager_id, manager_name, manager_nickname, dob_date, country_id)
                        cursor.execute(insert_sql, data)
                        print(f"Inserted manager: {manager_name} with ID {manager_id}")

# Commit changes and close the database connection
conn.commit()
cursor.close()
conn.close()

print("Manager data successfully inserted from all files.")
