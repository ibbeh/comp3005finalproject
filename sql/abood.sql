CREATE TABLE Player_Statistics (
    player_stat_id SERIAL PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    shots INTEGER,
    first_time_shots INTEGER,
    through_balls INTEGER,
    successful_dribbles INTEGER,
    dribbled_past INTEGER,
    intended_recipient_of_passes INTEGER,
    average_xg numeric(5,2),
    FOREIGN KEY (match_id) REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
);