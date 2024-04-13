import json
import psycopg2
import sys

def connect_to_db():
    """Connect to the PostgreSQL database server."""
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            dbname="your_dbname",
            user="your_username",
            password="your_password",
            host="your_host",
            port="your_port"
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 
    print("Connection successful.")
    return conn

def insert_manager(conn, manager):
    """Insert a manager into the Managers table."""
    cursor = conn.cursor()
    sql = """
    INSERT INTO Managers(manager_id, manager_name, manager_nickname, dob, country_id) 
    VALUES (%s, %s, %s, %s, %s) ON CONFLICT (manager_id) DO NOTHING;
    """
    cursor.execute(sql, (manager['id'], manager['name'], manager['nickname'], manager['dob'], manager['country']['id']))
    conn.commit()
    cursor.close()

def insert_team(conn, team):
    """Insert a team into the Teams table, including their manager."""
    cursor = conn.cursor()
    # Insert manager(s) for the team
    for manager in team['managers']:
        insert_manager(conn, manager)
    # Insert the team
    sql = """
    INSERT INTO Teams(team_id, team_name, manager_id, home_stadium_id, competition_id, season_id, team_gender) 
    VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (team_id) DO NOTHING;
    """
    cursor.execute(sql, (team['home_team_id'], team['home_team_name'], team['managers'][0]['id'], None, None, None, team['home_team_gender']))
    conn.commit()
    cursor.close()

def insert_stadium(conn, stadium):
    """Insert a stadium into the Stadiums table."""
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
        match['home_team']['managers'][0]['id'], match['away_team']['away_team_id'], 
        match['away_team']['managers'][0]['id'], match['home_score'], match['away_score'], 
        match['match_week'], match['competition_stage']['id'], match['stadium']['id'], 
        match['referee']['id']
    ))
    conn.commit()
    cursor.close()

def process_json_file(filepath):
    """Process a single JSON file to extract and insert data into the database."""
    conn = connect_to_db()
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            for match in data:
                insert_stadium(conn, match['stadium'])
                insert_referee(conn, match['referee'])
                insert_team(conn, match['home_team'])
                insert_team(conn, match['away_team'])
                insert_match(conn, match)
    except Exception as e:
        print("Error processing file:", e)
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
