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
    overview_info = teamdetails.TeamDetails(team_id=id)
    df_overview_info = overview_info.get_data_frames()[0]
    df_overview_info = df_overview_info.fillna('')
    df_overview_info = df_overview_info.drop(columns=['TEAM_ID'])
    print(df_overview_info.to_html(index=False))
    print(f"<div class=\"label\">Cities</div>")
    df_overview_info = overview_info.get_data_frames()[1]
    df_overview_info = df_overview_info.fillna('')
    df_overview_info = df_overview_info.drop(columns=['TEAM_ID'])
    print(df_overview_info.to_html(index=False))
    df_overview_info = overview_info.get_data_frames()[3]
    if len(df_overview_info) > 0:
        df_overview_info = df_overview_info.fillna('')
        print(f"<div class=\"label\">League Championships</div>")
        print(df_overview_info.to_html(index=False))
    df_overview_info = overview_info.get_data_frames()[4]
    if len(df_overview_info) > 0:
        df_overview_info = df_overview_info.fillna('')
        print(f"<div class=\"label\">Conference Titles</div>")
        print(df_overview_info[['YEARAWARDED']].to_html(index=False))
    df_overview_info = overview_info.get_data_frames()[5]
    if len(df_overview_info) > 0:
        df_overview_info = df_overview_info.fillna('')
        print(f"<div class=\"label\">Division Titles</div>")
        print(df_overview_info[['YEARAWARDED']].to_html(index=False))
    print(f"<div class=\"label\">Socials</div>")
    df_overview_info = overview_info.get_data_frames()[2]
    df_overview_info = df_overview_info.fillna('')
    print(df_overview_info.to_html(index=False))

elif mode == 'stats':
    print(f"<div class=\"label\">Stats</div>")
    stats_info = teamyearbyyearstats.TeamYearByYearStats(team_id=id)
    df_stats_info = stats_info.get_data_frames()[0]
    df_stats_info = df_stats_info.fillna('')
    print(df_stats_info.drop(columns=['TEAM_ID', 'TEAM_NAME', 'CONF_COUNT', 'DIV_COUNT', 'CONF_RANK', 'DIV_RANK', 'PO_WINS', 'PO_LOSSES', 'NBA_FINALS_APPEARANCE', 'TOV', 'BLK', 'PTS', 'PTS_RANK']).to_html(index=False))
    print(f"<div class=\"label\">Stats Cont.</div>")
    print(df_stats_info[['TEAM_CITY', 'YEAR', 'TOV', 'BLK', 'PTS', 'PTS_RANK', 'CONF_COUNT', 'DIV_COUNT', 'CONF_RANK', 'DIV_RANK', 'PO_WINS', 'PO_LOSSES', 'NBA_FINALS_APPEARANCE']].to_html(index=False))

elif mode == 'roster':
    print(f"<div class=\"label\">Players</div>")
    roster_info = commonteamroster.CommonTeamRoster(team_id=id)
    df_roster_info = roster_info.get_data_frames()[0]
    df_roster_info = df_roster_info.fillna('')
    df_roster_info = df_roster_info.rename(columns={'HOW_ACQUIRED': 'ACQUIRED'})
    print(df_roster_info[['PLAYER', 'NUM', 'POSITION', 'HEIGHT', 'WEIGHT', 'BIRTH_DATE', 'AGE', 'EXP', 'SCHOOL', 'ACQUIRED']].to_html(index=False))
    print(f"<div class=\"label\">Coaches</div>")
    df_roster_info = roster_info.get_data_frames()[1]
    df_roster_info = df_roster_info.fillna('')
    df_roster_info = df_roster_info.rename(columns={'COACH_NAME': 'NAME', 'COACH_TYPE': 'TYPE'})
    print(df_roster_info[['NAME', 'TYPE']].to_html(index=False))

