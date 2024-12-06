import google.generativeai as genai  # Replace with the actual Gemini SDK import
from PIL import Image  # For handling image input
from typing import List, Optional

# A
# Function to query Gemini API (Text)
def query_gemini_api(user_text: str, gemini_model: genai.GenerativeModel) -> str:
    """
    Calls the Gemini API with the user's text input and returns the response.

    Args:
        user_text (str): The text input from the user.
        gemini_model (GenerativeModel): Initialized Gemini model instance.

    Returns:
        str: The generated response from the Gemini API.
    """
    try:
        # Generate content using Gemini model's structured prompt
        response = gemini_model.generate_content(user_text)  # User's query
        
        # Resolve the response to ensure all processing is completed
        response.resolve()
        
        # Return the text content from the response
        return response

    except Exception as e:
        # Handle and return any errors
        return f"An error occurred: {e}"

   
# # B
# # Function to query the Gemini API (Image)
# import streamlit as st
# from PIL import Image
# import base64
# import io

# # Function to call the Gemini API
# def query_gemini_api_for_image(user_image, gemini_model: genai.GenerativeModel) -> str:
#     """
#     Sends an image to the Gemini API and retrieves the response.

#     Args:
#         user_image (PIL.Image): The uploaded image input from the user.
#         gemini_model (GenerativeModel): The initialized Gemini model instance.

#     Returns:
#         str: The generated response from the Gemini API.
#     """
#     try:
#         # Convert image to Base64 format
#         buffered = io.BytesIO()
#         user_image_format = user_image.format or "PNG"  # Default to PNG if format is not provided
#         user_image.save(buffered, format=user_image_format)
#         encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

#         # Prepare payload for Gemini API
#         payload = {
#             "parts": [
#                 {
#                     "blob": {
#                         "mime_type": f"image/{user_image_format.lower()}",
#                         "data": encoded_image
#                     }
#                 }
#             ]
#         }

#         # Call the Gemini API
#         response = gemini_model.generate_content(payload)

#         # Resolve the response to ensure processing is complete
#         response.resolve()

#         # Return the text content of the response
#         return response

#     except Exception as e:
#         return f"An error occurred: {e}"