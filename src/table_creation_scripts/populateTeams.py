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

def insert_team(conn, team):
    """Insert a team into the Teams table."""
    cursor = conn.cursor()
    sql = """
    INSERT INTO Teams(team_id, team_name, manager_id, home_stadium_id, competition_id, season_id, team_gender)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (team_id) DO NOTHING;
    """
    try:
        cursor.execute(sql, (
            team['team_id'],
            team['team_name'],
            team.get('manager_id'),  # Assuming manager_id could be present in the data
            team.get('home_stadium_id'),  # Assuming stadium_id could be present in the data
            team['competition_id'],
            team['season_id'],
            team['team_gender']
        ))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error inserting team {team['team_name']}: {str(error)}")
    cursor.close()

def process_json_file(filepath):
    """Process a single JSON file to extract and insert data into the database."""
    conn = connect_to_db()
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            teams = {}
            for match in data:
                season_id = match['season']['season_id']
                competition_id = match['competition']['competition_id']
                for side in ['home_team', 'away_team']:
                    team = match[side]
                    team_id = team[f'{side}_id']
                    if team_id not in teams:  # Check if team is already processed
                        teams[team_id] = {
                            'team_id': team_id,
                            'team_name': team[f'{side}_name'],
                            'team_gender': team[f'{side}_gender'],
                            'manager_id': None,  # Add logic to extract manager_id if available
                            'home_stadium_id': match.get('stadium', {}).get('id'),  # Extract stadium_id if available
                            'competition_id': competition_id,
                            'season_id': season_id
                        }
                        insert_team(conn, teams[team_id])
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
