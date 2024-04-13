--FINISHED
CREATE TABLE Competitions (
    competition_id  INTEGER,
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
    season_id INTEGER PRIMARY KEY,
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

--PENDING APPROVAL
CREATE TABLE Substitutions (
    event_id INTEGER PRIMARY KEY,
    player_out_id INTEGER,
    player_in_id INTEGER,
    reason VARCHAR(255),
    FOREIGN KEY (event_id) REFERENCES Events(event_id),
    FOREIGN KEY (player_out_id) REFERENCES Players(player_id),
    FOREIGN KEY (player_in_id) REFERENCES Players(player_id)
);

CREATE TABLE xGoals (
    total_xg DECIMAL(5,2) PRIMARY KEY,
    matches_played INTEGER,
    FOREIGN KEY (player_id) INTEGER REFERENCES Players(player_id),
);

--PENDING APPROVAL
CREATE TABLE Goals (
    event_id INTEGER PRIMARY KEY,
    goal_type VARCHAR(255),
    assist_event_id INTEGER,
    shot_id INTEGER,
    FOREIGN KEY (event_id) REFERENCES Events(event_id),
    FOREIGN KEY (assist_event_id) REFERENCES Events(event_id),
    FOREIGN KEY (shot_id) REFERENCES Events(event_id)
);

--PENDING APPROVAL
CREATE TABLE Penalties (
    event_id INTEGER PRIMARY KEY,
    is_scored BOOLEAN,
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);


--PENDING APPROVAL
CREATE TABLE Saves (
    event_id INTEGER PRIMARY KEY,
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);


--PENDING APPROVAL
CREATE TABLE Tackles (
    event_id INTEGER PRIMARY KEY,
    outcome BOOLEAN,
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);

--PENDING APPROVAL
CREATE TABLE Passes (
    event_id INTEGER PRIMARY KEY,
    pass_type VARCHAR(255),
    successful BOOLEAN,
    length DECIMAL(5,2),
    angle DECIMAL(5,2),
    height VARCHAR(255),
    end_location_x DECIMAL(5,2),
    end_location_y DECIMAL(5,2),
    recipient_id INTEGER,
    FOREIGN KEY (event_id) REFERENCES Events(event_id),
    FOREIGN KEY (recipient_id) REFERENCES Players(player_id)
);


--PENDING APPROVAL
CREATE TABLE Throw_Ins (
    event_id INTEGER PRIMARY KEY,
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);


--PENDING APPROVAL
CREATE TABLE Ball_Receipts (
    event_id INTEGER PRIMARY KEY,
    pass_from_id INTEGER,
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
    FOREIGN KEY (pass_from_id) REFERENCES Events(event_id)
);

--PENDING APPROVAL
CREATE TABLE Cards (
    event_id INTEGER PRIMARY KEY,
    card_type VARCHAR(255),
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);

--PENDING APPROVAL
CREATE TABLE Fouls (
    event_id INTEGER PRIMARY KEY,
    foul_type VARCHAR(255),
    player_fouled_id INTEGER,
    player_fouling_id INTEGER,
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
    FOREIGN KEY (player_fouled_id) REFERENCES Players(player_id)
    FOREIGN KEY (player_fouling_id) REFERENCES Players(player_id)
);

--PENDING APPROVAL
CREATE TABLE Offsides (
    event_id INTEGER PRIMARY KEY,
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);


--PENDING APPROVAL
CREATE TABLE Shots (
    event_id INTEGER PRIMARY KEY,
    outcome BOOLEAN,
    first_time BOOLEAN,
    shot_type VARCHAR(255),
    body_part VARCHAR(255),
    shot_location_x DECIMAL(5,2) 
    shot_location_y DECIMAL(5,2)
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);


--PENDING APPROVAL
CREATE TABLE Dribbles (
    event_id INTEGER PRIMARY KEY,
    success BOOLEAN,
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);


--PENDING APPROVAL
CREATE TABLE Events (
    event_id SERIAL PRIMARY KEY,
    match_id INTEGER,
    type VARCHAR(255),
    period INTEGER,
    timestamp TIME,
    minute INTEGER,
    second INTEGER,
    team_id INTEGER,
    player_id INTEGER,
    location_x DECIMAL(5,2),
    location_y DECIMAL(5,2),
    FOREIGN KEY (match_id) REFERENCES Matches(match_id),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id)
);


--PENDING APPROVAL
CREATE TABLE Ball_Recovery (
    event_id INTEGER PRIMARY KEY,
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);


--PENDING APPROVAL
CREATE TABLE Carries (
    event_id INTEGER PRIMARY KEY,
    end_location_x DECIMAL(5,2),
    end_location_y DECIMAL(5,2),
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);