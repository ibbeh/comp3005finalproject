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
    try:
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
    except KeyError as e:
        print(f"Missing key {e} in match data with ID {match['match_id']}. Skipping this match.")
    cursor.close()

def process_json_file(filepath):
    """Process a single JSON file to extract and insert data into the database."""
    conn = connect_to_db()
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for match in data:
                insert_match(conn, match)
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
