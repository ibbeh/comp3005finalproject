CREATE TABLE teams {
    team_id INT PRIMARY KEY,
    team_name VAR_CHAR(255) NOT NULL
}

CREATE TABLE matches {
    match_id INT PRIMARY KEY,
    competition_id INT,
    season_id INT,
    home_team_id INT,
    away_team_id INT,
    FOREIGN KEY (competition_id, season_id) REFERENCES competitions(competition_id, season_id),
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id)
}

CREATE TABLE players {
    player_id INT PRIMARY KEY,
    player_name VARCHAR(255) NOT NULL,
    player_nickname VARCHAR(255), 
    team_id INT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
}