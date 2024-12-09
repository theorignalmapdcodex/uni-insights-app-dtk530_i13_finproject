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

# I - User input text area
user_text = st.text_area(
    "Describe your preferences (e.g., location, academic reputation, international student ratio, employment rate):",
    placeholder="E.g., I want a university in the United States with a high academic reputation of 90, international student diversity of 85 and good employment rates around 80."
)


# II - NLP Feature Extraction
import re

def extract_features(sentence):
    # Define patterns for each feature
    country_pattern = r"university in the ([A-Za-z\s]+) with"
    academic_reputation_pattern = r"academic reputation of (\d+)"
    international_students_pattern = r"international student diversity of (\d+)"
    employment_rate_pattern = r"employment rates around (\d+)"

    # Extract features using regex
    country_match = re.search(country_pattern, sentence)
    academic_reputation_match = re.search(academic_reputation_pattern, sentence)
    international_students_match = re.search(international_students_pattern, sentence)
    employment_rate_match = re.search(employment_rate_pattern, sentence)

    # Assign extracted values or default to None
    extracted_features = {
        "Country": country_match.group(1).strip() if country_match else None,
        "Academic Reputation Score": float(academic_reputation_match.group(1)) if academic_reputation_match else None,
        "International Students Ratio Score": float(international_students_match.group(1)) if international_students_match else None,
        "Graduate Employment Rate Score": float(employment_rate_match.group(1)) if employment_rate_match else None
    }
    return extracted_features

if user_text:
    with st.spinner("Processing your input..."):
        features = extract_features(user_text)
        st.write("Extracted Features:")
        st.json(features)

    # # IIIa - Clustering Analysis
    # st.subheader("Clustering Analysis")
    # clustering_features = data[["International Students Ratio Score", "Graduate Employment Rate Score"]]
    # scaler = StandardScaler()
    # scaled_features = scaler.fit_transform(clustering_features)

    # kmeans = KMeans(n_clusters=3, random_state=42)
    # data["Cluster"] = kmeans.fit_predict(scaled_features)

    # user_cluster = kmeans.predict(scaler.transform([[features["International Students Ratio Score"], features["Graduate Employment Rate Score"]]]))[0]
    # top_universities = data[data["Cluster"] == user_cluster].head(3)

    # st.write(f"Top universities for your preferences (Cluster {user_cluster}):")
    # st.dataframe(top_universities[["University Name", "Country", "Graduate Employment Rate Score"]])

    # # IV - Plot Cluster Graph
    # st.subheader("Cluster Visualization")
    # fig, ax = plt.subplots(figsize=(10, 6))
    # scatter = ax.scatter(
    #     data["International Students Ratio Score"],
    #     data["Graduate Employment Rate Score"],
    #     c=data["Cluster"],
    #     cmap="viridis",
    #     alpha=0.7,
    #     edgecolor="k"
    # )
    # ax.set_xlabel("International Students Ratio Score")
    # ax.set_ylabel("Graduate Employment Rate Score")
    # ax.set_title("Clustering of Universities")
    # ax.scatter(
    #     features["International Students Ratio Score"],
    #     features["Graduate Employment Rate Score"],
    #     color="red",
    #     label="User Preference",
    #     s=150,
    #     edgecolor="black"
    # )
    # ax.legend()
    # st.pyplot(fig)
    
    
    # IIIb - Clustering Analysis: Updated Clustering and Recommendation Code From ChatGPT
    st.subheader("Clustering Analysis")

    # Include more features in clustering
    clustering_features = data[[
        "Academic Reputation Score",
        "International Students Ratio Score",
        "Graduate Employment Rate Score"
    ]]

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(clustering_features)

    kmeans = KMeans(n_clusters=3, random_state=42)
    data["Cluster"] = kmeans.fit_predict(scaled_features)

    # Scale user input
    if user_text:
        user_features_scaled = scaler.transform([[
            features["Academic Reputation Score"],
            features["International Students Ratio Score"],
            features["Graduate Employment Rate Score"]
        ]])

        user_cluster = kmeans.predict(user_features_scaled)[0]

        # Filter by cluster and country
        filtered_data = data[data["Cluster"] == user_cluster]
        if features["Country"]:
            filtered_data = filtered_data[filtered_data["Country"].str.contains(features["Country"], case=False)]

        # Recommend top universities based on clustering
        top_universities = filtered_data.sort_values(
            by=["Academic Reputation Score", "Graduate Employment Rate Score"], 
            ascending=False
        ).head(3)

        st.write(f"Top universities for your preferences (Cluster {user_cluster}):")
        st.dataframe(top_universities[["University Name", "Country", "Academic Reputation Score", "Graduate Employment Rate Score"]])

        # Cluster Visualization
        st.subheader("Cluster Visualization")
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(
            data["International Students Ratio Score"],
            data["Graduate Employment Rate Score"],
            c=data["Cluster"],
            cmap="viridis",
            alpha=0.7,
            edgecolor="k"
        )
        ax.set_xlabel("International Students Ratio Score")
        ax.set_ylabel("Graduate Employment Rate Score")
        ax.set_title("Clustering of Universities")
        ax.scatter(
            features["International Students Ratio Score"],
            features["Graduate Employment Rate Score"],
            color="red",
            label="User Preference",
            s=150,
            edgecolor="black"
        )
        ax.legend()
        st.pyplot(fig)

     

    
    # V - Use Gemini API to fetch additional details
    st.subheader("Additional Details")
    for index, row in top_universities.iterrows():
        query = f"Provide detailed insights about {row['University Name']} including its strengths, application deadlines, and top programs."
        with st.spinner(f"Fetching details for {row['University Name']}..."):
            response = gemini_model.generate_content(query).text
            st.write(f"### {row['University Name']}")
            st.write(response)


    # VI - User Optional Q&A
    st.subheader("Ask More Questions")
    follow_up_question = st.text_input("Ask any specific question about the recommended universities:")
    if st.button("Submit Question"):
        with st.spinner("Fetching answer..."):
            response = gemini_model.generate_content(follow_up_question).text
            st.write(response)