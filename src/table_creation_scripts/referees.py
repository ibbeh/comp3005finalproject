import json
import os
import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import sql

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

# Function to process each JSON file and update the Referees table
def process_json(file_name):
    with open(os.path.join(json_directory, file_name), 'r', encoding='utf-8') as file:
        data = json.load(file)
        referee_dict = {}
        for match in data:
            referee_info = match.get('referee')
            if referee_info:
                referee_id = referee_info['id']
                referee_data = (
                    referee_id,
                    referee_info['name'],
                    referee_info['country']['id']
                )
                # Use referee_id to prevent duplicates within the same batch
                referee_dict[referee_id] = referee_data

        referees = list(referee_dict.values())

        # Insert/update query
        insert_query = sql.SQL("""
            INSERT INTO Referees (referee_id, referee_name, country_id)
            VALUES %s
            ON CONFLICT (referee_id) DO UPDATE SET
            referee_name = EXCLUDED.referee_name,
            country_id = EXCLUDED.country_id
        """)

        execute_values(cursor, insert_query, referees)
        conn.commit()

# List JSON files excluding 'competitions.json'
json_files = [f for f in os.listdir(json_directory) if f.endswith('.json') and f != 'competitions.json']

# Process each file
for json_file in json_files:
    process_json(json_file)

# Close the database connection
cursor.close()
conn.close()
