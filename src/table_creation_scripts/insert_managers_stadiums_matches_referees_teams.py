"""
This script parses a JSON file containing match data and inserts the data into a PostgreSQL database.
It fills five tables: Managers, Stadiums, Teams, Matches, and Referees, based on the relationships defined in the provided schema.

Usage:
    Run this script from the command line, providing the path to the JSON file as an argument:
    $ python script_name.py path_to_your_json_file.json

Requirements:
    - psycopg2: PostgreSQL database adapter for Python.
    - json: To parse JSON files.
    Ensure that PostgreSQL credentials and connection details are correctly configured in the connect_to_db function.

Example JSON structure:
{
  "match_id": 123,
  "match_date": "YYYY-MM-DD",
  "kick_off": "HH:MM:SS",
  "competition": {
    "competition_id": 11,
    "country_name": "Country",
    "competition_name": "Competition"
  },
  ...
}

The script processes each match, extracting details about the match, teams, managers, stadium, and referee, inserting or updating records in the respective tables.
"""

import json
import psycopg2
import sys

def connect_to_db():
    """Connect to the PostgreSQL database server."""
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            dbname="FUT_STATS",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful.")
    return conn

def insert_country(conn, country_id, country_name):
    """Insert or update a country in the Countries table."""
    cursor = conn.cursor()
    sql = """
    INSERT INTO Countries(country_id, country_name) 
    VALUES (%s, %s) ON CONFLICT (country_id) DO UPDATE SET country_name = EXCLUDED.country_name;
    """
    cursor.execute(sql, (country_id, country_name))
    conn.commit()
    cursor.close()

def insert_manager(conn, manager):
    """Insert a manager into the Managers table."""
    insert_country(conn, manager['country']['id'], manager['country']['name'])
    cursor = conn.cursor()
    sql = """
    INSERT INTO Managers(manager_id, manager_name, manager_nickname, dob, country_id) 
    VALUES (%s, %s, %s, %s, %s) ON CONFLICT (manager_id) DO NOTHING;
    """
    cursor.execute(sql, (manager['id'], manager['name'], manager.get('nickname', None), manager['dob'], manager['country']['id']))
    conn.commit()
    cursor.close()

def insert_team(conn, team):
    """Insert a team into the Teams table, including their manager."""
    insert_country(conn, team['country']['id'], team['country']['name'])
    cursor = conn.cursor()
    # Insert manager(s) for the team
    if 'managers' in team and team['managers']:
        for manager in team['managers']:
            insert_manager(conn, manager)
        manager_id = team['managers'][0]['id']
    else:
        manager_id = None  # Defaulting to None if no managers are present

    sql = """
    INSERT INTO Teams(team_id, team_name, manager_id, home_stadium_id, competition_id, season_id, team_gender) 
    VALUES (%s, %s, %s, NULL, NULL, NULL, %s) ON CONFLICT (team_id) DO NOTHING;
    """
    cursor.execute(sql, (team['home_team_id'], team['home_team_name'], manager_id, team['home_team_gender']))
    conn.commit()
    cursor.close()

def insert_stadium(conn, stadium):
    """Insert a stadium into the Stadiums table."""
    insert_country(conn, stadium['country']['id'], stadium['country']['name'])
    cursor = conn.cursor()
    sql = """
    INSERT INTO Stadiums(stadium_id, stadium_name, country_id) 
    VALUES (%s, %s, %s) ON CONFLICT (stadium_id) DO NOTHING;
    """
    cursor.execute(sql, (stadium['id'], stadium['name'], stadium['country']['id']))
    conn.commit()
    cursor.close()

def insert_referee(conn, referee):
    """Insert a referee into the Referees table."""
    insert_country(conn, referee['country']['id'], referee['country']['name'])
    cursor = conn.cursor()
    sql = """
    INSERT INTO Referees(referee_id, referee_name, country_id) 
    VALUES (%s, %s, %s) ON CONFLICT (referee_id) DO NOTHING;
    """
    cursor.execute(sql, (referee['id'], referee['name'], referee['country']['id']))
    conn.commit()
    cursor.close()

def insert_match(conn, match):
    """Insert a match into the Matches table."""
    cursor = conn.cursor()
    sql = """
    INSERT INTO Matches(match_id, match_date, kick_off, season_id, competition_id, home_team_id, 
    home_manager_id, away_team_id, away_manager_id, home_score, away_score, match_week, 
    competition_stage_id, stadium_id, referee_id) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (match_id) DO NOTHING;
    """
    cursor.execute(sql, (
        match['match_id'], match['match_date'], match['kick_off'], match['season']['season_id'],
        match['competition']['competition_id'], match['home_team']['home_team_id'],
        match['home_team']['managers'][0]['id'] if match['home_team']['managers'] else None, 
        match['away_team']['away_team_id'], 
        match['away_team']['managers'][0]['id'] if match['away_team']['managers'] else None, 
        match['home_score'], match['away_score'], match['match_week'],
        match['competition_stage']['id'], match['stadium']['id'], match['referee']['id']
    ))
    conn.commit()
    cursor.close()

def process_json_file(filepath):
    """Process a single JSON file to extract and insert data into the database."""
    conn = connect_to_db()
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for match in data:
                try:
                    insert_country(conn, match['home_team']['country']['id'], match['home_team']['country']['name'])
                    insert_country(conn, match['away_team']['country']['id'], match['away_team']['country']['name'])
                    insert_stadium(conn, match['stadium'])
                    insert_referee(conn, match['referee'])
                    insert_team(conn, match['home_team'])
                    insert_team(conn, match['away_team'])
                    insert_match(conn, match)
                except KeyError as e:
                    print(f"Key error processing match {match['match_id']}: {str(e)}")
                except Exception as e:
                    print(f"Error processing match {match['match_id']}: {str(e)}")
    except Exception as e:
        print(f"Error reading file {filepath}: {str(e)}")
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_json_file>")
        sys.exit(1)
    filepath = sys.argv[1]
    process_json_file(filepath)
