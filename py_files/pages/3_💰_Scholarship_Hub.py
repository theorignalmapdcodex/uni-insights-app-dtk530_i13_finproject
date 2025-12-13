"""
Page 3: Scholarship & Funding Hub
Discover funding opportunities and calculate education costs
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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
set_page_config(page_title="Scholarship Hub")
apply_custom_css()
initialize_session_state()

# Display logo
display_logo()

st.markdown(f"<h1 style='color: {GOLD}; text-align: center;'>💰 Scholarship & Funding Hub</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color: {WHITE}; text-align: center; font-size: 1.1rem;'>Find funding opportunities and plan your education investment</p>", unsafe_allow_html=True)

# Get Gemini model
gemini_model = get_gemini_model()

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["🔍 Find Scholarships", "💵 Cost Calculator", "📊 ROI Analysis"])

# Tab 1: Find Scholarships
with tab1:
    st.markdown(f"<h2 style='color: {GOLD};'>Scholarship Finder</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        university_name = st.text_input(
            "University Name",
            placeholder="E.g., Stanford University",
            key="scholarship_uni"
        )

        degree_level = st.selectbox(
            "Degree Level",
            ["Undergraduate", "Master's", "PhD", "All Levels"],
            key="degree_level"
        )

    with col2:
        scholarship_type = st.multiselect(
            "Scholarship Type",
            ["Merit-based", "Need-based", "Athletic", "Diversity", "Field-specific", "International Students"],
            default=["Merit-based", "International Students"],
            key="scholarship_type"
        )

        student_profile = st.selectbox(
            "Student Profile",
            ["International Student", "Domestic Student", "Transfer Student", "First-Generation Student"],
            key="student_profile"
        )

    if st.button("🔍 Search Scholarships", key="search_scholarships"):
        with st.spinner(f"Finding scholarship opportunities for {university_name}..."):
            if gemini_model and university_name:
                scholarship_query = f"""
                List available scholarships and financial aid opportunities for {degree_level} {student_profile}s at {university_name}.

                Focus on: {', '.join(scholarship_type)}

                For each scholarship, provide:
                1. Scholarship name
                2. Amount/Coverage (full tuition, partial, stipend amount)
                3. Eligibility criteria (brief)
                4. Application deadline (if known, or typical timeline)
                5. Key requirements

                Organize by scholarship amount (highest to lowest).
                Include at least 5-7 options if available.
                Be specific and factual.
                """

                try:
                    response = gemini_model.generate_content(scholarship_query)

                    st.markdown(f"""
                    <div class="university-card">
                        <h3 style='color: {GOLD};'>Scholarship Opportunities at {university_name}</h3>
                        <div style='color: {WHITE};'>{response.text}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Additional resources
                    st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>Additional Scholarship Resources</h3>", unsafe_allow_html=True)

                    external_resources = st.button("🌐 Get External Scholarship Resources", key="external_scholarships")

                    if external_resources:
                        external_query = f"""
                        List 8-10 major external scholarship programs available for international students pursuing {degree_level} degrees in the United States.

                        For each, include:
                        - Scholarship name and organization
                        - Award amount
                        - Eligibility (nationality, field of study, etc.)
                        - Website (if widely known)

                        Include Fulbright, Chevening, and other prestigious programs.
                        """

                        with st.spinner("Fetching external scholarship programs..."):
                            try:
                                ext_response = gemini_model.generate_content(external_query)
                                st.markdown(f"""
                                <div class="university-card">
                                    <div style='color: {WHITE};'>{ext_response.text}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"Error: {e}")

                except Exception as e:
                    st.error(f"Error fetching scholarships: {e}")
            else:
                st.warning("Please enter a university name and ensure Gemini is configured.")

    # General scholarship tips
    st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>💡 Scholarship Application Tips</h3>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="university-card">
        <ul style='color: {WHITE}; font-size: 1.05rem; line-height: 1.8;'>
            <li><strong>Start Early:</strong> Many scholarships have deadlines 6-12 months before the academic year</li>
            <li><strong>Apply Broadly:</strong> Don't limit yourself to one scholarship - apply to multiple opportunities</li>
            <li><strong>Tailor Your Essays:</strong> Customize each application to align with the scholarship's mission</li>
            <li><strong>Highlight Unique Qualities:</strong> Emphasize what makes you stand out (leadership, community service, achievements)</li>
            <li><strong>Get Strong Recommendations:</strong> Choose recommenders who know you well and can speak to your strengths</li>
            <li><strong>Check Renewal Requirements:</strong> Understand if scholarships are one-time or renewable (and conditions)</li>
            <li><strong>Watch for Scams:</strong> Legitimate scholarships never require application fees</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Tab 2: Cost Calculator
with tab2:
    st.markdown(f"<h2 style='color: {GOLD};'>Education Cost Calculator</h2>", unsafe_allow_html=True)

    st.markdown(f"<p style='color: {WHITE};'>Estimate your total cost of attendance and plan your budget.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h3 style='color: {GOLD};'>Tuition & Fees</h3>", unsafe_allow_html=True)

        tuition_per_year = st.number_input(
            "Annual Tuition (USD)",
            min_value=0,
            max_value=100000,
            value=50000,
            step=1000,
            key="tuition"
        )

        fees = st.number_input(
            "Annual Fees (USD)",
            min_value=0,
            max_value=10000,
            value=2000,
            step=100,
            key="fees"
        )

        program_duration = st.number_input(
            "Program Duration (years)",
            min_value=1,
            max_value=6,
            value=4,
            key="duration"
        )

    with col2:
        st.markdown(f"<h3 style='color: {GOLD};'>Living Expenses</h3>", unsafe_allow_html=True)

        housing = st.number_input(
            "Annual Housing (USD)",
            min_value=0,
            max_value=30000,
            value=12000,
            step=500,
            key="housing"
        )

        food = st.number_input(
            "Annual Food (USD)",
            min_value=0,
            max_value=15000,
            value=5000,
            step=500,
            key="food"
        )

        other_expenses = st.number_input(
            "Other Annual Expenses (USD)",
            min_value=0,
            max_value=20000,
            value=3000,
            step=500,
            help="Transportation, books, personal expenses, etc.",
            key="other"
        )

    # Funding sources
    st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>Funding Sources</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        scholarships = st.number_input(
            "Annual Scholarships/Grants (USD)",
            min_value=0,
            max_value=100000,
            value=10000,
            step=1000,
            key="scholarships"
        )

        work_study = st.number_input(
            "Annual Work-Study/Part-time (USD)",
            min_value=0,
            max_value=30000,
            value=5000,
            step=500,
            key="work_study"
        )

    with col2:
        family_contribution = st.number_input(
            "Annual Family Contribution (USD)",
            min_value=0,
            max_value=100000,
            value=20000,
            step=1000,
            key="family"
        )

        loans = st.number_input(
            "Annual Loans (USD)",
            min_value=0,
            max_value=100000,
            value=10000,
            step=1000,
            key="loans"
        )

    # Calculate totals
    annual_cost = tuition_per_year + fees + housing + food + other_expenses
    total_cost = annual_cost * program_duration

    annual_funding = scholarships + work_study + family_contribution + loans
    total_funding = annual_funding * program_duration

    annual_gap = annual_cost - annual_funding
    total_gap = total_cost - total_funding

    total_debt = loans * program_duration

    # Display results
    st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>Cost Summary</h3>", unsafe_allow_html=True)

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric("Annual Cost", f"${annual_cost:,.0f}")

    with metric_col2:
        st.metric("Total Cost", f"${total_cost:,.0f}", help=f"{program_duration} years")

    with metric_col3:
        gap_color = "🔴" if annual_gap > 0 else "🟢"
        st.metric("Annual Gap", f"{gap_color} ${abs(annual_gap):,.0f}")

    with metric_col4:
        st.metric("Total Debt", f"${total_debt:,.0f}", help="From loans only")

    # Visualization
    st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>Cost Breakdown</h3>", unsafe_allow_html=True)

    # Cost breakdown pie chart
    cost_data = {
        'Category': ['Tuition', 'Fees', 'Housing', 'Food', 'Other'],
        'Amount': [tuition_per_year, fees, housing, food, other_expenses]
    }
    cost_df = pd.DataFrame(cost_data)

    fig_cost = px.pie(
        cost_df,
        values='Amount',
        names='Category',
        title='Annual Cost Distribution',
        color_discrete_sequence=px.colors.sequential.YlOrRd
    )
    fig_cost.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=WHITE)
    )

    # Funding sources bar chart
    funding_data = {
        'Source': ['Scholarships', 'Work-Study', 'Family', 'Loans'],
        'Amount': [scholarships, work_study, family_contribution, loans]
    }
    funding_df = pd.DataFrame(funding_data)

    fig_funding = px.bar(
        funding_df,
        x='Source',
        y='Amount',
        title='Annual Funding Sources',
        color='Amount',
        color_continuous_scale='YlOrBr'
    )
    fig_funding.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=WHITE),
        showlegend=False
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_cost, use_container_width=True)
    with col2:
        st.plotly_chart(fig_funding, use_container_width=True)

    # 4-year projection
    st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>{program_duration}-Year Financial Projection</h3>", unsafe_allow_html=True)

    years = list(range(1, program_duration + 1))
    cumulative_cost = [annual_cost * i for i in years]
    cumulative_funding = [annual_funding * i for i in years]
    cumulative_debt = [loans * i for i in years]

    fig_projection = go.Figure()

    fig_projection.add_trace(go.Scatter(
        x=years,
        y=cumulative_cost,
        name='Cumulative Cost',
        line=dict(color='#ff6b6b', width=3)
    ))

    fig_projection.add_trace(go.Scatter(
        x=years,
        y=cumulative_funding,
        name='Cumulative Funding',
        line=dict(color='#51cf66', width=3)
    ))

    fig_projection.add_trace(go.Scatter(
        x=years,
        y=cumulative_debt,
        name='Cumulative Debt',
        line=dict(color='#ffd43b', width=3, dash='dash')
    ))

    fig_projection.update_layout(
        title=f'{program_duration}-Year Financial Outlook',
        xaxis_title='Year',
        yaxis_title='Amount (USD)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=WHITE),
        hovermode='x unified'
    )

    st.plotly_chart(fig_projection, use_container_width=True)

# Tab 3: ROI Analysis
with tab3:
    st.markdown(f"<h2 style='color: {GOLD};'>Return on Investment (ROI) Analysis</h2>", unsafe_allow_html=True)

    st.markdown(f"<p style='color: {WHITE};'>Analyze the financial return on your education investment.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        total_investment = st.number_input(
            "Total Education Investment (USD)",
            min_value=0,
            max_value=500000,
            value=int(total_cost),
            step=5000,
            help="Use the cost calculator tab to estimate this",
            key="investment"
        )

        expected_salary = st.number_input(
            "Expected Starting Salary (USD/year)",
            min_value=0,
            max_value=300000,
            value=70000,
            step=5000,
            key="salary"
        )

    with col2:
        salary_growth = st.slider(
            "Expected Annual Salary Growth (%)",
            0, 15, 5,
            help="Average salary increase per year",
            key="growth"
        )

        career_years = st.number_input(
            "Career Duration (years)",
            min_value=1,
            max_value=40,
            value=30,
            key="career_years"
        )

    # Calculate ROI
    if st.button("📊 Calculate ROI", key="calc_roi"):
        # Calculate cumulative earnings
        cumulative_earnings = []
        salary = expected_salary
        total_earnings = 0

        for year in range(1, career_years + 1):
            total_earnings += salary
            cumulative_earnings.append(total_earnings)
            salary *= (1 + salary_growth / 100)

        # Break-even year
        break_even_year = None
        for year, earnings in enumerate(cumulative_earnings, 1):
            if earnings >= total_investment:
                break_even_year = year
                break

        # Display metrics
        st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>ROI Metrics</h3>", unsafe_allow_html=True)

        roi_col1, roi_col2, roi_col3, roi_col4 = st.columns(4)

        with roi_col1:
            st.metric("Total Investment", f"${total_investment:,.0f}")

        with roi_col2:
            lifetime_earnings = cumulative_earnings[-1]
            st.metric("Lifetime Earnings", f"${lifetime_earnings:,.0f}", help=f"{career_years} years")

        with roi_col3:
            if break_even_year:
                st.metric("Break-Even Year", f"{break_even_year} years")
            else:
                st.metric("Break-Even Year", "N/A")

        with roi_col4:
            net_gain = lifetime_earnings - total_investment
            roi_percentage = (net_gain / total_investment * 100) if total_investment > 0 else 0
            st.metric("Total ROI", f"{roi_percentage:,.0f}%")

        # Visualization
        st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>Earnings vs Investment Over Time</h3>", unsafe_allow_html=True)

        years_range = list(range(1, career_years + 1))

        fig_roi = go.Figure()

        fig_roi.add_trace(go.Scatter(
            x=years_range,
            y=cumulative_earnings,
            name='Cumulative Earnings',
            fill='tozeroy',
            line=dict(color=GOLD, width=3)
        ))

        fig_roi.add_hline(
            y=total_investment,
            line_dash="dash",
            line_color="red",
            annotation_text="Investment Amount",
            annotation_position="right"
        )

        if break_even_year:
            fig_roi.add_vline(
                x=break_even_year,
                line_dash="dash",
                line_color="green",
                annotation_text=f"Break-Even: Year {break_even_year}",
                annotation_position="top"
            )

        fig_roi.update_layout(
            xaxis_title='Years After Graduation',
            yaxis_title='Amount (USD)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=WHITE),
            hovermode='x unified'
        )

        st.plotly_chart(fig_roi, use_container_width=True)

        # Insights
        st.markdown(f"""
        <div class="university-card">
            <h3 style='color: {GOLD};'>ROI Insights</h3>
            <ul style='color: {WHITE}; font-size: 1.05rem; line-height: 1.8;'>
                <li>Your total investment of <strong>${total_investment:,.0f}</strong> will generate <strong>${lifetime_earnings:,.0f}</strong> over {career_years} years</li>
                <li>You'll break even in approximately <strong>{break_even_year if break_even_year else 'N/A'}</strong> years after graduation</li>
                <li>Your net gain will be <strong>${net_gain:,.0f}</strong>, representing a <strong>{roi_percentage:.1f}%</strong> return on investment</li>
                <li>With {salary_growth}% annual growth, your salary will reach <strong>${expected_salary * ((1 + salary_growth/100) ** 10):,.0f}</strong> in 10 years</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
display_footer()
