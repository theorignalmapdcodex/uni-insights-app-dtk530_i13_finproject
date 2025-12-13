"""
Page 2: Application Journey Planner
Personalized timeline and checklist for university applications
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))

from utils import (
    set_page_config,
    apply_custom_css,
    display_logo,
    display_footer,
    initialize_session_state,
    get_gemini_model,
    GOLD, BLUE_DARK, BLUE_MEDIUM, BLUE_LIGHT, WHITE, GOLD_LIGHT
)

# Page configuration
set_page_config(page_title="Application Journey")
apply_custom_css()
initialize_session_state()

# Display logo
display_logo()

st.markdown(f"<h1 style='color: {GOLD}; text-align: center;'>📋 Application Journey Planner</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color: {WHITE}; text-align: center; font-size: 1.1rem;'>Your personalized roadmap from application to enrollment</p>", unsafe_allow_html=True)

# Initialize journey-specific session state
if 'journey_universities' not in st.session_state:
    st.session_state.journey_universities = []

if 'timeline_tasks' not in st.session_state:
    st.session_state.timeline_tasks = {}

# Get Gemini model
gemini_model = get_gemini_model()

# Step 1: Select Universities
st.markdown(f"<h2 style='color: {GOLD};'>Step 1: Select Your Target Universities</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    university_input = st.text_input(
        "Add a university to your journey:",
        placeholder="E.g., Stanford University",
        key="add_university"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Add University", key="add_uni_btn"):
        if university_input and university_input not in st.session_state.journey_universities:
            st.session_state.journey_universities.append(university_input)
            st.success(f"Added {university_input} to your journey!")
        elif university_input in st.session_state.journey_universities:
            st.warning("This university is already in your list!")

# Display selected universities
if st.session_state.journey_universities:
    st.markdown(f"<h3 style='color: {GOLD};'>Your Selected Universities ({len(st.session_state.journey_universities)})</h3>", unsafe_allow_html=True)

    for idx, uni in enumerate(st.session_state.journey_universities):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"<p style='color: {WHITE}; font-size: 1.1rem;'>✅ {uni}</p>", unsafe_allow_html=True)
        with col2:
            if st.button("🗑️ Remove", key=f"remove_{idx}"):
                st.session_state.journey_universities.remove(uni)
                st.rerun()

    st.markdown("<hr style='border: 1px solid #f0c244; margin: 2rem 0;'>", unsafe_allow_html=True)

    # Step 2: Application Timeline
    st.markdown(f"<h2 style='color: {GOLD};'>Step 2: Set Your Application Timeline</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        application_season = st.selectbox(
            "Application Season",
            ["Fall 2025", "Spring 2026", "Fall 2026", "Spring 2027"],
            key="app_season"
        )

    with col2:
        degree_type = st.selectbox(
            "Degree Type",
            ["Undergraduate", "Graduate (Master's)", "Graduate (PhD)"],
            key="degree_type"
        )

    if st.button("🗓️ Generate Timeline", key="gen_timeline"):
        with st.spinner("Creating your personalized timeline..."):
            # Generate timeline with AI
            if gemini_model:
                timeline_query = f"""
                Create a detailed month-by-month application timeline for a {degree_type} student applying to universities for {application_season}.
                Include:
                1. Key milestones (testing, document preparation, application submission, decisions)
                2. Recommended actions for each month
                3. Critical deadlines to watch for

                Format as a structured timeline starting from 12 months before the application deadline.
                Keep each month's description concise (2-3 bullet points).
                """

                try:
                    response = gemini_model.generate_content(timeline_query)
                    st.session_state.timeline_generated = response.text
                except Exception as e:
                    st.error(f"Error generating timeline: {e}")

    # Display generated timeline
    if 'timeline_generated' in st.session_state:
        st.markdown(f"<h3 style='color: {GOLD};'>Your Personalized Timeline</h3>", unsafe_allow_html=True)

        with st.expander("📅 View Full Timeline", expanded=True):
            st.markdown(f"<div style='color: {WHITE};'>{st.session_state.timeline_generated}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border: 1px solid #f0c244; margin: 2rem 0;'>", unsafe_allow_html=True)

    # Step 3: Document Checklist
    st.markdown(f"<h2 style='color: {GOLD};'>Step 3: Application Document Checklist</h2>", unsafe_allow_html=True)

    # Standard checklist items
    checklist_items = {
        "Transcripts": [
            "Official high school transcripts (if undergrad)",
            "Official undergraduate transcripts (if grad)",
            "Transcript evaluation/translation (if from non-US institution)",
        ],
        "Test Scores": [
            "Standardized test (SAT/ACT for undergrad, GRE/GMAT for grad)",
            "English proficiency (TOEFL/IELTS/Duolingo)",
            "Subject-specific tests (if required)",
        ],
        "Essays & Writing": [
            "Personal statement / Statement of Purpose",
            "Supplemental essays (vary by university)",
            "Writing samples (if required for grad programs)",
        ],
        "Recommendations": [
            "Letters of recommendation (typically 2-3)",
            "Resume/CV",
            "List of recommenders with contact info",
        ],
        "Financial Documents": [
            "Bank statements / Proof of financial support",
            "Scholarship/funding applications",
            "CSS Profile / FAFSA (if applicable)",
        ],
        "Application Forms": [
            "Common App / Coalition App / University-specific application",
            "Application fee or fee waiver documentation",
            "Portfolio (if applying for arts/design programs)",
        ]
    }

    # Create interactive checklist
    for category, items in checklist_items.items():
        with st.expander(f"📁 {category}", expanded=False):
            for item in items:
                checkbox_key = f"check_{category}_{item}"
                if checkbox_key not in st.session_state:
                    st.session_state[checkbox_key] = False

                is_checked = st.checkbox(
                    item,
                    value=st.session_state[checkbox_key],
                    key=checkbox_key
                )

    # Progress tracking
    total_items = sum(len(items) for items in checklist_items.values())
    completed_items = sum(
        1 for category, items in checklist_items.items()
        for item in items
        if st.session_state.get(f"check_{category}_{item}", False)
    )

    progress_pct = (completed_items / total_items) * 100 if total_items > 0 else 0

    st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>Overall Progress</h3>", unsafe_allow_html=True)
    st.progress(progress_pct / 100)
    st.markdown(f"<p style='color: {WHITE}; font-size: 1.2rem; text-align: center;'>{completed_items} of {total_items} items completed ({progress_pct:.1f}%)</p>", unsafe_allow_html=True)

    st.markdown("<hr style='border: 1px solid #f0c244; margin: 2rem 0;'>", unsafe_allow_html=True)

    # Step 4: Deadline Tracker
    st.markdown(f"<h2 style='color: {GOLD};'>Step 4: Deadline Tracker</h2>", unsafe_allow_html=True)

    st.markdown(f"<p style='color: {WHITE};'>Set application deadlines for each university to stay organized.</p>", unsafe_allow_html=True)

    for uni in st.session_state.journey_universities:
        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            st.markdown(f"<p style='color: {WHITE}; font-size: 1.1rem; padding-top: 0.5rem;'>{uni}</p>", unsafe_allow_html=True)

        with col2:
            deadline_key = f"deadline_{uni}"
            deadline = st.date_input(
                "Application Deadline",
                key=deadline_key,
                label_visibility="collapsed"
            )

            if deadline:
                st.session_state.application_deadlines[uni] = deadline

        with col3:
            if uni in st.session_state.application_deadlines:
                days_until = (st.session_state.application_deadlines[uni] - datetime.now().date()).days
                if days_until > 30:
                    st.success(f"{days_until} days")
                elif days_until > 7:
                    st.warning(f"{days_until} days")
                else:
                    st.error(f"{days_until} days")

    # Deadline summary
    if st.session_state.application_deadlines:
        st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>Upcoming Deadlines</h3>", unsafe_allow_html=True)

        deadlines_sorted = sorted(
            st.session_state.application_deadlines.items(),
            key=lambda x: x[1]
        )

        for uni, deadline in deadlines_sorted[:5]:
            days_until = (deadline - datetime.now().date()).days
            st.markdown(f"""
            <div class="university-card">
                <p style='color: {GOLD}; font-weight: bold; margin: 0;'>{uni}</p>
                <p style='color: {WHITE}; margin: 0;'>Deadline: {deadline.strftime('%B %d, %Y')} ({days_until} days remaining)</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='border: 1px solid #f0c244; margin: 2rem 0;'>", unsafe_allow_html=True)

    # Step 5: AI-Powered Application Tips
    st.markdown(f"<h2 style='color: {GOLD};'>Step 5: Get Personalized Application Tips</h2>", unsafe_allow_html=True)

    selected_uni_for_tips = st.selectbox(
        "Select a university for personalized tips:",
        st.session_state.journey_universities,
        key="tips_uni"
    )

    if st.button("💡 Get Application Tips", key="get_tips"):
        with st.spinner(f"Generating tips for {selected_uni_for_tips}..."):
            if gemini_model:
                tips_query = f"""
                Provide detailed application tips for a {degree_type} student applying to {selected_uni_for_tips}.
                Include:
                1. What the admissions committee looks for
                2. How to stand out in your application
                3. Common mistakes to avoid
                4. Tips for essays and personal statements
                5. What makes a strong application for this institution

                Keep the response practical and actionable.
                """

                try:
                    response = gemini_model.generate_content(tips_query)
                    st.markdown(f"""
                    <div class="university-card">
                        <h3 style='color: {GOLD};'>Application Tips for {selected_uni_for_tips}</h3>
                        <div style='color: {WHITE};'>{response.text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating tips: {e}")

else:
    # Placeholder when no universities selected
    st.info("👆 Start by adding universities to your application journey above!")

    st.markdown(f"""
    <div class="university-card">
        <h3 style='color: {GOLD};'>Why Use the Application Journey Planner?</h3>
        <ul style='color: {WHITE}; font-size: 1.05rem; line-height: 1.8;'>
            <li><strong>Stay Organized:</strong> Track all your target universities in one place</li>
            <li><strong>Never Miss a Deadline:</strong> Set and monitor application deadlines</li>
            <li><strong>Complete Documentation:</strong> Use our comprehensive checklist to ensure nothing is missed</li>
            <li><strong>Personalized Timeline:</strong> Get a custom timeline based on your application season</li>
            <li><strong>AI-Powered Tips:</strong> Receive institution-specific application advice</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
display_footer()
