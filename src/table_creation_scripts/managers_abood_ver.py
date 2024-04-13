import json
import os
import psycopg2

# Database connection parameters
host = "localhost"
database = input("DB Name: ")
user = input("DB User: ")
password = input("DB Password: ")
port = "5432"

# Connect to PostgreSQL
conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
cursor = conn.cursor()

# SQL for inserting data
insert_sql = """
INSERT INTO Managers (manager_id, manager_name, manager_nickname, dob, country_id)
VALUES (%s, %s, %s, %s, %s);
"""

# Define the path to the directory containing JSON files
json_directory = "C:/codeYearTwo/3005_final/data"

# Process each JSON file individually
for filename in os.listdir(json_directory):
    if filename.endswith(".json") and filename != 'competitions.json':
        file_path = os.path.join(json_directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            match_data = json.load(file)
            print(f"Processing file: {filename}")
            for match in match_data:
                # Check if manager_id is not None
                if match.get("manager_id") is not None:
                    manager_id = match["manager_id"]
                    manager_name = match["manager_name"]
                    manager_nickname = match["manager_nickname"]
                    dob = match["dob"]
                    country_id = match["country_id"]
                    
                    # Execute the insert SQL statement
                    data = (manager_id, manager_name, manager_nickname, dob, country_id)
                    cursor.execute(insert_sql, data)
                    print(f"Manager added: {manager_id} from {filename}")

# Commit changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Data successfully inserted.")
