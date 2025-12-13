"""
Page 1: University Discovery & Matching
Smart recommendations with ML clustering and advanced filtering
"""
import streamlit as st
import pandas as pd
import numpy as np
import re
from sklearn.cluster import KMeans
import plotly.express as px
import random

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))

from utils import (
    set_page_config,
    apply_custom_css,
    display_logo,
    display_footer,
    load_university_data,
    get_gemini_model,
    recode_columns,
    initialize_session_state,
    format_country_list,
    GOLD, BLUE_DARK, BLUE_MEDIUM, BLUE_LIGHT, WHITE, GOLD_LIGHT
)

# Page configuration
set_page_config(page_title="Discovery & Matching")
apply_custom_css()
initialize_session_state()

# Display logo
display_logo()

st.markdown(f"<h1 style='color: {GOLD}; text-align: center;'>🎯 University Discovery & Matching</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color: {WHITE}; text-align: center; font-size: 1.1rem;'>Find universities that match your preferences using AI-powered recommendations</p>", unsafe_allow_html=True)

# Load data
data = load_university_data()
gemini_model = get_gemini_model()

if data is None:
    st.error("Failed to load university data. Please check the dataset path.")
    st.stop()

# Create tabs for different input methods
tab1, tab2 = st.tabs(["💬 Natural Language", "🔧 Advanced Filters"])

with tab1:
    st.markdown(f"<h3 style='color: {GOLD};'>Describe Your Ideal University</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {WHITE};'>Tell us what you're looking for in natural language, and we'll find the best matches!</p>", unsafe_allow_html=True)

    user_text = st.text_area(
        "Your preferences:",
        placeholder="E.g., I want a university in the United States with a high academic reputation of 90, international student diversity of 85 and good employment rates around 80.",
        height=100,
        key="natural_language_input"
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        find_universities_btn = st.button("🔍 Find Universities", key="find_btn", use_container_width=True)

with tab2:
    st.markdown(f"<h3 style='color: {GOLD};'>Use Advanced Filters</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox(
            "Country (Optional)",
            ["Any Country"] + format_country_list(data),
            key="country_filter"
        )

        academic_rep = st.slider(
            "Academic Reputation Score",
            0, 100, 70,
            help="Higher scores indicate better academic reputation",
            key="academic_slider"
        )

    with col2:
        intl_students = st.slider(
            "International Student Diversity",
            0, 100, 50,
            help="Higher scores indicate more international students",
            key="intl_slider"
        )

        employment = st.slider(
            "Graduate Employment Rate",
            0, 100, 70,
            help="Higher scores indicate better employment outcomes",
            key="employment_slider"
        )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        advanced_search_btn = st.button("🔍 Search with Filters", key="advanced_btn", use_container_width=True)

# Feature extraction function
def extract_features(sentence):
    """Extract features from natural language input using regex"""
    country_pattern = r"university in (?:the )?([A-Za-z\s]+?)(?:\s+with|\s+that)"
    academic_reputation_pattern = r"academic reputation of (\d+)"
    international_students_pattern = r"(?:international student diversity|diversity) of (\d+)"
    employment_rate_pattern = r"employment rates? around (\d+)"

    country_match = re.search(country_pattern, sentence, re.IGNORECASE)
    academic_reputation_match = re.search(academic_reputation_pattern, sentence, re.IGNORECASE)
    international_students_match = re.search(international_students_pattern, sentence, re.IGNORECASE)
    employment_rate_match = re.search(employment_rate_pattern, sentence, re.IGNORECASE)

    extracted_features = {
        "Country": country_match.group(1).strip() if country_match else None,
        "Academic Reputation Score": float(academic_reputation_match.group(1)) if academic_reputation_match else None,
        "International Students Ratio Score": float(international_students_match.group(1)) if international_students_match else None,
        "Graduate Employment Rate Score": float(employment_rate_match.group(1)) if employment_rate_match else None
    }
    return extracted_features

# Process search
features = None
if find_universities_btn and user_text:
    with st.spinner("🔍 Processing your preferences..."):
        features = extract_features(user_text)
        st.session_state.user_preferences = features

elif advanced_search_btn:
    features = {
        "Country": None if country == "Any Country" else country,
        "Academic Reputation Score": float(academic_rep),
        "International Students Ratio Score": float(intl_students),
        "Graduate Employment Rate Score": float(employment)
    }
    st.session_state.user_preferences = features

# Run recommendation if features are available
if features:
    st.markdown("<hr style='border: 1px solid #f0c244; margin: 2rem 0;'>", unsafe_allow_html=True)

    # Display extracted preferences
    st.markdown(f"<h3 style='color: {GOLD};'>Your Preferences</h3>", unsafe_allow_html=True)

    pref_col1, pref_col2, pref_col3, pref_col4 = st.columns(4)

    with pref_col1:
        country_val = features["Country"] if features["Country"] else "Any"
        st.metric("Country", country_val)

    with pref_col2:
        academic_val = features["Academic Reputation Score"] if features["Academic Reputation Score"] else "N/A"
        st.metric("Academic Rep.", academic_val)

    with pref_col3:
        intl_val = features["International Students Ratio Score"] if features["International Students Ratio Score"] else "N/A"
        st.metric("Intl. Diversity", intl_val)

    with pref_col4:
        emp_val = features["Graduate Employment Rate Score"] if features["Graduate Employment Rate Score"] else "N/A"
        st.metric("Employment Rate", emp_val)

    # Clustering Analysis
    with st.spinner("🤖 Running ML clustering analysis..."):
        data_encoded = recode_columns(data.copy())

        clustering_features = data_encoded[[
            "Academic Reputation Score Encoded",
            "International Students Ratio Score Encoded",
            "Graduate Employment Rate Score Encoded"
        ]]

        num_clusters = 25
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        data_encoded["Cluster"] = kmeans.fit_predict(clustering_features)

        # Encode user preferences
        features_df = pd.DataFrame([features])
        features_encoded = recode_columns(features_df)

        selected_features_encoded = features_encoded[[
            "Academic Reputation Score Encoded",
            "International Students Ratio Score Encoded",
            "Graduate Employment Rate Score Encoded"
        ]]

        user_cluster = kmeans.predict(selected_features_encoded)[0]

        # Filter by cluster
        filtered_data = data_encoded[data_encoded["Cluster"] == user_cluster].copy()

        # Filter by country if specified
        if features["Country"]:
            filtered_data_country = filtered_data[
                filtered_data["Country"].str.contains(features["Country"], case=False, na=False)
            ]

            if len(filtered_data_country) > 0:
                filtered_data = filtered_data_country
            else:
                st.warning(f"⚠️ No universities found in {features['Country']} matching your preferences. Showing similar universities from other countries.")

        # Get top recommendations
        top_universities = filtered_data.sort_values(
            by=["Academic Reputation Score", "International Students Ratio Score", "Graduate Employment Rate Score"],
            ascending=False
        ).head(5)

        st.session_state.recommended_universities = top_universities

    # Display Results
    st.markdown(f"<h2 style='color: {GOLD}; margin-top: 2rem;'>🎓 Top Recommended Universities (Cluster {user_cluster})</h2>", unsafe_allow_html=True)

    if len(top_universities) > 0:
        # Summary cards
        for idx, (index, row) in enumerate(top_universities.iterrows(), 1):
            with st.expander(f"#{idx} - {row['University Name']} ({row['Country']})", expanded=(idx == 1)):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Academic Reputation",
                        f"{row['Academic Reputation Score']:.1f}",
                        help="Score out of 100"
                    )

                with col2:
                    st.metric(
                        "International Diversity",
                        f"{row['International Students Ratio Score']:.1f}",
                        help="Score out of 100"
                    )

                with col3:
                    st.metric(
                        "Employment Rate",
                        f"{row['Graduate Employment Rate Score']:.1f}",
                        help="Score out of 100"
                    )

                # Action buttons
                btn_col1, btn_col2, btn_col3 = st.columns(3)

                with btn_col1:
                    if st.button(f"📋 Add to Journey", key=f"journey_{index}"):
                        st.success(f"Added {row['University Name']} to your Application Journey!")

                with btn_col2:
                    if st.button(f"⭐ Bookmark", key=f"bookmark_{index}"):
                        if row['University Name'] not in st.session_state.bookmarked_universities:
                            st.session_state.bookmarked_universities.append(row['University Name'])
                            st.success(f"Bookmarked {row['University Name']}!")

                with btn_col3:
                    if st.button(f"🔍 Get AI Insights", key=f"ai_{index}"):
                        with st.spinner(f"Fetching insights for {row['University Name']}..."):
                            if gemini_model:
                                query = f"""Provide a brief overview (3-4 sentences) of {row['University Name']} highlighting:
                                1. What makes it unique for international students
                                2. Its strongest academic programs
                                3. Campus culture and student life"""

                                try:
                                    response = gemini_model.generate_content(query)
                                    st.info(response.text)
                                except Exception as e:
                                    st.error(f"Error fetching AI insights: {e}")

        # Detailed comparison table
        st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>📊 Detailed Comparison</h3>", unsafe_allow_html=True)

        comparison_df = top_universities[[
            "University Name",
            "Country",
            "World Rank",
            "Academic Reputation Score",
            "Employer Reputation Score",
            "International Students Ratio Score",
            "Graduate Employment Rate Score",
            "Faculty Research Output Score"
        ]].reset_index(drop=True)

        st.dataframe(comparison_df, use_container_width=True, height=400)

    else:
        st.warning("No universities found matching your criteria. Please try different preferences.")

    # Visualization
    st.markdown(f"<h2 style='color: {GOLD}; margin-top: 3rem;'>📈 Cluster Visualization</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {WHITE};'>3D visualization showing all universities across key metrics. Your cluster is highlighted.</p>", unsafe_allow_html=True)

    # Prepare visualization data
    viz_data = data_encoded.copy()
    viz_data["Size"] = 5
    viz_data.loc[viz_data["Cluster"] == user_cluster, "Size"] = 15
    viz_data["Is Your Cluster"] = viz_data["Cluster"] == user_cluster

    # Generate cluster names and colors
    cluster_names = [f"Cluster {i}" for i in range(num_clusters)]
    colors = [f"#{''.join(random.choices('0123456789ABCDEF', k=6))}" for _ in range(num_clusters)]

    # Highlight user cluster in gold
    colors[user_cluster] = GOLD

    color_discrete_map = {name: color for name, color in zip(cluster_names, colors)}
    viz_data['Cluster Name'] = viz_data['Cluster'].map({i: name for i, name in enumerate(cluster_names)})

    # Create 3D scatter plot
    fig = px.scatter_3d(
        viz_data,
        x='Academic Reputation Score',
        y='International Students Ratio Score',
        z='Graduate Employment Rate Score',
        color='Cluster Name',
        size='Size',
        hover_data=['University Name', 'Country'],
        title="3D University Landscape by Key Metrics",
        color_discrete_map=color_discrete_map,
        opacity=0.7
    )

    fig.update_layout(
        scene=dict(
            xaxis_title="Academic Reputation",
            yaxis_title="International Diversity",
            zaxis_title="Employment Rate"
        ),
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)

# Footer
display_footer()
