import sys
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players

player = sys.argv[1]
player_info = players.find_players_by_full_name(player)

if len(player_info) != 1:
    print(f"<p class=\"error_label\">No player by the name of {sys.argv[1]}...<br>Make sure to enter their full name, first and last!</p>")
    exit()

id = player_info[0]['id']
    
common_info = commonplayerinfo.CommonPlayerInfo(player_id=id)

df_common_info = common_info.get_data_frames()[0]
df_common_info = df_common_info.rename(columns={'DISPLAY_FIRST_LAST': 'NAME'})

career_stats = playercareerstats.PlayerCareerStats(player_id=id) 

df_career_stats = career_stats.get_data_frames()[0]
df_career_stats = df_career_stats.fillna('')
df_career_stats = df_career_stats.rename(columns={'TEAM_ABBREVIATION': 'TEAM'})
df_career_stats = df_career_stats.rename(columns={'PLAYER_AGE': 'AGE'})
df_career_stats = df_career_stats.rename(columns={'SEASON_ID': 'SEASON'})

df_career_stats_playoff = career_stats.get_data_frames()[2]
df_career_stats_playoff = df_career_stats_playoff.fillna('')
df_career_stats_playoff = df_career_stats_playoff.rename(columns={'TEAM_ABBREVIATION': 'TEAM'})
df_career_stats_playoff = df_career_stats_playoff.rename(columns={'PLAYER_AGE': 'AGE'})
df_career_stats_playoff = df_career_stats_playoff.rename(columns={'SEASON_ID': 'SEASON'})

print(f"<div class=\"label\">Overview</div>")
print(df_common_info[['NAME', 'COUNTRY', 'HEIGHT', 'WEIGHT', 'JERSEY', 'POSITION', 'FROM_YEAR', 'TO_YEAR']].to_html(index=False))

print(f"<div class=\"label\">Career Regular Season</div>")
print(df_career_stats[['SEASON', 'TEAM', 'AGE', 'GP', 'GS', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']].to_html(index=False))

if len(df_career_stats_playoff) > 0:
    print(f"<div class=\"label\">Career Playoff Season</div>")
    print(df_career_stats_playoff[['SEASON', 'TEAM', 'AGE', 'GP', 'GS', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']].to_html(index=False))
