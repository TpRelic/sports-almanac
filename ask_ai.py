#!/usr/bin/env python3
import os
import sys
from openai import OpenAI
import check_api_key
from nba_api.live.nba.endpoints import boxscore
import pandas as pd
from pathlib import Path

# Add database path
DB_PATH = Path(__file__).parent / "Games.csv"

# Initialize OpenAI client
OPENAI_API_KEY = check_api_key.get_openai_key()
if OPENAI_API_KEY is None:
    print("Error: OpenAI API key not found")
    sys.exit(1)
client = OpenAI(api_key=OPENAI_API_KEY)

def get_game_from_database(game_id: str) -> dict:
    """Fetch game information from local database."""
    try:
        # Read the Games.csv database with explicit data types
        df = pd.read_csv(DB_PATH, 
                        dtype={
                            'gameId': str,
                            'gameDate': str,
                            'hometeamName': str,
                            'awayteamName': str,
                            'homeScore': str,
                            'awayScore': str,
                            'winner': str
                        },
                        low_memory=False)
        
        # Ensure game_id is string type for comparison
        game_id = str(game_id)
        
        # Find the specific game
        game_records = df[df['GAME_ID'] == game_id].to_dict('records')
        if game_records:
            return game_records[0]
        print(f"Game ID {game_id} not found in database")
        return None
    except Exception as e:
        print(f"Database error: {str(e)}")
        print(f"Available columns: {df.columns.tolist() if 'df' in locals() else 'No dataframe loaded'}")
        return None

def get_game_info(game_id: str) -> dict:
    """Fetch game information from NBA API."""
    try:
        bs = boxscore.BoxScore(game_id)
        data = bs.get_dict().get('game', {})
        
        # Extract basic game info
        away_team = data.get('awayTeam', {})
        home_team = data.get('homeTeam', {})
        
        return {
            'game_id': game_id,
            'away_team': {
                'name': away_team.get('teamName'),
                'code': away_team.get('teamTricode'),
                'score': away_team.get('score')
            },
            'home_team': {
                'name': home_team.get('teamName'),
                'code': home_team.get('teamTricode'),
                'score': home_team.get('score')
            },
            'period': data.get('period', 0),
            'game_clock': data.get('gameClock', ''),
            'game_status': data.get('gameStatus', '')
        }
    except Exception as e:
        return None

def get_ai_response(user_input: str, game_context: dict = None) -> str:
    """Get AI response with enhanced game context."""
    try:
        # Get both live and historical game info
        game_info = None
        game_history = None
        
        if game_context and 'game_id' in game_context:
            game_info = get_game_info(game_context['game_id'])
            game_history = get_game_from_database(game_context['game_id'])

        # Create enhanced system message
        system_text = """You are an AI assistant analyzing NBA games and stats. 
        Keep your responses short and concise. Provide accurate information based on the game data provided.
        If you don't know the answer, please utilize the web search tool to find the information required"""
        
        if game_info:
            # Add live game context
            system_text += f"\nCurrent Game Context:\n"
            system_text += f"{game_info['away_team']['name']} ({game_info['away_team']['code']}) vs "
            system_text += f"{game_info['home_team']['name']} ({game_info['home_team']['code']})\n"
            system_text += f"Score: {game_info['away_team']['score']} - {game_info['home_team']['score']}\n"
            system_text += f"Period: {game_info['period']}, Clock: {game_info['game_clock']}\n"
            
        if game_history:
            # Add historical context
            system_text += f"\nGame History:\n"
            system_text += f"Season: {game_history.get('SEASON', 'N/A')}\n"
            system_text += f"Game Type: {game_history.get('GAME_TYPE', 'Regular Season')}\n"
            system_text += f"Series Game: {game_history.get('SERIES_GAME', 'N/A')}\n"
            system_text += f"Series Standing: {game_history.get('SERIES_STANDING', 'N/A')}\n"
            
        if game_context and game_context.get('compact_plays'):
            system_text += "\nRecent Plays (Format: [Type][PlayerNumber][Value]):\n"
            system_text += "Type: P=Points, R=Rebound, A=Assist, S=Steal, B=Block\n"
            system_text += f"Last actions: {' '.join(game_context['compact_plays'][-10:])}\n"

        # Create the input structure
        input_data = [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": system_text}]
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": user_input}]
            }
        ]

        # Call OpenAI API
        response = client.responses.create(
            model="gpt-4o-mini",
            input=input_data,
            text={"format": {"type": "text"}},
            reasoning={},
            tools=[
                {
                    "type": "web_search_preview",
                    "user_location": {"type": "approximate"},
                    "search_context_size": "medium"
                }
            ],
            temperature=1,
            max_output_tokens=256,
            top_p=1,
            store=True
        )

        # Extract content from response
        if hasattr(response, 'output') and response.output:
            for message in response.output:
                if hasattr(message, 'content'):
                    for content in message.content:
                        if content.type == 'output_text':
                            return content.text.strip()
        return "I couldn't process that request. Please try again."

    except Exception as e:
        return f"Error: {str(e)}"

def format_response(text: str) -> str:
    """Format the response text for better readability."""
    formatted = "\n" + "─" * 80 + "\n\n"  # Wider separator
    formatted += text
    formatted += "\n\n" + "─" * 80 + "\n"
    return formatted

if __name__ == "__main__":
    print("\nNBA Insights AI")
    print("Ask me anything about NBA games and stats!\n")
    
    user_input = input("Your question: ")
    print("\nSearching...")
    
    # Get the response from OpenAI
    response_text = get_ai_response(user_input)
    formatted_response = format_response(response_text)
    
    # Print the formatted response
    print(formatted_response)
