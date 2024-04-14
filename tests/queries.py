# Created by Gabriel Martell

'''
Version 1.2 (04/13/2024)
=========================================================
queries.py (Carleton University COMP3005 - Database Management Student Template Code)

This is the template code for the COMP3005 Database Project 1, and must be accomplished on an Ubuntu Linux environment.
Your task is to ONLY write your SQL queries within the prompted space within each Q_# method (where # is the question number).

You may modify code in terms of testing purposes (commenting out a Qn method), however, any alterations to the code, such as modifying the time, 
will be flagged for suspicion of cheating - and thus will be reviewed by the staff and, if need be, the Dean. 

To review the Integrity Violation Attributes of Carleton University, please view https://carleton.ca/registrar/academic-integrity/ 

=========================================================
'''

# Imports
import psycopg
import csv
import subprocess
import os
import re

# Connection Information
''' 
The following is the connection information for this project. These settings are used to connect this file to the autograder.
You must NOT change these settings - by default, db_host, db_port and db_username are as follows when first installing and utilizing psql.
For the user "postgres", you must MANUALLY set the password to 1234.

This can be done with the following snippet:

sudo -u postgres psql
\password postgres

'''
root_database_name = "project_database"
query_database_name = "query_database"
db_username = 'postgres'
db_password = '1234'
db_host = 'localhost'
db_port = '5432'

# Directory Path - Do NOT Modify
dir_path = os.path.dirname(os.path.realpath(__file__))

# Loading the Database after Drop - Do NOT Modify
#================================================
def load_database(conn):
    drop_database(conn)

    cursor = conn.cursor()
    # Create the Database if it DNE
    try:
        conn.autocommit = True
        cursor.execute(f"CREATE DATABASE {query_database_name};")
        conn.commit()

    except Exception as error:
        print(error)

    finally:
        cursor.close()
        conn.autocommit = False
    conn.close()
    
    # Connect to this query database.
    dbname = query_database_name
    user = db_username
    password = db_password
    host = db_host
    port = db_port
    conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    # Import the dbexport.sql database data into this database
    try:
        command = f'psql -h {host} -U {user} -d {query_database_name} -a -f "{os.path.join(dir_path, "dbexport.sql")}" > /dev/null 2>&1'
        env = {'PGPASSWORD': password}
        subprocess.run(command, shell=True, check=True, env=env)

    except Exception as error:
        print(f"An error occurred while loading the database: {error}")
    
    # Return this connection.
    return conn    

# Dropping the Database after Query n Execution - Do NOT Modify
#================================================
def drop_database(conn):
    # Drop database if it exists.

    cursor = conn.cursor()

    try:
        conn.autocommit = True
        cursor.execute(f"DROP DATABASE IF EXISTS {query_database_name};")
        conn.commit()

    except Exception as error:
        print(error)
        pass

    finally:
        cursor.close()
        conn.autocommit = False

# Reconnect to Root Database - Do NOT Modify
#================================================
def reconnect():
    dbname = root_database_name
    user = db_username
    password = db_password
    host = db_host
    port = db_port
    return psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Getting the execution time of the query through EXPLAIN ANALYZE - Do NOT Modify
#================================================
def get_time(cursor, sql_query):
    # Prefix your query with EXPLAIN ANALYZE
    explain_query = f"EXPLAIN ANALYZE {sql_query}"

    try:
        # Execute the EXPLAIN ANALYZE query
        cursor.execute(explain_query)
        
        # Fetch all rows from the cursor
        explain_output = cursor.fetchall()
        
        # Convert the output tuples to a single string
        explain_text = "\n".join([row[0] for row in explain_output])
        
        # Use regular expression to find the execution time
        # Look for the pattern "Execution Time: <time> ms"
        match = re.search(r"Execution Time: ([\d.]+) ms", explain_text)
        if match:
            execution_time = float(match.group(1))
            return f"Execution Time: {execution_time} ms"
        else:
            print("Execution Time not found in EXPLAIN ANALYZE output.")
            return f"NA"
        
    except Exception as error:
        print(f"[ERROR] Error getting time.\n{error}")


# Write the results into some Q_n CSV. If the is an error with the query, it is a INC result - Do NOT Modify
#================================================
def write_csv(execution_time, cursor, i):
    # Collect all data into this csv, if there is an error from the query execution, the resulting time is INC.
    try:
        colnames = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        filename = f"{dir_path}/Q_{i}.csv"

        with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            
            # Write column names to the CSV file
            csvwriter.writerow(colnames)
            
            # Write data rows to the CSV file
            csvwriter.writerows(rows)

    except Exception as error:
        execution_time[i-1] = "INC"
        print(error)
    
#================================================
        
'''
The following 10 methods, (Q_n(), where 1 < n < 10) will be where you are tasked to input your queries.
To reiterate, any modification outside of the query line will be flagged, and then marked as potential cheating.
Once you run this script, these 10 methods will run and print the times in order from top to bottom, Q1 to Q10 in the terminal window.
'''
def Q_1(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """
    SELECT
    P.player_name,
    COALESCE(P.player_nickname, 'No Nickname') AS player_nickname,  -- Handles any NULL nicknames
    ROUND((X.total_xg / P.num_matches_played)::numeric, 2) AS avg_xg  -- Casts the division result to numeric and rounds it to 2 decimal places
FROM
    Players P
JOIN
    xGoals X ON P.player_id = X.player_id AND P.season_id = X.season_id AND P.competition_id = X.competition_id
JOIN
    Seasons S ON P.season_id = S.season_id AND P.competition_id = S.competition_id
WHERE
    S.competition_name = 'La Liga' AND
    S.season_name = '2020/2021' AND
    X.total_xg > 0
ORDER BY
    avg_xg DESC;

    """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[0] = (time_val)

    write_csv(execution_time, cursor, 1)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_2(conn, execution_time):

    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """ SELECT
    P.player_name,
    COUNT(S.event_id) AS total_shots
FROM
    Players P
JOIN
    Events E ON P.player_id = E.player_id AND P.season_id = E.season_id AND P.competition_id = E.competition_id
JOIN
    Shots S ON E.event_id = S.event_id
JOIN
    Seasons SE ON SE.season_id = P.season_id AND SE.competition_id = P.competition_id
WHERE
    SE.competition_name = 'La Liga' AND
    SE.season_name = '2020/2021'
GROUP BY
    P.player_name
HAVING
    COUNT(S.event_id) > 0
ORDER BY
    total_shots DESC;
 """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[1] = (time_val)

    write_csv(execution_time, cursor, 2)

    cursor.close()
    new_conn.close()

    return reconnect()
    
def Q_3(conn, execution_time):

    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """ SELECT
    P.player_name,
    COUNT(S.event_id) AS total_first_time_shots
FROM
    Players P
JOIN
    Events E ON P.player_id = E.player_id
JOIN
    Shots S ON E.event_id = S.event_id AND S.first_time = TRUE
JOIN
    Seasons SE ON E.season_id = SE.season_id AND E.competition_id = SE.competition_id
WHERE
    SE.competition_name = 'La Liga' AND
    SE.season_name IN ('2020/2021', '2019/2020', '2018/2019')
GROUP BY
    P.player_name
HAVING
    COUNT(S.event_id) > 0
ORDER BY
    total_first_time_shots DESC;
 """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[2] = (time_val)

    write_csv(execution_time, cursor, 3)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_4(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """ SELECT
    T.team_name,
    COUNT(P.event_id) AS total_passes
FROM
    Teams T
JOIN
    Events E ON T.team_id = E.team_id AND T.season_id = E.season_id AND T.competition_id = E.competition_id
JOIN
    Passes P ON E.event_id = P.event_id
JOIN
    Seasons S ON T.season_id = S.season_id AND T.competition_id = S.competition_id
WHERE
    S.competition_name = 'La Liga' AND
    S.season_name = '2020/2021'
GROUP BY
    T.team_name
HAVING
    COUNT(P.event_id) > 0
ORDER BY
    total_passes DESC;
 """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[3] = (time_val)

    write_csv(execution_time, cursor, 4)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_5(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """ 
SELECT
    P.player_name,
    COUNT(PA.recipient_id) AS recipient_count
FROM
    Players P
JOIN
    Events E ON P.player_id = E.player_id AND P.season_id = E.season_id AND P.competition_id = E.competition_id
JOIN
    Passes PA ON E.event_id = PA.event_id AND PA.recipient_id = P.player_id
JOIN
    Seasons S ON P.season_id = S.season_id AND P.competition_id = S.competition_id
WHERE
    S.competition_name = 'Premier League' AND
    S.season_name = '2003/2004'
GROUP BY
    P.player_name
HAVING
    COUNT(PA.recipient_id) > 0
ORDER BY
    recipient_count DESC;
 """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[4] = (time_val)

    write_csv(execution_time, cursor, 5)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_6(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """
SELECT
    T.team_name,
    COUNT(S.event_id) AS total_shots
FROM
    Teams T
JOIN
    Events E ON T.team_id = E.team_id
JOIN
    Shots S ON E.event_id = S.event_id
JOIN
    Seasons SE ON T.season_id = SE.season_id AND T.competition_id = SE.competition_id
WHERE
    SE.competition_name = 'Premier League' AND
    SE.season_name = '2003/2004'
GROUP BY
    T.team_name
HAVING
    COUNT(S.event_id) > 0
ORDER BY
    total_shots DESC;
 """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[5] = (time_val)

    write_csv(execution_time, cursor, 6)

    cursor.close()
    new_conn.close()

    return reconnect()


def Q_7(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """ 
SELECT
    P.player_name,
    COUNT(PA.event_id) AS total_through_balls
FROM
    Players P
JOIN
    Events E ON P.player_id = E.player_id
JOIN
    Passes PA ON E.event_id = PA.event_id AND PA.pass_type = 'Through'
JOIN
    Seasons S ON P.season_id = S.season_id AND P.competition_id = S.competition_id
WHERE
    S.competition_name = 'La Liga' AND
    S.season_name = '2020/2021'
GROUP BY
    P.player_name
HAVING
    COUNT(PA.event_id) > 0
ORDER BY
    total_through_balls DESC;
"""

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[6] = (time_val)

    write_csv(execution_time, cursor, 7)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_8(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """ 
SELECT
    T.team_name,
    COUNT(P.event_id) AS total_through_balls
FROM
    Teams T
JOIN
    Events E ON T.team_id = E.team_id
JOIN
    Passes P ON E.event_id = P.event_id AND P.pass_type = 'Through'
JOIN
    Seasons S ON T.season_id = S.season_id AND T.competition_id = S.competition_id
WHERE
    S.competition_name = 'La Liga' AND
    S.season_name = '2020/2021'
GROUP BY
    T.team_name
HAVING
    COUNT(P.event_id) > 0
ORDER BY
    total_through_balls DESC;
"""

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[7] = (time_val)

    write_csv(execution_time, cursor, 8)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_9(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """
SELECT
    P.player_name,
    COUNT(D.event_id) AS total_successful_dribbles
FROM
    Players P
JOIN
    Events E ON P.player_id = E.player_id AND P.season_id = E.season_id AND P.competition_id = E.competition_id
JOIN
    Dribbles D ON E.event_id = D.event_id AND D.success = TRUE
JOIN
    Seasons S ON P.season_id = S.season_id AND P.competition_id = S.competition_id
WHERE
    S.competition_name = 'La Liga' AND
    S.season_name IN ('2020/2021', '2019/2020', '2018/2019')
GROUP BY
    P.player_name
HAVING
    COUNT(D.event_id) > 0
ORDER BY
    total_successful_dribbles DESC;
 """

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[8] = (time_val)

    write_csv(execution_time, cursor, 9)

    cursor.close()
    new_conn.close()

    return reconnect()

def Q_10(conn, execution_time):
    new_conn = load_database(conn)
    cursor = new_conn.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    query = """ 
SELECT
    P.player_name,
    COUNT(DP.event_id) AS times_dribbled_past
FROM
    Players P
JOIN
    Events E ON P.player_id = E.player_id
JOIN
    Dribbled_Past DP ON E.event_id = DP.event_id
JOIN
    Seasons S ON P.season_id = S.season_id AND P.competition_id = S.competition_id
WHERE
    S.competition_name = 'La Liga' AND
    S.season_name = '2020/2021'
GROUP BY
    P.player_name
HAVING
    COUNT(DP.event_id) > 0
ORDER BY
    times_dribbled_past ASC;
"""

    #==========================================================================

    time_val = get_time(cursor, query)
    cursor.execute(query)
    execution_time[9] = (time_val)

    write_csv(execution_time, cursor, 10)

    cursor.close()
    new_conn.close()

    return reconnect()

# Running the queries from the Q_n methods - Do NOT Modify
#=====================================================
def run_queries(conn):

    execution_time = [0,0,0,0,0,0,0,0,0,0]

    conn = Q_1(conn, execution_time)
    conn = Q_2(conn, execution_time)
    conn = Q_3(conn, execution_time)
    conn = Q_4(conn, execution_time)
    conn = Q_5(conn, execution_time)
    conn = Q_6(conn, execution_time)
    conn = Q_7(conn, execution_time)
    conn = Q_8(conn, execution_time)
    conn = Q_9(conn, execution_time)
    conn = Q_10(conn, execution_time)

    for i in range(10):
        print(execution_time[i])

''' MAIN '''
try:
    if __name__ == "__main__":

        dbname = root_database_name
        user = db_username
        password = db_password
        host = db_host
        port = db_port

        conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        
        run_queries(conn)
except Exception as error:
    print(error)
    #print("[ERROR]: Failure to connect to database.")
#_______________________________________________________