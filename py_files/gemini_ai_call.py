# from gemini_api import the_api_key  # Import the API key from gemini_api.py
# import requests

# import genai  # Assuming `genai` is the package used to interact with Gemini API

# # Function to call the Gemini API
# def query_gemini_api(user_query: str, gemini_model: genai.GenerativeModel) -> str:
#     response = gemini_model.generate_content([
#         "Your instructions for the Gemini model",
#         user_query,  # User's query input
#     ])
#     response.resolve()  # Resolves the response
#     return response.text  # Returns the response text from Gemini
