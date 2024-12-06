import requests

# Load environment variables
from gemini_api import *


def query_gemini_api(user_query):
    """
    Function to query Google's Gemini API with the user's input.
    """
    # Define the API endpoint
    api_url = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"
    
    # Headers and payload
    headers = {
        "Authorization": f"Bearer {DTK530_GEMINI_AI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": {
            "text": user_query
        },
        "temperature": 0.7,
        "maxOutputTokens": 150
    }
    
    try:
        # Make the API request
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()
        
        # Extract and return the response text
        return data.get("candidates", [{}])[0].get("output", "No response from API.")
    except Exception as e:
        return f"An error occurred: {e}"
