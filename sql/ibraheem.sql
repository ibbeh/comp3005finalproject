CREATE TABLE Competitions (
    compeition_id  INTEGER,
    season_id INTEGER,
    competition_name VARCHAR(255),
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