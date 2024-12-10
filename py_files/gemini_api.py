import os
from dotenv import load_dotenv

# Loading environment variables from the .env file
load_dotenv()

# Getting the api key from the environment variable
the_api_key = os.getenv("DTK530_GEMINI_AI_API_KEY")

# Using the API key in my code
# print(the_api_key)