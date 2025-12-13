"""
University Recommendation and Insights App - Home Page
Enhancing the University Application Journey for Students Worldwide
"""
import streamlit as st
from utils import (
    set_page_config,
    apply_custom_css,
    display_logo,
    display_footer,
    initialize_session_state,
    GOLD, BLUE_DARK, BLUE_MEDIUM, BLUE_LIGHT, WHITE, GOLD_LIGHT
)

# Page configuration
set_page_config(page_title="University Insights - Home")

# Apply styling
apply_custom_css()

# Initialize session state
initialize_session_state()

# Display logo
display_logo()

# Welcome Section
st.markdown(f"""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: {GOLD}; font-size: 2.5rem; margin-bottom: 1rem;">
        Welcome to University Recommendation & Insights App
    </h1>
    <p style="color: {WHITE}; font-size: 1.2rem; line-height: 1.8;">
        Enhancing the University Application Journey of Undergraduate and Graduate Students All Around the World
    </p>
</div>
""", unsafe_allow_html=True)

# Mission Statement
st.markdown(f"""
<div class="university-card">
    <h2 style="color: {GOLD}; text-align: center;">Our Mission</h2>
    <p style="color: {WHITE}; font-size: 1.1rem; line-height: 1.8; text-align: center;">
        We help international students navigate the complex university application process by providing
        data-driven insights into <strong>application success rates</strong>, <strong>scholarship opportunities</strong>,
        and <strong>institutional criteria</strong> to make informed decisions about their educational future.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Feature Overview
st.markdown(f"<h2 style='color: {GOLD}; text-align: center;'>What We Offer</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="university-card">
        <h3 style="color: {GOLD};">🎯 Smart Discovery</h3>
        <p style="color: {WHITE};">
            Find universities that match your preferences using advanced machine learning clustering.
            Compare institutions side-by-side and make informed decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="university-card">
        <h3 style="color: {GOLD};">📋 Journey Planner</h3>
        <p style="color: {WHITE};">
            Get a personalized application timeline with deadlines, document checklists,
            and step-by-step guidance from selection to enrollment.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="university-card">
        <h3 style="color: {GOLD};">💰 Funding Hub</h3>
        <p style="color: {WHITE};">
            Discover scholarship opportunities, compare costs, calculate ROI,
            and find funding options for your education.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col4, col5 = st.columns(2)

with col4:
    st.markdown(f"""
    <div class="university-card">
        <h3 style="color: {GOLD};">📊 Success Insights</h3>
        <p style="color: {WHITE};">
            Analyze acceptance rates, international student intake trends,
            and program-specific competitiveness to improve your chances.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="university-card">
        <h3 style="color: {GOLD};">🤖 AI Assistant</h3>
        <p style="color: {WHITE};">
            Ask questions and get instant answers powered by Google Gemini AI.
            Context-aware responses based on your selected universities.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# How It Works
st.markdown(f"<h2 style='color: {GOLD}; text-align: center;'>How It Works</h2>", unsafe_allow_html=True)

st.markdown(f"""
<div class="university-card">
    <div style="color: {WHITE}; font-size: 1.1rem; line-height: 2;">
        <p><strong style="color: {GOLD};">Step 1:</strong> Navigate to <strong>🎯 Discovery & Matching</strong> to describe your preferences and get personalized university recommendations.</p>
        <p><strong style="color: {GOLD};">Step 2:</strong> Visit <strong>📋 Application Journey</strong> to create your timeline and track application requirements.</p>
        <p><strong style="color: {GOLD};">Step 3:</strong> Explore <strong>💰 Scholarship Hub</strong> to find funding opportunities and calculate costs.</p>
        <p><strong style="color: {GOLD};">Step 4:</strong> Review <strong>📊 Success Insights</strong> to understand acceptance rates and competitiveness.</p>
        <p><strong style="color: {GOLD};">Step 5:</strong> Use the <strong>🤖 AI Assistant</strong> anytime to get answers to your specific questions.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Research Foundation
st.markdown(f"<h2 style='color: {GOLD}; text-align: center;'>Research-Based Approach</h2>", unsafe_allow_html=True)

st.markdown(f"""
<div class="university-card">
    <p style="color: {WHITE}; font-size: 1.05rem; line-height: 1.8;">
        This application is built on rigorous research leveraging the <strong style="color: {GOLD};">2023 QS World University Ranking Dataset</strong>
        to analyze key factors influencing international student decisions. Our approach combines:
    </p>
    <ul style="color: {WHITE}; font-size: 1.05rem; line-height: 1.8;">
        <li>Machine Learning (K-Means Clustering with 25 clusters)</li>
        <li>Natural Language Processing for smart preference extraction</li>
        <li>Google Gemini AI for enhanced insights and guidance</li>
        <li>Data visualization for better understanding of university landscapes</li>
    </ul>
    <p style="color: {WHITE}; font-size: 1.05rem; line-height: 1.8;">
        Our goal is to provide actionable insights for students navigating the "foreign" application process,
        understand institutional dynamics, and make informed decisions regarding scholarships and school selection.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Call to Action
st.markdown(f"""
<div style="text-align: center; padding: 2rem 0;">
    <h2 style="color: {GOLD};">Ready to Start Your Journey?</h2>
    <p style="color: {WHITE}; font-size: 1.1rem;">
        Select a page from the sidebar to begin exploring your university options!
    </p>
</div>
""", unsafe_allow_html=True)

# Professional Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem 0; border-bottom: 2px solid rgba(240, 194, 68, 0.3); margin-bottom: 1.5rem;">
        <h2 style="color: {GOLD}; margin: 0; font-size: 1.4rem; font-weight: 700;">🎓 University Insights</h2>
        <p style="color: {GOLD_LIGHT}; margin: 0.5rem 0 0 0; font-size: 0.85rem; font-weight: 500;">Your Path to Success</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(26, 95, 168, 0.3) 0%, rgba(7, 55, 99, 0.5) 100%);
                padding: 1.25rem;
                border-radius: 10px;
                margin-bottom: 1.5rem;
                border: 2px solid rgba(240, 194, 68, 0.2);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);">
        <h3 style="color: {GOLD}; margin-top: 0; font-size: 1.1rem; font-weight: 600;">📍 Quick Navigation</h3>
        <p style="color: {WHITE}; font-size: 0.9rem; margin-bottom: 1rem; line-height: 1.6;">
            Select a page from above to begin your university application journey:
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Navigation cards
    nav_items = [
        ("🏠", "Home", "Welcome & Overview"),
        ("🎯", "Discovery & Matching", "Find Your Universities"),
        ("📋", "Application Journey", "Plan Your Timeline"),
        ("💰", "Scholarship Hub", "Find Funding"),
        ("📊", "Success Insights", "Analyze Your Chances"),
        ("🤖", "AI Assistant", "Get Instant Help")
    ]

    for emoji, title, desc in nav_items:
        st.markdown(f"""
        <div style="background-color: rgba(255, 255, 255, 0.05);
                    padding: 0.85rem;
                    border-radius: 8px;
                    margin-bottom: 0.75rem;
                    border-left: 3px solid rgba(240, 194, 68, 0.4);
                    transition: all 0.3s ease;">
            <p style="color: {GOLD}; margin: 0; font-weight: 600; font-size: 0.95rem;">
                {emoji} {title}
            </p>
            <p style="color: {GOLD_LIGHT}; margin: 0.25rem 0 0 0; font-size: 0.8rem;">
                {desc}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick stats or info
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(240, 194, 68, 0.15) 0%, rgba(240, 194, 68, 0.05) 100%);
                padding: 1.25rem;
                border-radius: 10px;
                border: 2px solid rgba(240, 194, 68, 0.3);
                text-align: center;">
        <h4 style="color: {GOLD}; margin: 0 0 0.75rem 0; font-size: 1rem; font-weight: 600;">📊 Dataset Info</h4>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div style="margin: 0.5rem;">
                <p style="color: {GOLD}; font-size: 1.8rem; font-weight: 700; margin: 0;">1,422</p>
                <p style="color: {WHITE}; font-size: 0.75rem; margin: 0;">Universities</p>
            </div>
            <div style="margin: 0.5rem;">
                <p style="color: {GOLD}; font-size: 1.8rem; font-weight: 700; margin: 0;">100+</p>
                <p style="color: {WHITE}; font-size: 0.75rem; margin: 0;">Countries</p>
            </div>
            <div style="margin: 0.5rem;">
                <p style="color: {GOLD}; font-size: 1.8rem; font-weight: 700; margin: 0;">25</p>
                <p style="color: {WHITE}; font-size: 0.75rem; margin: 0;">ML Clusters</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Footer in sidebar
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; border-top: 1px solid rgba(240, 194, 68, 0.2); margin-top: 1rem;">
        <p style="color: {GOLD_LIGHT}; font-size: 0.75rem; margin: 0;">
            Powered by AI & ML
        </p>
        <p style="color: {WHITE}; font-size: 0.7rem; margin: 0.25rem 0 0 0; opacity: 0.7;">
            QS Rankings 2023
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
display_footer()
