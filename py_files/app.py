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


#--------------------------------------#

# Title and introduction# Streamlit App UI
st.title("University Recommendation and Insights App")
st.markdown("This app helps international students find the best universities and gain insights based on key metrics.")

# Sidebar: User Input
st.sidebar.header("User Inputs")
user_text = st.text_area(
    "Describe your preferences (e.g., location, academic reputation, international student ratio, employment rate):",
    placeholder="E.g., I want a university in the United States with a high academic reputation and good employment rates."
)

# Extracted keywords from user input
def extract_features(user_text):
    # Dummy extraction logic (replace with actual NLP feature extraction)
    extracted_features = {
        "Country": "United States",
        "International Students Ratio Score": 85.0,
        "Academic Reputation Score": 90.0,
        "Graduate Employment Rate Score": 95.0
    }
    return extracted_features

if user_text:
    with st.spinner("Processing your input..."):
        features = extract_features(user_text)
        st.write("Extracted Features:")
        st.json(features)

    # Clustering Analysis
    st.subheader("Clustering Analysis")
    clustering_features = data[["International Students Ratio Score", "Graduate Employment Rate Score"]]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(clustering_features)

    kmeans = KMeans(n_clusters=3, random_state=42)
    data["Cluster"] = kmeans.fit_predict(scaled_features)

    user_cluster = kmeans.predict(scaler.transform([[features["International Students Ratio Score"], features["Graduate Employment Rate Score"]]]))[0]
    top_universities = data[data["Cluster"] == user_cluster].head(3)

    st.write(f"Recommended Universities from Cluster {user_cluster}:")
    st.table(top_universities[["University Name", "Country", "Academic Reputation Score"]])

    # Use Gemini API to fetch additional details
    st.subheader("Additional Details")
    for index, row in top_universities.iterrows():
        query = f"Provide detailed insights about {row['University Name']} including its strengths, application deadlines, and top programs."
        with st.spinner(f"Fetching details for {row['University Name']}..."):
            response = gemini_model.generate_content(query).text
            st.write(f"### {row['University Name']}")
            st.write(response)

    # User Q&A
    st.subheader("Ask More Questions")
    follow_up_question = st.text_input("Ask any specific question about the recommended universities:")
    if st.button("Submit Question"):
        with st.spinner("Fetching answer..."):
            response = gemini_model.generate_content(follow_up_question).text
            st.write(response)