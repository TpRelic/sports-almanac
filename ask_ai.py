#!/usr/bin/env python3
import os
import sys
from openai import OpenAI
import check_api_key
from nba_api.live.nba.endpoints import boxscore

# Initialize OpenAI client
OPENAI_API_KEY = check_api_key.get_openai_key()
if OPENAI_API_KEY is None:
    print("Error: OpenAI API key not found")
    sys.exit(1)
client = OpenAI(api_key=OPENAI_API_KEY)

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
    """Get AI response with game context and web search capability."""
    try:
        # Get game info if game_id is available
        game_info = None
        if game_context and 'game_id' in game_context:
            game_info = get_game_info(game_context['game_id'])

        # Create system message with game context
        system_text = "You are an AI assistant analyzing NBA games and stats. "
        
        if game_info:
            system_text += f"\nCurrent Game Context:\n"
            system_text += f"{game_info['away_team']['name']} ({game_info['away_team']['code']}) vs "
            system_text += f"{game_info['home_team']['name']} ({game_info['home_team']['code']})\n"
            system_text += f"Score: {game_info['away_team']['score']} - {game_info['home_team']['score']}\n"
            system_text += f"Period: {game_info['period']}, Clock: {game_info['game_clock']}\n"
            
            if game_context.get('compact_plays'):
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