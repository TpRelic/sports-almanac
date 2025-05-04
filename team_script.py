import sys
import io
from nba_api.stats.endpoints import teaminfocommon
from nba_api.stats.endpoints import teamyearbyyearstats
from nba_api.stats.endpoints import teamdetails
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.static import teams

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

team = sys.argv[1]
team_info = teams.find_teams_by_full_name(team)

if len(team_info) != 1:
    print(f"<p class=\"error_label\">No team by the name of {sys.argv[1]}...<br>Make sure to enter the team's full name!</p>")
    exit()

id = team_info[0]['id']

mode = sys.argv[2]

if mode == 'overview':
    print(f"<div class=\"label\">Overview</div>")
    common_info = teaminfocommon.TeamInfoCommon(team_id=id)
    df_common_info = common_info.get_data_frames()[0]
    df_common_info = df_common_info.fillna('')
    df_common_info = df_common_info.rename(columns={'SEASON_YEAR': 'SEASON', 'TEAM_CITY': 'CITY', 'TEAM_NAME': 'NAME', 'TEAM_ABBREVIATION': 'ABBRV.', 'TEAM_CONFERENCE': 'CONFERENCE', 'TEAM_DIVISION': 'DIVISION'})
    print(df_common_info[['SEASON', 'CITY', 'NAME', 'ABBRV.', 'CONFERENCE', 'DIVISION', 'W', 'L', 'PCT', 'CONF_RANK', 'DIV_RANK', 'MIN_YEAR', 'MAX_YEAR']].to_html(index=False))

    print(f"<div class=\"label\">Ranks</div>")
    common_info = teaminfocommon.TeamInfoCommon(team_id=id)
    df_common_info = common_info.get_data_frames()[1]
    df_common_info = df_common_info.fillna('')
    print(df_common_info[['PTS_RANK', 'PTS_PG', 'REB_RANK', 'REB_PG', 'AST_RANK', 'AST_PG', 'OPP_PTS_RANK', 'OPP_PTS_PG']].to_html(index=False))

elif mode == 'stats':
    print(f"<div class=\"label\">Stats</div>")
    stats_info = teamyearbyyearstats.TeamYearByYearStats(team_id=id)
    df_stats_info = stats_info.get_data_frames()[0]
    df_stats_info = df_stats_info.fillna('')
    print(df_stats_info.drop(columns=['TEAM_ID', 'TEAM_NAME', 'CONF_COUNT', 'DIV_COUNT', 'CONF_RANK', 'DIV_RANK', 'PO_WINS', 'PO_LOSSES', 'NBA_FINALS_APPEARANCE', 'TOV', 'BLK', 'PTS', 'PTS_RANK']).to_html(index=False))
    print(f"<div class=\"label\">Stats Cont.</div>")
    print(df_stats_info[['TEAM_CITY', 'YEAR', 'TOV', 'BLK', 'PTS', 'PTS_RANK', 'CONF_COUNT', 'DIV_COUNT', 'CONF_RANK', 'DIV_RANK', 'PO_WINS', 'PO_LOSSES', 'NBA_FINALS_APPEARANCE']].to_html(index=False))

elif mode == 'awards':
    print(f"<div class=\"label\">Awards Stub</div>")

elif mode == 'roster':
    print(f"<div class=\"label\">Players</div>")
    roster_info = commonteamroster.CommonTeamRoster(team_id=id)
    df_roster_info = roster_info.get_data_frames()[0]
    df_roster_info = df_roster_info.fillna('')
    print(df_roster_info.to_html(index=False))
    print(f"<div class=\"label\">Coaches</div>")
    df_roster_info = roster_info.get_data_frames()[1]
    df_roster_info = df_roster_info.fillna('')
    print(df_roster_info.to_html(index=False))




#common_info = commonplayerinfo.CommonPlayerInfo(player_id=id)

#df_common_info = common_info.get_data_frames()[0]
#df_common_info = df_common_info.rename(columns={'DISPLAY_FIRST_LAST': 'NAME'})

#career_stats = playercareerstats.PlayerCareerStats(player_id=id) 

#df_career_stats = career_stats.get_data_frames()[0]
#df_career_stats = df_career_stats.fillna('')
#df_career_stats = df_career_stats.rename(columns={'TEAM_ABBREVIATION': 'TEAM'})
#df_career_stats = df_career_stats.rename(columns={'PLAYER_AGE': 'AGE'})
#df_career_stats = df_career_stats.rename(columns={'SEASON_ID': 'SEASON'})

#df_career_stats_playoff = career_stats.get_data_frames()[2]
#df_career_stats_playoff = df_career_stats_playoff.fillna('')
#df_career_stats_playoff = df_career_stats_playoff.rename(columns={'TEAM_ABBREVIATION': 'TEAM'})
#df_career_stats_playoff = df_career_stats_playoff.rename(columns={'PLAYER_AGE': 'AGE'})
#df_career_stats_playoff = df_career_stats_playoff.rename(columns={'SEASON_ID': 'SEASON'})

#print(f"<div class=\"label\">Overview</div>")
#print(df_common_info[['NAME', 'COUNTRY', 'HEIGHT', 'WEIGHT', 'JERSEY', 'POSITION', 'FROM_YEAR', 'TO_YEAR']].to_html(index=False))

#print(f"<div class=\"label\">Career Regular Season</div>")
#print(df_career_stats[['SEASON', 'TEAM', 'AGE', 'GP', 'GS', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']].to_html(index=False))

#if len(df_career_stats_playoff) > 0:
#    print(f"<div class=\"label\">Career Playoff Season</div>")
#    print(df_career_stats_playoff[['SEASON', 'TEAM', 'AGE', 'GP', 'GS', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']].to_html(index=False))
