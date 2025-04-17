import os
from dotenv import load_dotenv

def get_key():
    """
    trys returning the Gemini API key from environment variables or .env file
    otherwise returns None.
    """
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    return api_key

# Example usage:
if __name__ == "__main__":
    api_key = get_key()
    if api_key:
        print(f"Gemini API key found: {api_key[:5]}...")
    else:
        print("Error: Gemini API key not found. Please set it in your environment variables or .env file.")