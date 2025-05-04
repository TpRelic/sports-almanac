#!/usr/bin/env python3
import os
import sys
from openai import OpenAI
import check_api_key

# Initialize OpenAI client
OPENAI_API_KEY = check_api_key.get_openai_key()
if OPENAI_API_KEY is None:
    print("Error: OpenAI API key not found")
    sys.exit(1)
client = OpenAI(api_key=OPENAI_API_KEY)

def get_ai_response(user_input: str, game_context: dict = None) -> str:
    """Get AI response with game context."""
    try:
        # Create system message with live game context
        system_content = {
            "type": "input_text",
            "text": "You are an AI assistant analyzing a live NBA game. "
                   "Provide insights based on the current game state and player statistics."
        }
        
        if game_context:
            context = (
                f"Current Game State:\n"
                f"Score: {game_context['current_scores']['away']} - {game_context['current_scores']['home']}\n"
                f"Latest Play: {game_context['current_play']}\n\n"
                f"Player Statistics:\n"
            )
            
            # Add player stats
            for player, stats in game_context['player_stats'].items():
                context += f"{player} ({stats['team']}): {stats['points']} pts, {stats['rebounds']} reb, {stats['assists']} ast\n"
            
            system_content["text"] += f"\n\nGame Context:\n{context}"

        input_data = [
            {
                "role": "system",
                "content": [system_content]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": user_input
                    }
                ]
            }
        ]

        # Call OpenAI API with increased tokens and temperature adjustment
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
            temperature=0.7,  # Reduced for more focused responses
            max_output_tokens=256,  # Increased for more detailed responses
            top_p=0.9,
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
