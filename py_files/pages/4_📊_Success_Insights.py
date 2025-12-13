"""
Page 4: Success Insights Dashboard
Analyze acceptance rates, competitiveness, and admission trends
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    initialize_session_state,
    format_country_list,
    GOLD, BLUE_DARK, BLUE_MEDIUM, BLUE_LIGHT, WHITE, GOLD_LIGHT
)

# Page configuration
set_page_config(page_title="Success Insights")
apply_custom_css()
initialize_session_state()

# Display logo
display_logo()

st.markdown(f"<h1 style='color: {GOLD}; text-align: center;'>📊 Success Insights Dashboard</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color: {WHITE}; text-align: center; font-size: 1.1rem;'>Data-driven insights to maximize your application success</p>", unsafe_allow_html=True)

# Load data
data = load_university_data()
gemini_model = get_gemini_model()

if data is None:
    st.error("Failed to load university data.")
    st.stop()

# Tabs for different insights
tab1, tab2, tab3, tab4 = st.tabs(["🌍 Global Trends", "🎯 Competitiveness Analysis", "📈 Program Insights", "🤖 AI Success Predictor"])

# Tab 1: Global Trends
with tab1:
    st.markdown(f"<h2 style='color: {GOLD};'>Global University Landscape</h2>", unsafe_allow_html=True)

    # Top countries by number of ranked universities
    st.markdown(f"<h3 style='color: {GOLD};'>Top Countries by Number of Ranked Universities</h3>", unsafe_allow_html=True)

    country_counts = data['Country'].value_counts().head(15).reset_index()
    country_counts.columns = ['Country', 'Number of Universities']

    fig_countries = px.bar(
        country_counts,
        x='Country',
        y='Number of Universities',
        title='Top 15 Countries with Most Ranked Universities',
        color='Number of Universities',
        color_continuous_scale='YlOrBr'
    )
    fig_countries.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=WHITE),
        showlegend=False
    )
    st.plotly_chart(fig_countries, use_container_width=True)

    # Score distributions
    st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>Score Distributions Across All Universities</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        avg_academic = data['Academic Reputation Score'].mean()
        median_academic = data['Academic Reputation Score'].median()
        st.metric(
            "Academic Reputation",
            f"{avg_academic:.1f}",
            delta=f"Median: {median_academic:.1f}"
        )

    with col2:
        avg_intl = data['International Students Ratio Score'].mean()
        median_intl = data['International Students Ratio Score'].median()
        st.metric(
            "Intl. Student Diversity",
            f"{avg_intl:.1f}",
            delta=f"Median: {median_intl:.1f}"
        )

    with col3:
        avg_emp = data['Graduate Employment Rate Score'].mean()
        median_emp = data['Graduate Employment Rate Score'].median()
        st.metric(
            "Employment Rate",
            f"{avg_emp:.1f}",
            delta=f"Median: {median_emp:.1f}"
        )

    # Distribution histograms
    fig_dist = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Academic Reputation', 'International Diversity', 'Employment Rate')
    )

    fig_dist.add_trace(
        go.Histogram(x=data['Academic Reputation Score'], name='Academic Rep', marker_color=GOLD),
        row=1, col=1
    )
    fig_dist.add_trace(
        go.Histogram(x=data['International Students Ratio Score'], name='Intl. Students', marker_color='#ff6b6b'),
        row=1, col=2
    )
    fig_dist.add_trace(
        go.Histogram(x=data['Graduate Employment Rate Score'], name='Employment', marker_color='#51cf66'),
        row=1, col=3
    )

    fig_dist.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=WHITE)
    )
    st.plotly_chart(fig_dist, use_container_width=True)

    # Regional analysis
    st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>Regional Performance Analysis</h3>", unsafe_allow_html=True)

    selected_countries = st.multiselect(
        "Select countries to compare:",
        format_country_list(data),
        default=['United States', 'United Kingdom', 'Canada', 'Australia'] if all(c in data['Country'].values for c in ['United States', 'United Kingdom', 'Canada', 'Australia']) else data['Country'].value_counts().head(4).index.tolist(),
        key="country_compare"
    )

    if selected_countries:
        filtered_data = data[data['Country'].isin(selected_countries)]

        country_metrics = filtered_data.groupby('Country').agg({
            'Academic Reputation Score': 'mean',
            'International Students Ratio Score': 'mean',
            'Graduate Employment Rate Score': 'mean'
        }).reset_index()

        country_metrics_melted = country_metrics.melt(
            id_vars='Country',
            value_vars=['Academic Reputation Score', 'International Students Ratio Score', 'Graduate Employment Rate Score'],
            var_name='Metric',
            value_name='Score'
        )

        fig_regional = px.bar(
            country_metrics_melted,
            x='Country',
            y='Score',
            color='Metric',
            barmode='group',
            title='Average Scores by Country',
            color_discrete_map={
                'Academic Reputation Score': GOLD,
                'International Students Ratio Score': '#ff6b6b',
                'Graduate Employment Rate Score': '#51cf66'
            }
        )
        fig_regional.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=WHITE)
        )
        st.plotly_chart(fig_regional, use_container_width=True)

# Tab 2: Competitiveness Analysis
with tab2:
    st.markdown(f"<h2 style='color: {GOLD};'>University Competitiveness Analysis</h2>", unsafe_allow_html=True)

    st.markdown(f"<p style='color: {WHITE};'>Understand how competitive different universities are based on their scores and rankings.</p>", unsafe_allow_html=True)

    # Competitiveness tiers
    st.markdown(f"<h3 style='color: {GOLD};'>Competitiveness Tiers</h3>", unsafe_allow_html=True)

    # Create competitiveness score (composite of the three key metrics)
    data_comp = data.copy()
    data_comp['Competitiveness Score'] = (
        data_comp['Academic Reputation Score'] * 0.4 +
        data_comp['International Students Ratio Score'] * 0.2 +
        data_comp['Graduate Employment Rate Score'] * 0.4
    )

    # Define tiers
    def get_tier(score):
        if score >= 80:
            return "Highly Competitive"
        elif score >= 60:
            return "Very Competitive"
        elif score >= 40:
            return "Competitive"
        elif score >= 20:
            return "Moderately Competitive"
        else:
            return "Less Competitive"

    data_comp['Tier'] = data_comp['Competitiveness Score'].apply(get_tier)

    # Tier distribution
    tier_counts = data_comp['Tier'].value_counts().reset_index()
    tier_counts.columns = ['Tier', 'Count']

    # Define tier order
    tier_order = ["Highly Competitive", "Very Competitive", "Competitive", "Moderately Competitive", "Less Competitive"]
    tier_counts['Tier'] = pd.Categorical(tier_counts['Tier'], categories=tier_order, ordered=True)
    tier_counts = tier_counts.sort_values('Tier')

    col1, col2 = st.columns([1, 2])

    with col1:
        for _, row in tier_counts.iterrows():
            st.metric(row['Tier'], row['Count'])

    with col2:
        fig_tiers = px.pie(
            tier_counts,
            values='Count',
            names='Tier',
            title='Distribution of Universities by Competitiveness',
            color_discrete_sequence=px.colors.sequential.YlOrRd
        )
        fig_tiers.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=WHITE)
        )
        st.plotly_chart(fig_tiers, use_container_width=True)

    # Top competitive universities
    st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>Top 20 Most Competitive Universities</h3>", unsafe_allow_html=True)

    top_competitive = data_comp.nlargest(20, 'Competitiveness Score')[[
        'University Name',
        'Country',
        'World Rank',
        'Academic Reputation Score',
        'International Students Ratio Score',
        'Graduate Employment Rate Score',
        'Competitiveness Score',
        'Tier'
    ]].reset_index(drop=True)

    st.dataframe(top_competitive, use_container_width=True, height=400)

    # Acceptance rate estimator (AI-powered)
    st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>Get Acceptance Rate Insights</h3>", unsafe_allow_html=True)

    university_for_acceptance = st.selectbox(
        "Select a university:",
        data['University Name'].unique(),
        key="acceptance_uni"
    )

    if st.button("📊 Get Acceptance Insights", key="acceptance_btn"):
        with st.spinner(f"Fetching acceptance insights for {university_for_acceptance}..."):
            if gemini_model:
                acceptance_query = f"""
                Provide detailed acceptance and admissions information for {university_for_acceptance}:

                1. Approximate acceptance rate (undergraduate and graduate if different)
                2. What makes this university competitive
                3. Typical admitted student profile (test scores, GPA, achievements)
                4. Tips for standing out in applications
                5. International student acceptance trends (if applicable)

                Be specific and factual. If exact numbers aren't known, provide ranges or recent estimates.
                """

                try:
                    response = gemini_model.generate_content(acceptance_query)
                    st.markdown(f"""
                    <div class="university-card">
                        <h3 style='color: {GOLD};'>Acceptance Insights: {university_for_acceptance}</h3>
                        <div style='color: {WHITE};'>{response.text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# Tab 3: Program Insights
with tab3:
    st.markdown(f"<h2 style='color: {GOLD};'>Program-Specific Insights</h2>", unsafe_allow_html=True)

    st.markdown(f"<p style='color: {WHITE};'>Get detailed insights about specific programs and their competitiveness.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        program_university = st.selectbox(
            "Select University:",
            data['University Name'].unique(),
            key="program_uni"
        )

    with col2:
        program_field = st.selectbox(
            "Field of Study:",
            [
                "Computer Science / Engineering",
                "Business / MBA",
                "Medicine / Healthcare",
                "Law",
                "Natural Sciences",
                "Social Sciences",
                "Arts / Humanities",
                "Engineering (Other)",
                "Education",
                "Public Policy / International Affairs"
            ],
            key="program_field"
        )

    program_level = st.radio(
        "Program Level:",
        ["Undergraduate", "Master's", "PhD"],
        horizontal=True,
        key="program_level"
    )

    if st.button("🔍 Get Program Insights", key="program_insights_btn"):
        with st.spinner(f"Fetching insights for {program_field} at {program_university}..."):
            if gemini_model:
                program_query = f"""
                Provide comprehensive information about {program_field} {program_level} programs at {program_university}:

                1. Program Rankings and Reputation
                   - National/global ranking in this field
                   - What makes this program stand out

                2. Competitiveness
                   - Approximate acceptance rate for this specific program
                   - Typical admitted student profile
                   - Application requirements unique to this program

                3. Career Outcomes
                   - Graduate employment rate in this field
                   - Top employers/career paths
                   - Average starting salaries

                4. Research Opportunities (if graduate program)
                   - Notable research areas
                   - Faculty expertise
                   - Funding opportunities

                5. International Student Perspective
                   - International student percentage in this program
                   - Support for international students
                   - Visa/work opportunities post-graduation

                Be specific and data-driven where possible.
                """

                try:
                    response = gemini_model.generate_content(program_query)
                    st.markdown(f"""
                    <div class="university-card">
                        <h3 style='color: {GOLD};'>{program_field} at {program_university}</h3>
                        <p style='color: {WHITE}; opacity: 0.8;'>Program Level: {program_level}</p>
                        <div style='color: {WHITE};'>{response.text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

    # Field comparison
    st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>Compare Programs Across Universities</h3>", unsafe_allow_html=True)

    compare_field = st.selectbox(
        "Field to Compare:",
        [
            "Computer Science",
            "Business / MBA",
            "Engineering",
            "Medicine",
            "Law",
            "Sciences",
            "Humanities"
        ],
        key="compare_field"
    )

    compare_unis = st.multiselect(
        "Select Universities (max 5):",
        data['University Name'].unique(),
        max_selections=5,
        key="compare_unis"
    )

    if compare_unis and st.button("📊 Compare Programs", key="compare_btn"):
        with st.spinner("Generating comparison..."):
            if gemini_model:
                compare_query = f"""
                Create a detailed comparison table for {compare_field} programs at these universities:
                {', '.join(compare_unis)}

                Include:
                - Program ranking/reputation
                - Acceptance rate/competitiveness
                - Key strengths/specializations
                - Notable faculty or research
                - Career outcomes
                - International student friendliness

                Format as a comparison that helps a student make an informed decision.
                """

                try:
                    response = gemini_model.generate_content(compare_query)
                    st.markdown(f"""
                    <div class="university-card">
                        <h3 style='color: {GOLD};'>{compare_field} Program Comparison</h3>
                        <div style='color: {WHITE};'>{response.text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# Tab 4: AI Success Predictor
with tab4:
    st.markdown(f"<h2 style='color: {GOLD};'>AI-Powered Success Predictor</h2>", unsafe_allow_html=True)

    st.markdown(f"<p style='color: {WHITE};'>Get personalized insights on your chances of admission based on your profile.</p>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="university-card">
        <p style='color: {WHITE}; font-size: 1.05rem;'>
            <strong>Note:</strong> This is an AI-powered estimate for guidance purposes only.
            Actual admission decisions depend on many factors and vary by institution.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h3 style='color: {GOLD};'>Academic Profile</h3>", unsafe_allow_html=True)

        gpa = st.number_input(
            "GPA (4.0 scale)",
            min_value=0.0,
            max_value=4.0,
            value=3.5,
            step=0.1,
            key="gpa"
        )

        test_score = st.number_input(
            "Test Score (SAT: 1600 scale, GRE: 340 scale, or percentile)",
            min_value=0,
            max_value=1600,
            value=1400,
            help="Enter SAT (out of 1600), GRE (out of 340), or percentile",
            key="test_score"
        )

        english_proficiency = st.selectbox(
            "English Proficiency",
            ["Native Speaker", "TOEFL 110+", "TOEFL 100-109", "TOEFL 90-99", "TOEFL 80-89", "IELTS 7.5+", "IELTS 7.0-7.5", "IELTS 6.5-7.0"],
            key="english"
        )

    with col2:
        st.markdown(f"<h3 style='color: {GOLD};'>Experience & Activities</h3>", unsafe_allow_html=True)

        extracurriculars = st.multiselect(
            "Extracurricular Activities",
            ["Leadership Positions", "Research Experience", "Internships", "Volunteer Work", "Sports/Athletics", "Arts/Music", "Entrepreneurship", "Publications/Awards"],
            key="extracurriculars"
        )

        work_experience = st.number_input(
            "Work Experience (years)",
            min_value=0,
            max_value=20,
            value=0,
            key="work_exp"
        )

        unique_achievements = st.text_area(
            "Unique Achievements or Awards",
            placeholder="E.g., National olympiad medal, published research, startup founder, etc.",
            key="achievements"
        )

    target_university = st.selectbox(
        "Target University:",
        data['University Name'].unique(),
        key="target_uni"
    )

    target_program = st.text_input(
        "Target Program:",
        placeholder="E.g., Computer Science, MBA, etc.",
        key="target_program"
    )

    if st.button("🎯 Predict My Chances", key="predict_btn"):
        with st.spinner("Analyzing your profile..."):
            if gemini_model and target_program:
                prediction_query = f"""
                Analyze the admission chances for this student profile applying to {target_program} at {target_university}:

                Academic Profile:
                - GPA: {gpa}/4.0
                - Test Score: {test_score}
                - English Proficiency: {english_proficiency}

                Experience:
                - Extracurriculars: {', '.join(extracurriculars) if extracurriculars else 'None specified'}
                - Work Experience: {work_experience} years
                - Unique Achievements: {unique_achievements if unique_achievements else 'None specified'}

                Provide:
                1. Estimated admission probability (Reach/Target/Safety)
                2. Strengths of this profile
                3. Areas that could be improved
                4. Specific recommendations to strengthen the application
                5. How this profile compares to typical admitted students

                Be honest but encouraging. Provide actionable advice.
                """

                try:
                    response = gemini_model.generate_content(prediction_query)
                    st.markdown(f"""
                    <div class="university-card">
                        <h3 style='color: {GOLD};'>Your Admission Chances: {target_program} at {target_university}</h3>
                        <div style='color: {WHITE};'>{response.text}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Additional recommendations
                    st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>Get Alternative Recommendations</h3>", unsafe_allow_html=True)

                    if st.button("🎓 Find Similar Universities", key="similar_btn"):
                        similar_query = f"""
                        Based on this student profile, recommend 5 alternative universities for {target_program} that would be good matches.

                        Include a mix of:
                        - 2 reach schools (ambitious but possible)
                        - 2 target schools (good fit)
                        - 1 safety school (likely admission)

                        For each, briefly explain why it's a good match.
                        """

                        with st.spinner("Finding alternatives..."):
                            try:
                                similar_response = gemini_model.generate_content(similar_query)
                                st.markdown(f"""
                                <div class="university-card">
                                    <div style='color: {WHITE};'>{similar_response.text}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"Error: {e}")

                except Exception as e:
                    st.error(f"Error: {e}")

# Footer
display_footer()
