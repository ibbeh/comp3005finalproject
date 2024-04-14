import json
import psycopg2
import os  # Import os module to handle file system operations

# Database connection parameters
host = "localhost"
database = input("DB Name: ")
user = input("DB User: ")
password = input("DB Password: ")
port = "5432"

# Connect to PostgreSQL
conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
cursor = conn.cursor()

# SQL for inserting data into Countries table
insert_sql = """
INSERT INTO Countries (country_id, country_name)
VALUES (%s, %s) ON CONFLICT (country_id) DO NOTHING;
"""

# Define the base directory where the data folders are located
base_dir = '../../data'

# Walk through each directory in the base directory
for dirpath, dirnames, filenames in os.walk(base_dir):
    if 'competitions.json' in filenames:
        filepath = os.path.join(dirpath, 'competitions.json')  # Construct the full file path
        # Load and parse competitions.json
        with open(filepath, 'r', encoding='utf-8') as file:
            competitions = json.load(file)
            seen_countries = {}  # to avoid inserting duplicates
            for entry in competitions:
                country_id = entry['competition_id']  # Assuming the competition_id can serve as the country_id
                country_name = entry['country_name']
                if country_id not in seen_countries:
                    seen_countries[country_id] = country_name
                    data = (country_id, country_name)
                    cursor.execute(insert_sql, data)

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Countries data successfully inserted from all files.")
