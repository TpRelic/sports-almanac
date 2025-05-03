import sys
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players

player = sys.argv[1]
player_info = players.find_players_by_full_name(player)
id = player_info[0]['id']

common_info = commonplayerinfo.CommonPlayerInfo(player_id=id)

df_common_info = common_info.get_data_frames()[0]
df_common_info = df_common_info.rename(columns={'DISPLAY_FIRST_LAST': 'NAME'})

career_stats = playercareerstats.PlayerCareerStats(player_id=id) 

df_career_stats = career_stats.get_data_frames()[0]
df_career_stats = df_career_stats.rename(columns={'TEAM_ABBREVIATION': 'TEAM'})
df_career_stats = df_career_stats.rename(columns={'PLAYER_AGE': 'AGE'})
df_career_stats = df_career_stats.rename(columns={'SEASON_ID': 'SEASON'})

print(df_common_info[['NAME', 'COUNTRY', 'HEIGHT', 'WEIGHT', 'JERSEY', 'POSITION', 'FROM_YEAR', 'TO_YEAR']].to_html(index=False))
print(df_career_stats[['SEASON', 'TEAM', 'AGE', 'GP', 'GS', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']].to_html(index=False))
