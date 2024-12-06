import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

import google.generativeai as genai
import os
import warnings

warnings.filterwarnings("ignore")

# Load the dataset
data = pd.read_csv('../datasets/clean/qs2023_worlduni_rank_cleandata.csv')

from constants_and_styles import *
from gemini_ai_call import *
from gemini_api import *

# Gemini API integration 1
def __get_gemini_client__() -> genai.GenerativeModel:
    genai.configure(api_key=the_api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    return gemini_model
   
gemini_model = __get_gemini_client__()

# Title and introduction
st.title("University Recommendation and Analysis App")
st.markdown("This app helps international students find the best universities based on international presence and graduate employment outcomes.")

# Sidebar inputs
st.sidebar.header("User Inputs")
int_students_score = st.sidebar.slider("Desired International Students Ratio Score (0-100):", 0.0, 100.0, step=0.1)
selected_model = st.sidebar.selectbox("Select Analysis Model:", ["Clustering", "Regression"])

# Clustering analysis
if selected_model == "Clustering":
    st.subheader("Clustering Analysis")

    # Prepare data for clustering
    features = data[['International Students Ratio Score', 'Graduate Employment Rate Score']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Apply KMeans
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    data['Cluster'] = kmeans.fit_predict(scaled_features)

    # Visualize clusters
    fig, ax = plt.subplots()
    scatter = ax.scatter(data['International Students Ratio Score'],
                        data['Graduate Employment Rate Score'],
                        c=data['Cluster'], cmap='viridis', alpha=0.7)
    ax.set_xlabel("International Students Ratio Score")
    ax.set_ylabel("Graduate Employment Rate Score")
    ax.set_title("Clustering of Universities")
    st.pyplot(fig)

    # Recommend universities from the same cluster
    selected_cluster = kmeans.predict(scaler.transform([[int_students_score, 0]]))[0]
    st.write(f"Based on your input score, you belong to Cluster {selected_cluster}. Here are some universities from this cluster:")
    st.dataframe(data[data['Cluster'] == selected_cluster][['University Name', 'Graduate Employment Rate Score']].head())
  
    # Regression analysis
elif selected_model == "Regression":
    st.subheader("Regression Prediction")

    # Prepare data for regression
    X = data[['International Students Ratio Score']]
    y = data['Graduate Employment Rate Score']
    reg_model = LinearRegression()
    reg_model.fit(X, y)

    # Make prediction
    predicted_employment_rate = reg_model.predict([[int_students_score]])[0]
    st.write(f"Predicted Graduate Employment Rate Score: **{predicted_employment_rate:.2f}**")

    # Regression plot
    fig, ax = plt.subplots()
    ax.scatter(X, y, color='blue', alpha=0.5, label="Actual Data")
    ax.plot(X, reg_model.predict(X), color='red', label="Regression Line")
    ax.set_xlabel("International Students Ratio Score")
    ax.set_ylabel("Graduate Employment Rate Score")
    ax.set_title("Regression Analysis")
    ax.legend()
    st.pyplot(fig)

    # Display regression performance
    mse = mean_squared_error(y, reg_model.predict(X))
    st.write(f"Model Mean Squared Error: **{mse:.2f}**")
    
#--------------------------------------------------------------#

# Streamlit UI for User Input(s)
st.title("University Insights with Gemini API")
st.subheader("Ask Questions about University Rankings or Outcomes")

# # A
# Select the desired model for A
try:
    the_gemini_model = gemini_model  # Ensure the model is valid
except Exception as e:
    st.error(f"Error initializing Gemini model: {e}")
    the_gemini_model = None

user_input = st.text_input("Enter your query:")

# Button to submit and process input
if st.button("Generate Response"):
    if not user_input:
        st.error("Please provide the required input before proceeding.")
    else:
        # Initialize the Gemini model with your API key
        if the_gemini_model:
            try:
                # Make the API call
                with st.spinner("Fetching insights from Gemini API..."):
                    gemini_response = query_gemini_api(user_input, the_gemini_model)   # the_gemini_model.generate_content(user_input) | query_gemini_api(user_input, the_gemini_model)
                st.success("Gemini API Response:")
                st.write(gemini_response.text)  # Display the response from Gemini

            except Exception as e:
                st.error(f"An error occurred while fetching data from Gemini API: {e}")
        else:
            st.warning("Gemini model is not properly initialized. Please check the configuration.")
        

# # B
# # Streamlit App
# st.title("Gemini AI Image Analysis")
# st.write("Upload an image to get insights from the Gemini AI API.")

# # Upload an image
# uploaded_file = st.file_uploader("Upload an image (PNG or JPG)", type=["png", "jpg", "jpeg"])

# if uploaded_file:
#     try:
#         # Open the uploaded image using PIL
#         image = Image.open(uploaded_file)

#         # Display the uploaded image
#         st.image(image, caption="Uploaded Image", use_container_width=True)

#         # Select the Gemini model
#         try:
#             my_gemini_model = gemini_model  # Replace with the correct Gemini model initialization
#         except Exception as e:
#             st.error(f"Error initializing Gemini model: {e}")
#             my_gemini_model = None

#         # If model is successfully initialized
#         if gemini_model:
#             if st.button("Analyze Image"):
#                 with st.spinner("Fetching insights from Gemini API..."):
#                     response = query_gemini_api_for_image(image, gemini_model)
#                     st.success("Gemini API Response:")
#                     st.write(response)
#         else:
#             st.error("Gemini model is not properly initialized. Please check the configuration.")

#     except Exception as e:
#         st.error(f"Error processing the uploaded image: {e}")
# else:
#     st.info("Please upload an image to proceed.")