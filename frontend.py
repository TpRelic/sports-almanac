# Query nba.live.endpoints for the score board of GameID 0022000180 = NYK vs BOS
# Simple PlayByPlay Loop demonstrating data usage
from nba_api.live.nba.endpoints import playbyplay
from nba_api.stats.static import players
pbp = playbyplay.PlayByPlay('0022000196')
line = "{action_number}: {period}:{clock} {player_id} ({action_type})"
actions = pbp.get_dict()['game']['actions'] #plays are referred to in the live data as `actions`
for action in actions:
    player_name = ''
    player = players.find_player_by_id(action['personId'])
    if player is not None:
        player_name = player['full_name']
    print(line.format(action_number=action['actionNumber'],period=action['period'],clock=action['clock'],action_type=action['actionType'],player_id=player_name))


from nba_api.live.nba.endpoints import boxscore

# Initialize the BoxScore object with the Game ID
box = boxscore.BoxScore('0022000196') 

# Get the away team dictionary
away_team_dict = box.away_team.get_dict()

# Print the away team dictionary
print("Away Team Dictionary:")
print(away_team_dict)        #equal to box.get_dict()['game']['awayTeam']
#box.away_team_player_stats.get_dict() #equal to box.get_dict()['game']['awayTeam']['players']
#box.away_team_stats.get_dict()        #equal to box.get_dict()['game']['homeTeam'] w/o ['players']
#box.home_team.get_dict()              #equal to box.get_dict()['game']['homeTeam']
#box.home_team_player_stats.get_dict() #equal to box.get_dict()['game']['homeTeam']['players']
#box.home_team_stats.get_dict()        #equal to box.get_dict()['game']['homeTeam'] w/o ['players']
#box.game_details.get_dict()           #equal to box.get_dict()['game'] scrubbed of all other dictionaries
#box.officials.get_dict()              #equal to box.get_dict()['game']['officials']
