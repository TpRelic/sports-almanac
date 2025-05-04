import pandas as pd
from datetime import datetime

class GameFinder:
    def __init__(self):
        """Initialize GameFinder with games data."""
        # Alternative solution with explicit dtypes
        self.games_df = pd.read_csv("Games.csv", dtype={
            'gameId': str,
            'gameDate': str,
            'hometeamCity': str,
            'hometeamName': str,
            'hometeamId': str,
            'awayteamCity': str,
            'awayteamName': str,
            'awayteamId': str,
            'homeScore': float,
            'awayScore': float,
            'winner': str,
            'gameType': str,
            'attendance': float,
            'arenaId': str,
            'gameLabel': str,
            'gameSubLabel': str,
            'seriesGameNumber': float
        })
        
        # Convert gameDate to datetime
        self.games_df['gameDate'] = pd.to_datetime(self.games_df['gameDate'])

    def find_game_id(self, date_str, home_team, away_team):
        """
        Find NBA Game ID given date and team names.
        
        Args:
            date_str (str): Date in 'YYYY-MM-DD' format
            home_team (str): Home team name
            away_team (str): Away team name
            
        Returns:
            str: Game ID if found, error message if not found
        """
        try:
            # Convert date string to datetime
            date = pd.to_datetime(date_str).date()
            
            # Search for the game
            game = self.games_df[
                (self.games_df['gameDate'].dt.date == date) &
                (self.games_df['hometeamName'].str.contains(home_team, case=False)) &
                (self.games_df['awayteamName'].str.contains(away_team, case=False))
            ]
            
            if not game.empty:
                # Return game ID as string
                return str("00" + str(game.iloc[0]['gameId']))
            else:
                return "Game not found"
                
        except Exception as e:
            return f"Error finding game: {str(e)}"

    def get_available_games(self, date_str):
        """
        Get all games available for a specific date.
        
        Args:
            date_str (str): Date in 'YYYY-MM-DD' format
            
        Returns:
            dict: Dictionary of game descriptions mapped to game IDs
        """
        try:
            date = pd.to_datetime(date_str).date()
            days_games = self.games_df[self.games_df['gameDate'].dt.date == date]
            
            game_options = {}
            for _, game in days_games.iterrows():
                # Create more detailed game description
                display_text = f"{game['awayteamName']} @ {game['hometeamName']}"
                game_options[display_text] = str(game['gameId'])
                
            return game_options
            
        except Exception as e:
            print(f"Error getting available games: {str(e)}")
            return {}

# Example usage
if __name__ == "__main__":
    finder = GameFinder()
    
    # Test date format matches the CSV
    print("Testing game finder...")
    
    # Example 1: Find specific game
    game_id = finder.find_game_id('2024-05-15', 'Thunder', 'Mavericks')
    print(f"Found game ID: {game_id}")
    
    # Example 2: Get all games for a date
    games = finder.get_available_games('2025-01-01')
    print("\nGames available on 2025-01-01:")
    for desc, gid in games.items():
        print(f"{desc}: {gid}")

