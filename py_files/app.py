###############################################################

# Importing the necessary packages
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

from matplotlib.colors import ListedColormap
import plotly.express as px

import re

import PIL.Image

################################################################



# Securely accessing my dataset
from pathlib import Path
uni_recommend_rawdata_csv = Path(__file__).parents[1] / 'datasets/clean/qs2023_worlduni_rank_cleandata.csv'

# Loading the dataset
data = pd.read_csv(uni_recommend_rawdata_csv)

# Importing the necessary functions needed to run the app
from gemini_ai_call import *
from gemini_api import *

# Gemini API integration #1 - Calling the Gemini API
def __get_gemini_client__() -> genai.GenerativeModel:
    genai.configure(api_key=the_api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    return gemini_model
   
gemini_model = __get_gemini_client__()

# Function to recode the selected features (Academic Reputation Score, International Students Ratio Score, Graduate Employment Rate Score) from the dataset for clustering/classification
def recode_the_cols(data):
    the_ranges = [0,20,40,60,80,100]
    the_labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
    the_map_dict = {
        'Very Low': 0,
        'Low': 1,
        'Medium': 2, 
        'High': 3,
        'Very High': 4
    }

    # Segmenting and sorting data values into bins for easy classification
    data['Academic Reputation Score Encoded'] = pd.cut( data['Academic Reputation Score'],bins = the_ranges , include_lowest = True, labels = the_labels)
    data['International Students Ratio Score Encoded'] = pd.cut( data['International Students Ratio Score'],bins = the_ranges , include_lowest = True, labels = the_labels)
    data['Graduate Employment Rate Score Encoded'] = pd.cut( data['Graduate Employment Rate Score'],bins = the_ranges , include_lowest = True, labels = the_labels)

    # Mapping the new codes to the new encoded columns
    data['Academic Reputation Score Encoded'] = data['Academic Reputation Score Encoded'].map(the_map_dict)
    data['International Students Ratio Score Encoded'] = data['International Students Ratio Score Encoded'].map(the_map_dict)
    data['Graduate Employment Rate Score Encoded'] = data['Graduate Employment Rate Score Encoded'].map(the_map_dict)
    
    return data
    


#------------------------ The Streamlit App starts here! --------------------------#

# Function for styling the app [BlueBlack - #21262D; Grey - #C9D1D9]

def set_background_theme():
    st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #073763;
        color: #f0c244;
    } 
    
    /* Customizing the button element */
    .stButton>button {
        background-color: #f0c244;
        color: #073763;
        margin-left: 270px;
    }
    
    .stTextArea {
        label-color: #f0c244;
        color: #073763;
    }
    
    </style>
    """, unsafe_allow_html=True)   

# Calling the styling function
set_background_theme()

# App Logo
app_logo_image_path = Path(__file__).parents[1] / 'images/UR&IA.png'
app_logo_image = PIL.Image.open(app_logo_image_path)
st.image(app_logo_image)

# Title and Introduction
# st.title("University Recommendation and Insights App")
st.markdown("This app helps international students find the best universities and gain insights based on key metrics.")

st.markdown(f'<div style="text-align: center; color: white; font-size:14px"> Describe your preferences (e.g., location, academic reputation, international student ratio, employment rate):', unsafe_allow_html=True)
# I - User input text area
user_text = st.text_area(
    " ",
    placeholder="E.g., I want a university in the United States with a high academic reputation of 90, international student diversity of 85 and good employment rates around 80."
)

user_to_click = st.button("Recommend!")

# II - Natural Language Processing Feature Extraction using Regex

def extract_features(sentence):
    
    # Defining patterns for each feature
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

# Check for some errors here
if user_text and user_to_click:
    with st.spinner("Processing your input..."):
        features = extract_features(user_text)
        # st.write("Extracted Features:")
        # st.json(features)
    
    # III - Clustering Analysis
    st.subheader("Clustering Analysis")
 
    data = recode_the_cols(data) # Creating 3 new columns with encoded to perform  our clustering

    # Features for classification/clustering
    clustering_features = data[[
        "Academic Reputation Score Encoded",
        "International Students Ratio Score Encoded",
        "Graduate Employment Rate Score Encoded"
    ]]
    
    data = recode_the_cols(data)

    num_of_clusters = 25 

    kmeans = KMeans(n_clusters=num_of_clusters, random_state=42)
    data["Cluster"] = kmeans.fit_predict(clustering_features)

    # Recoding user input to allow for clustering
    if user_text:
        features_encoded = recode_the_cols(pd.DataFrame([features]))
        
        selected_features_encoded = features_encoded[[
        "Academic Reputation Score Encoded",
        "International Students Ratio Score Encoded",
        "Graduate Employment Rate Score Encoded"
        ]]
        
        # print(selected_features_encoded)

        user_cluster = kmeans.predict(selected_features_encoded)[0]
        
        # EXTRA - Filtering by cluster and country
        filtered_data = data[data["Cluster"] == user_cluster]
        
        # Tackling the edge case of a country not being in the dataset
        if features["Country"]:
            filtered_data_country = filtered_data[filtered_data["Country"].str.contains(features["Country"], case=False)]
            
            if len(filtered_data_country) > 0:
                filtered_data = filtered_data_country
            else:
                st.markdown('<p style="color:white;">Unfortunately, no schools are available for your selected preference scores but below are other schools in different countries you can consider!</p>', unsafe_allow_html=True)
                
        # Recommend top universities based on clustering
        top_universities = filtered_data.sort_values(
            by=["Academic Reputation Score", "International Students Ratio Score", "Graduate Employment Rate Score"], 
            ascending=False
        ).head(3)

        st.write(f"Top universities for your preferences (Cluster {user_cluster}):")
        st.dataframe(top_universities[["University Name", "Country", "Academic Reputation Score","International Students Ratio Score","Graduate Employment Rate Score"]])


    # IV - Plotting Cluster Graph for enhanced UI experience for user
    st.subheader("Cluster Visualization")

    data["Size"] = 2

    # Creating 3D scatter plot with Plotly to visualize the three features helping predict the best scores and schools
    fig = px.scatter_3d(
        data,
        x='Academic Reputation Score',
        y='International Students Ratio Score',
        z='Graduate Employment Rate Score',
        color=data['Cluster'].astype(str),  # Use cluster labels as color
        title="3D Scatter Plot of Clusters",
        labels={'cluster': 'Cluster'},
        symbol = 'Cluster',
        size = 'Size'
    )
    # Adding centroids to help pinpoint the 3 selected schools
    centroids = kmeans.cluster_centers_[:3] # The top 3 universities
    centroids_df = pd.DataFrame(centroids, columns=['Academic Reputation Score', 'International Students Ratio Score', 'Graduate Employment Rate Score'])
    fig.add_scatter3d(
        x=centroids_df['Academic Reputation Score'],
        y=centroids_df['International Students Ratio Score'],
        z=centroids_df['Graduate Employment Rate Score'],
        mode='markers',
        marker=dict(size=16, color='black', symbol='cross'),
        name='Top 3 User Preferences'
    )
    st.plotly_chart(fig, use_container_width=True)
         

    
    # V - Gemini API Integration #2 - Using Gemini API to fetch additional details
    st.subheader("Additional Details")
    for index, row in top_universities.iterrows():
        query = f"""
                    Please provide a comprehensive overview of {row['University Name']} focusing on:

                        1. Top 3 Undergraduate Programs:
                        - Program Names
                        - Unique Strengths
                        - Notable Faculty/Research Areas

                        2. Top 3 Graduate Programs:
                        - Program Names
                        - Research Opportunities
                        - Industry/Academic Connections

                        3. Distinctive Historical or Institutional Element:
                        - Unique Founding Story
                        - Groundbreaking Research/Innovation
                        - Cultural/Academic Contribution That Sets It Apart

                        4. Quick Stats:
                        - Total Student Population
                        - International Student Percentage
                        - Student-to-Faculty Ratio
                        - Year Founded
                """
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
           
st.markdown(f'<div style="text-align: center; color: #f0c244;"> Made with ❤️ by theoriginialmapd © Copyright 2024 @ Duke in DESIGNTK530', unsafe_allow_html=True)