Table Seasons {
  season_id integer
  competition_id integer
  competition_name varchar(255)
  country_name varchar(255)
  competition_gender varchar(255)
  competition_youth boolean
  competition_international boolean
  season_name varchar(255)
  Indexes {
    (season_id, competition_id) [pk]
  }
}

Table Countries {
  country_id integer [pk]
  country_name varchar(255)
}

Table Managers {
  manager_id integer [pk]
  manager_name varchar(255)
  manager_nickname varchar(255)
  dob date
  country_id integer
}

Table Stadiums {
  stadium_id integer [pk]
  stadium_name varchar(255)
  country_id integer
}

Table Teams {
  team_id integer [pk]
  team_name varchar(255) [not null]
  manager_id integer
  home_stadium_id integer
  competition_id integer
  season_id integer
  team_gender varchar(255)
}

Table Positions {
  position_id integer [pk]
  position_name varchar(255)
}

Table Players {
  player_id integer [pk]
  player_name varchar(255) [not null]
  player_nickname varchar(255)
  jersey_number integer
  country_id integer
  team_id integer
  position_id integer
  num_matches_played integer
}

Table Matches {
  match_id integer [pk]
  match_date date
  kick_off time
  season_id integer
  competition_id integer
  home_team_id integer
  home_manager_id integer
  away_team_id integer
  away_manager_id integer
  home_score integer
  away_score integer
  match_week integer
  competition_stage_id integer
  stadium_id integer
  referee_id integer
}

Table Referees {
  referee_id integer [pk]
  referee_name varchar(255)
  country_id integer
}

Table Events {
  event_id varchar(255) [pk]
  match_id integer
  type varchar(255)
  period integer
  timestamp time
  minute integer
  second integer
  team_id integer
  player_id integer
  location_x decimal(5,2)
  location_y decimal(5,2)
}

Table Player_Statistics {
  stat_id serial [pk]
  shots integer
  passes integer
  goals integer
  assists integer
  dribbles integer
  tackles integer
  saves integer
  match_id integer
  player_id integer
  red_cards integer
  yellow_cards integer
}

Table Team_Statistics {
  team_stat_id serial [pk]
  team_id integer
  match_id integer
  possession_percentage decimal(5,2)
  passes_completed integer
  tackles integer
  shots_on_target integer
}

Table Substitutions {
  event_id varchar(255) [pk]
  player_out_id integer
  player_in_id integer
  reason varchar(255)
}

Table xGoals {
  player_id integer
  total_xg decimal(5,2) [pk]
}

Table Goals {
  event_id varchar(255) [pk]
  goal_type varchar(255)
  assist_event_id varchar(255)
  shot_id varchar(255)
}

Table Penalties {
  event_id varchar(255) [pk]
  goal_id varchar(255)
}

Table Free_Kick {
  event_id varchar(255) [pk]
  goal_id varchar(255)
  pass_id varchar(255)
  body_part varchar(255)
}

Table Corners {
  event_id varchar(255) [pk]
  technique varchar(255)
  body_part varchar(255)
  outcome varchar(255)
}

Table Goal_Kick {
  event_id varchar(255) [pk]
  pass_id varchar(255)
}

Table Saves {
  event_id varchar(255) [pk]
}

Table Tackles {
  event_id varchar(255) [pk]
  outcome boolean
}

Table Duels {
  event_id varchar(255) [pk]
  type varchar(255)
  outcome varchar(255)
  under_pressure boolean
}

Table Clearences {
  event_id varchar(255) [pk]
  under_pressure boolean
  body_part varchar(255)
  play_pattern varchar(255)
  is_out boolean
}

Table Interceptions {
  event_id varchar(255) [pk]
  outcome varchar(255)
  play_pattern varchar(255)
}

Table Passes {
  event_id varchar(255) [pk]
  pass_type varchar(255)
  successful boolean
  length decimal(5,2)
  angle decimal(5,2)
  height varchar(255)
  end_location_x decimal(5,2)
  end_location_y decimal(5,2)
  recipient_id integer
  body_part varchar(255)
}

Table Throw_Ins {
  event_id varchar(255) [pk]
}

Table Ball_Receipts {
  event_id varchar(255) [pk]
  pass_from_id varchar(255)
}

Table Cards {
  event_id varchar(255) [pk]
  card_type varchar(255)
}

Table Fouls {
  event_id varchar(255) [pk]
  foul_type varchar(255)
  player_fouling_id integer
}

Table Offsides {
  event_id varchar(255) [pk]
}

Table Shots {
  event_id varchar(255) [pk]
  outcome boolean
  first_time boolean
  shot_type varchar(255)
  body_part varchar(255)
  shot_location_x decimal(5,2)
  shot_location_y decimal(5,2)
}

Table Dribbles {
  event_id varchar(255) [pk]
  success boolean
}

Table Ball_Recovery {
  event_id varchar(255) [pk]
}

Table Carries {
  event_id varchar(255) [pk]
  end_location_x decimal(5,2)
  end_location_y decimal(5,2)
}

Table Injury_Stoppage {
  event_id varchar(255) [pk]
}

Table Pressure {
  event_id varchar(255) [pk]
}


Ref: Managers.country_id > Countries.country_id
Ref: Stadiums.country_id > Countries.country_id
Ref: Teams.manager_id > Managers.manager_id
Ref: Teams.home_stadium_id > Stadiums.stadium_id
Ref: Teams.(season_id, competition_id) > Seasons.(season_id, competition_id)
Ref: Players.position_id > Positions.position_id
Ref: Players.country_id > Countries.country_id
Ref: Players.team_id > Teams.team_id
Ref: Matches.(season_id, competition_id) > Seasons.(season_id, competition_id)
Ref: Matches.home_team_id > Teams.team_id
Ref: Matches.away_team_id > Teams.team_id
Ref: Referees.country_id > Countries.country_id
Ref: Events.match_id > Matches.match_id
Ref: Events.team_id > Teams.team_id
Ref: Events.player_id > Players.player_id
Ref: Player_Statistics.match_id > Matches.match_id
Ref: Player_Statistics.player_id > Players.player_id
Ref: Team_Statistics.team_id > Teams.team_id
Ref: Team_Statistics.match_id > Matches.match_id
Ref: Substitutions.event_id > Events.event_id
Ref: Substitutions.player_out_id > Players.player_id
Ref: Substitutions.player_in_id > Players.player_id
Ref: xGoals.player_id > Players.player_id
Ref: Goals.event_id > Events.event_id
Ref: Goals.assist_event_id > Events.event_id
Ref: Goals.shot_id > Events.event_id
Ref: Penalties.event_id > Events.event_id
Ref: Penalties.goal_id > Goals.event_id
Ref: Free_Kick.event_id > Events.event_id
Ref: Free_Kick.goal_id > Goals.event_id
Ref: Free_Kick.pass_id > Events.event_id
Ref: Corners.event_id > Events.event_id
Ref: Goal_Kick.event_id > Events.event_id
Ref: Goal_Kick.pass_id > Events.event_id
Ref: Saves.event_id > Events.event_id
Ref: Tackles.event_id > Events.event_id
Ref: Duels.event_id > Events.event_id
Ref: Clearences.event_id > Events.event_id
Ref: Interceptions.event_id > Events.event_id
Ref: Passes.event_id > Events.event_id
Ref: Passes.recipient_id > Players.player_id
Ref: Throw_Ins.event_id > Events.event_id
Ref: Ball_Receipts.event_id > Events.event_id
Ref: Ball_Receipts.pass_from_id > Events.event_id
Ref: Cards.event_id > Events.event_id
Ref: Fouls.event_id > Events.event_id
Ref: Fouls.player_fouling_id > Players.player_id
Ref: Offsides.event_id > Events.event_id
Ref: Shots.event_id > Events.event_id
Ref: Dribbles.event_id > Events.event_id
Ref: Ball_Recovery.event_id > Events.event_id
Ref: Carries.event_id > Events.event_id
Ref: Injury_Stoppage.event_id > Events.event_id
Ref: Pressure.event_id > Events.event_id
