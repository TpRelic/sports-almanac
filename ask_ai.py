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

def get_ai_response(user_input: str) -> str:
    """Get AI response with web search capability."""
    try:
        # Create the input structure
        input_data = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "You are an AI assistant that helps analyze NBA games and stats. For YouTube URLs, extract and provide game details in this format:\nDate: MM/DD/YYYY\nTeam A: \nTeam B:"
                    }
                ]
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
            max_output_tokens=128,
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
