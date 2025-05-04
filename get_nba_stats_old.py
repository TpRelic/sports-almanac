from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2
import pandas as pd

def get_game_stats(team_a='CHA', team_b='NOP', game_date="03/30/2025"):
    """
    Requests NBA game stats for team_a, team_b, on the specified date.
    
    Args:
        team_a, team_b: TEAM_ABBREVIATION '###' format to check games.
        game_date (str): Date in MM/DD/YYYY format (default: "03/30/2025")
    
    Returns:
        tuple: (player_stats_df, team_stats_df):
            Player stats (23 rows × 24 columns)
            Team Stats (3 rows × 25 columns)
                or None if no game found
    """
    # getch games on the specified date
    
    # TODO: check existing database if we want
    # else get from api and store it
    #
    # current code just gets from api
    
    gamefinder = leaguegamefinder.LeagueGameFinder(
        date_from_nullable=game_date,
        date_to_nullable=game_date
    )
    games = gamefinder.get_data_frames()[0]

    # filter for team
    found_games = games[
        ((games['TEAM_ABBREVIATION'] == team_a) & (games['MATCHUP'].str.contains(team_b))) |
        ((games['TEAM_ABBREVIATION'] == team_b) & (games['MATCHUP'].str.contains(team_a)))
    ]

    if not found_games.empty:
        game_id = found_games['GAME_ID'].iloc[0]
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
        player_stats = boxscore.get_data_frames()[0].drop(boxscore.get_data_frames()[0].columns[:5], axis=1)
        # print(player_stats)
        team_stats = boxscore.get_data_frames()[1]
        # print(team_stats)
        # temp_stats = boxscore.get_data_frames()[0]  # Player stats DataFrame
        # player_stats = temp_stats.drop(temp_stats.columns[:5], axis=1)  # axis 1 is columns
        
        return player_stats, team_stats
    else:
        print(f"No game found between the Hornets and Pelicans on {game_date}.")
        return None


# Example usage:
if __name__ == "__main__":
    # get stats as example
    player_stats, team_stats = get_game_stats(game_date="03/30/2025")
    
    if player_stats is not None:
        print("Player Stats:")
        print(player_stats)
        print("\nTeam Stats:")
        print(team_stats)