import os
from dotenv import load_dotenv

load_dotenv()

def get_key():
    return os.getenv('GEMINI_API_KEY')

def get_openai_key():
    return os.getenv('OPENAI_API_KEY')

# Example usage:
if __name__ == "__main__":
    gemini_api_key = get_key()
    openai_api_key = get_openai_key()
    
    if gemini_api_key:
        print(f"Gemini API key found: {gemini_api_key[:5]}...")
    else:
        print("Error: Gemini API key not found. Please set it in your environment variables or .env file.")
    
    if openai_api_key:
        print(f"OpenAI API key found: {openai_api_key[:5]}...")
    else:
        print("Error: OpenAI API key not found. Please set it in your environment variables or .env file.")