--FINISHED
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


--FINISHED
CREATE TABLE Seasons (
    season_id SERIAL PRIMARY KEY,
    season_name VARCHAR(255),
    start_date DATE,
    end_date DATE,
    competition_id INTEGER,
    FOREIGN KEY competition_id REFERENCES Competitions(competition_id)
);


--FINISHED
CREATE TABLE Teams (
    team_id INTEGER PRIMARY KEY,
    team_name VARCHAR(255) NOT NULL
    manager_id INTEGER 
    home_stadium_id INTEGER
    competition_id INTEGER
    team_gender VARCHAR(255),
    FOREIGN KEY (manager_id) REFERENCES Manager(manager_id)
    FOREIGN KEY (home_stadium_id) REFERENCES Stadium(home_stadium_id)
    FOREIGN KEY (competition_id) REFERENCES Competitions(competition_id)
);


--FINISHED
CREATE TABLE Players (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(255) NOT NULL,
    player_nickname VARCHAR(255),
    jersey_number INTEGER,
    country_id INTEGER
    team_id INTEGER,
    position_id INTEGER,
    FOREIGN KEY (position_id) REFERENCES Positions(position_id)
    FOREIGN KEY (country_id) REFERENCES Countries(country_id)
    FOREIGN KEY (team_id)  REFERENCES Teams(team_id)
);


--FINISHED
CREATE TABLE Matches (
    match_id INTEGER PRIMARY KEY,
    match_date DATE,
    kick_off TIME,
    competition_id INTEGER,
    season_id INTEGER,
    home_team_id INTEGER,
    home_manager_id INTEGER,
    away_team_id INTEGER,
    away_manager_id INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    match_week INTEGER,
    competition_stage_id INTEGER,
    stadium_id INTEGER,
    stadium_name VARCHAR(255),
    referee_id INTEGER,
    FOREIGN KEY (competition_id, season_id) REFERENCES Competitions(competition_id, season_id),
    FOREIGN KEY (home_team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES Teams(team_id)

);

--FINISHED
CREATE TABLE Referees (
    referee_id INT PRIMARY KEY,
    referee_name VARCHAR(255),
    country_id INTEGER,
    FOREIGN KEY (country_id) REFERENCES Countries(country_id)
);

--FINISHED
CREATE TABLE Stadiums (
    stadium_id INT PRIMARY KEY,
    stadium_name VARCHAR(255),
    country_id INTEGER,
    FOREIGN KEY (country_id) REFERENCES Countries(country_id)
);

--FINISHED
CREATE TABLE Managers (
    manager_id INT PRIMARY KEY,
    manager_name VARCHAR(255)
    manager_nickname VARCHAR(255),
    dob DATE,
    country_id INTEGER,
    FOREIGN KEY (country_id) REFERENCES Countries(country_id)
);

--FINISHED
CREATE TABLE Positions (
    position_id INTEGER PRIMARY KEY,
    position_name VARCHAR(255),
);


CREATE TABLE Player_Statistics (
    stat_id SERIAL PRIMARY KEY,
    shots INTEGER,
    passes INTEGER,
    goals INTEGER,
    assists INTEGER,
    dribbles INTEGER,
    tackles INTEGER,
    saves INTEGER,
    red_cards INTEGER,
    yellow_cards INTEGER
    FOREIGN KEY (match_id) REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
);

CREATE TABLE Team_Statistics (
    team_stat_id SERIAL PRIMARY KEY,
    possession_percentage DECIMAL(5,2),
    passes_completed INTEGER,
    tackles INTEGER,
    shots_on_target INTEGER
    FOREIGN KEY (team_id) INTEGER REFERENCES Teams(team_id),
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
);


CREATE TABLE Substitutions (
    substitution_id SERIAL PRIMARY KEY,
    substitution_minute INTEGER,
    substitutiton_period INTEGER,
    substitution_reason VARCHAR(255),
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
    FOREIGN KEY (player_in_id) INTEGER REFERENCES Players(player_id),
    FOREIGN KEY (player_out_id) INTEGER REFERENCES Players(player_id),
);

CREATE TABLE xGoals (
    total_xg INTEGER PRIMARY KEY,
    matches_played INTEGER,
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
);

CREATE TABLE Goals (
    goal_id SERIAL PRIMARY KEY,
    goal_minute INTEGER,
    goal_type VARCHAR(255)
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
    FOREIGN KEY (assist_player_id) INTEGER REFERENCES Players(player_id),
);

CREATE TABLE Penalties (
    penalty_id SERIAL PRIMARY KEY,
    is_scored BOOLEAN
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
    FOREIGN KEY (goal_id) INTEGER REFERENCES Goals(goal_id),
);

CREATE TABLE Saves (
    save_id SERIAL PRIMARY KEY,
    save_minute INTEGER
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
);

CREATE TABLE Tackles (
    tackle_id SERIAL PRIMARY KEY,
    tackle_minute INTEGER,
    success BOOLEAN
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
);

CREATE TABLE Passes (
    pass_id SERIAL PRIMARY KEY,
    pass_type VARCHAR(255),
    successful BOOLEAN
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
);

CREATE TABLE Throw_Ins (
    throw_in_id SERIAL PRIMARY KEY,
    throw_in_minute INTEGER
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
);

CREATE TABLE Ball_Receipts (
    receipt_id SERIAL PRIMARY KEY,
    receipt_minute INTEGER
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
);

CREATE TABLE Cards (
    card_id SERIAL PRIMARY KEY,
    card_type VARCHAR(255),
    card_minute INTEGER
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
);

CREATE TABLE Fouls (
    foul_id SERIAL PRIMARY KEY,
    foul_minute INTEGER
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
);

CREATE TABLE Offsides (
    offside_id SERIAL PRIMARY KEY,
    offside_minute INTEGER
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
);

CREATE TABLE Shots (
    shot_id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES Matches(match_id),
    player_id INTEGER REFERENCES Players(player_id),
    shot_minute INTEGER,
    on_target BOOLEAN
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
);

CREATE TABLE Dribbles (
    dribble_id SERIAL PRIMARY KEY,
    dribble_minute INTEGER,
    success BOOLEAN
    FOREIGN KEY (match_id) INTEGER REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
);