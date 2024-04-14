import os
import json
import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname="FUTSTATS",
        user="postgres",
        password="Kuwait$22",
        host="localhost",
        port="5432"
    )

def parse_substitutions(data):
    for event in data:
        if event['type']['name'] == 'Substitution':
            yield {
                'event_id': event['id'],
                'player_out_id': event['player']['id'],
                'player_in_id': event.get('substitution', {}).get('replacement', {}).get('id', None),
                'reason': event.get('substitution', {}).get('outcome', {}).get('name', None),
                'competition_id': event.get('competition_id', None),
                'season_id': event.get('season_id', None)
            }

def parse_shots(data):
    for event in data:
        if event['type']['name'] == 'Shot':
            yield {
                'event_id': event['id'],
                'outcome': event['shot']['outcome']['name'],
                'first_time': event.get('shot', {}).get('first_time', False),
                'shot_type': event['shot']['type']['name'],
                'body_part': event['shot']['body_part']['name'],
                'shot_location_x': event['location'][0],
                'shot_location_y': event['location'][1]
            }

def parse_passes(data):
    for event in data:
        if event['type']['name'] == 'Pass':
            yield {
                'event_id': event['id'],
                'pass_type': event['pass']['type']['name'],
                'pass_technique': event['pass'].get('technique', {}).get('name', 'Standard'),
                'successful': event['pass'].get('outcome', {}).get('name', 'Complete') == 'Complete',
                'length': event['pass']['length'],
                'angle': event['pass']['angle'],
                'height': event['pass']['height']['name'],
                'end_location_x': event['pass']['end_location'][0],
                'end_location_y': event['pass']['end_location'][1],
                'recipient_id': event['pass']['recipient']['id'],
                'body_part': event['pass']['body_part']['name']
            }

def insert_data(cursor, table, data):
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, list(data.values()))

def process_files(directory):
    conn = connect_db()
    cursor = conn.cursor()

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)

            for substitution in parse_substitutions(data):
                insert_data(cursor, 'Substitutions', substitution)
            for shot in parse_shots(data):
                insert_data(cursor, 'Shots', shot)
            for pass_event in parse_passes(data):
                insert_data(cursor, 'Passes', pass_event)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    directory = "../../data/events"
    process_files(directory)
