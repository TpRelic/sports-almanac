from google import genai
import creds    # include a file 'creds.py' with "api_key = '...' "

client = genai.Client(api_key=creds.api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words."
)

print(response.text)