CREATE TABLE Teams (
    team_id INTEGER PRIMARY KEY,
    team_name VAR_CHAR(255) NOT NULL
);


CREATE TABLE Matches (
    match_id INTEGER PRIMARY KEY,
    match_date DATE,
    kick_off TIME,
    competition_id INTEGER,
    season_id INTEGER,
    home_team_id INTEGER,
    away_team_id INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    match_week INTEGER,
    competition_stage_id INTEGER,
    stadium_id INTEGER,
    referee_id INTEGER,
    FOREIGN KEY (competition_id, season_id) REFERENCES Competitions(competition_id, season_id),
    FOREIGN KEY (home_team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES Teams(team_id)
);



CREATE TABLE Players (
    player_id INTEGER PRIMARY KEY,
    player_name VARCHAR(255) NOT NULL,
    player_nickname VARCHAR(255), 
    team_id INTEGER,
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
);


CREATE TABLE Competitions (
    compeition_id  INTEGER,
    season_id INTEGER,
    country_name VARCHAR(255),
    competition_name VARCHAR(255),
    competition_gender VARCHAR(255),
    competition_youth BOOLEAN,
    competition_international BOOLEAN,
    season_name VARCHAR(255),
    PRIMARY KEY (competition_id, season_id)
);


CREATE TABLE Team_Statistics (
    team_stat_id SERIAL PRIMARY KEY,
    match_id INTEGER,
    team_id INTEGER,
    passes INTEGER,
    through_balls INTEGER,
    shots INTEGER,
    FOREIGN KEY (match_id) REFERENCES Matches(match_id),
    FOREIGN KEY (team_Id) REFERENCES Teams(team_id)
);


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