import os
import google.generativeai as genai

import check_api_key    # to get the env GEMINI_API_KEY
import example_prompts  # essentially does makes the 'history' to be fed into the model.start_chat's history.
import get_nba_stats_old    # contains function to ftches player stats for a game on the specified date and team

api_key = check_api_key.get_key()
if api_key is None:
    print("Error: Gemini API key not found. Please set it in your environment variables or .env file.")
    exit()
genai.configure(api_key = api_key)

# get / change stats for the game here
# convert the dataframes to strings
player_stats, team_stats = get_nba_stats_old.get_game_stats('CHA', 'NOP', "03/30/2025")
player_stats_str = player_stats.to_string()
team_stats_str = team_stats.to_string()

# create the model
generation_config = {
    "temperature": 0.25,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain"
}

prompting = f"""### Instructions
    You are an AI assistant that helps summarize and analyze the provided game facts, stats, and data in an accessible manner.

    ### Example
    Here are the player stats:
    {player_stats_str}

    Here are the team stats:
    {team_stats_str}

    ### Continue the responces below.
"""

# print(prompting)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config = generation_config,
    
    system_instruction = prompting
)

# from example_prompts.py
chat_session = model.start_chat(
    history = example_prompts.history
)

def main():
    print("Executed as main, send test message to Gemini about a given game (default 'CHA', 'NOP', \"03/30/2025\")")
    while True:
        user_input = input("Enter a msg for Gemini (or exit): ")
        if user_input.lower() == 'exit':
            print("ok bye bye")
            break
        if not user_input.strip(): # Check if the input is empty or contains only whitespace
            response = chat_session.send_message(content= "?") # fallback message
            print(response.text)
        else:
            response = chat_session.send_message(content=user_input)
            print(response.text)

if __name__ == "__main__":
    main()