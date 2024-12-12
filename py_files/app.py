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

# Load the dataset
data = pd.read_csv('../datasets/clean/qs2023_worlduni_rank_cleandata.csv')

from gemini_ai_call import *
from gemini_api import *

# Gemini API integration 1
def __get_gemini_client__() -> genai.GenerativeModel:
    genai.configure(api_key=the_api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    return gemini_model
   
gemini_model = __get_gemini_client__()


# Recoding the dataset for clustering/classification
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

    #1
    data['Academic Reputation Score Encoded'] = pd.cut( data['Academic Reputation Score'],bins = the_ranges , include_lowest = True, labels = the_labels)
    data['International Students Ratio Score Encoded'] = pd.cut( data['International Students Ratio Score'],bins = the_ranges , include_lowest = True, labels = the_labels)
    data['Graduate Employment Rate Score Encoded'] = pd.cut( data['Graduate Employment Rate Score'],bins = the_ranges , include_lowest = True, labels = the_labels)

    #2
    data['Academic Reputation Score Encoded'] = data['Academic Reputation Score Encoded'].map(the_map_dict)
    data['International Students Ratio Score Encoded'] = data['International Students Ratio Score Encoded'].map(the_map_dict)
    data['Graduate Employment Rate Score Encoded'] = data['Graduate Employment Rate Score Encoded'].map(the_map_dict)
    
    return data
    

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
    # my_extraction_prompt = f"""
    # Extract the important entities mentioned in the text below. First extract all Country name, then extract all Academic reputation score, then extract International Students ratio score which fit the content and finally extract Graduate Employment Rate score. Make sure you ignore percentages. Also, for the country name, use the full version if it means changing the short versions to the long ones.

    # Desired format/response should be json format with its corresponding values: 
    # Country: -||- 
    # Academic reputation: -||- 
    # International Students ratio: -||- 
    # Graduate Employment Rate: -||- 
    
    # Text: {sentence}"""
    
    # # Call the gemini query function and pass prompt
    # # Parse the .json result to to_dict and extract the features
    # # *** Check if country, aca rep, int stud etc. is present in query

    # # fuzzy search - when working in the filtered_data_country section (https://github.com/rapidfuzz/RapidFuzz)
    
    
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
        # st.write("Extracted Features:")
        # st.json(features)

    # IIIa - Clustering Analysis
    
    num_of_clusters = 25

    
    # st.subheader("Clustering Analysis")
    # clustering_features = data[["Academic Reputation Score","International Students Ratio Score", "Graduate Employment Rate Score"]]
    # scaler = StandardScaler()
    # scaled_features = scaler.fit_transform(clustering_features)

    # kmeans = KMeans(n_clusters=num_of_clusters, random_state=42)
    # data["Cluster"] = kmeans.fit_predict(scaled_features)

    # user_cluster = kmeans.predict(scaler.transform([[features["Academic Reputation Score"],features["International Students Ratio Score"], features["Graduate Employment Rate Score"]]]))[0]
    # top_universities = data[data["Cluster"] == user_cluster].head(3)

    # st.write(f"Top universities for your preferences (Cluster {user_cluster}):")
    # st.dataframe(top_universities[["University Name", "Country", "Academic Reputation Score","International Students Ratio Score","Graduate Employment Rate Score"]])



    # # IV - Plot Cluster Graph
    # st.subheader("Cluster Visualization")


    # # Create 3D scatter plot with Plotly
    # fig = px.scatter_3d(
    #     data,
    #     x='Academic Reputation Score',
    #     y='International Students Ratio Score',
    #     z='Graduate Employment Rate Score',
    #     color=data['Cluster'].astype(str),  # Use cluster labels as color
    #     title="3D Scatter Plot of Clusters",
    #     labels={'cluster': 'Cluster'}
    # )
    # # # Add centroids
    # centroids = kmeans.cluster_centers_[:3]
    # centroids_df = pd.DataFrame(centroids, columns=['Academic Reputation Score', 'International Students Ratio Score', 'Graduate Employment Rate Score'])
    # fig.add_scatter3d(
    #     x=centroids_df['Academic Reputation Score'],
    #     y=centroids_df['International Students Ratio Score'],
    #     z=centroids_df['Graduate Employment Rate Score'],
    #     mode='markers',
    #     marker=dict(size=8, color='black', symbol='star'),
    #     name='Top 3 User Preferences'
    # )
    # st.plotly_chart(fig, use_container_width=True)
    
    
    # fig, ax = plt.subplots(figsize=(10, 6))
    # scatter = ax.scatter3d(
    #     data["Academic Reputation Score"],
    #     data["International Students Ratio Score"],
    #     data["Graduate Employment Rate Score"],
    #     c=data["Cluster"],
    #     cmap= custom_cmap,
    #     alpha=0.7,
    #     edgecolor="k"
    # )
    # ax.set_xlabel("Academic Reputation Score")
    # ax.set_ylabel("International Students Ratio Score")
    # ax.set_zlabel("Graduate Employment Rate Score")
    
    # ax.set_title("Clustering of Universities")
    # ax.scatter3d(
    #     features["Academic Reputation Score"],
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
    
 
    data = recode_the_cols(data) # Creating 3 new columns with encoded to perform our clustering

    # Include more features in clustering
    clustering_features = data[[
        "Academic Reputation Score Encoded",
        "International Students Ratio Score Encoded",
        "Graduate Employment Rate Score Encoded"
    ]]
    
    data = recode_the_cols(data)

    scaler = StandardScaler()
    # scaled_features = scaler.fit_transform(clustering_features) # Not need for clustering

    num_of_clusters = 25 

    kmeans = KMeans(n_clusters=num_of_clusters, random_state=42)
    data["Cluster"] = kmeans.fit_predict(clustering_features)

    # Scale user input
    if user_text:
        features_encoded = recode_the_cols(pd.DataFrame([features]))
        
        selected_features_encoded = features_encoded[[
        "Academic Reputation Score Encoded",
        "International Students Ratio Score Encoded",
        "Graduate Employment Rate Score Encoded"
        ]]
        
        print(selected_features_encoded)

        user_cluster = kmeans.predict(selected_features_encoded)[0]
        

        # Filter by cluster and country
        filtered_data = data[data["Cluster"] == user_cluster]
            
        
        if features["Country"]:
            filtered_data_country = filtered_data[filtered_data["Country"].str.contains(features["Country"], case=False)]
            
            if len(filtered_data_country) > 0:
                filtered_data = filtered_data_country
            else:
                st.write("Unfortunately, no schools are available for your selected preference scores but below are other 3 schools in different countries you can consider!")
                
        # Recommend top universities based on clustering
        top_universities = filtered_data.sort_values(
            by=["Academic Reputation Score", "International Students Ratio Score", "Graduate Employment Rate Score"], 
            ascending=False
        ).head(3)

        st.write(f"Top universities for your preferences (Cluster {user_cluster}):")
        st.dataframe(top_universities[["University Name", "Country", "Academic Reputation Score","International Students Ratio Score","Graduate Employment Rate Score"]])



    # IV - Plot Cluster Graph
    st.subheader("Cluster Visualization")

    data["Size"] = 2

    # Create 3D scatter plot with Plotly
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
    # # Add centroids
    centroids = kmeans.cluster_centers_[:3]
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