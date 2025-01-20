import streamlit as st
import pandas as pd
import time
import plotly.express as px
import altair as alt  # Adding Altair as a backup visualization option

# Importing the necessary functions needed to run the app
from gemini_ai_call import *
from gemini_api import *

# Gemini API integration #1 - Calling the Gemini API
def __get_gemini_client__() -> genai.GenerativeModel:
    genai.configure(api_key=the_api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    return gemini_model

gemini_model = __get_gemini_client__()

# Configure page settings for better presentation
st.set_page_config(
    page_title="AI-Driven Idea Generator",
    layout="wide"
)

# Enhanced prompt conversion with iteration-specific guidance
def convert_to_prompt(hmw_question, iteration, previous_ideas=[]):
    base_prompt = f"Generate innovative ideas to address: {hmw_question}."
    
    if iteration == 1:
        return f"{base_prompt} Focus on broad, transformative concepts. Provide 10 distinct ideas."
    elif iteration == 2:
        return f"{base_prompt} Building on existing ideas but exploring new directions. Generate 8 additional unique ideas different from: {', '.join(previous_ideas)}."
    else:
        return f"{base_prompt} Push for breakthrough concepts in unexplored areas. Generate 7 final innovative ideas distinct from: {', '.join(previous_ideas)}."

# Enhanced idea generation with progressive iterations
def generate_ideas(gemini_model, hmw_question):
    all_ideas = []
    iterations = [(1, 10), (2, 8), (3, 7)]
    
    for iteration_num, target_ideas in iterations:
        with st.spinner(f"Generating iteration {iteration_num} of 3..."):
            try:
                prompt = convert_to_prompt(hmw_question, iteration_num, all_ideas)
                response = gemini_model.generate_content(prompt)
                
                # Process and clean the response
                new_ideas = [idea.strip() for idea in response.text.strip().split("\n")
                           if idea.strip() and not idea.strip().isdigit()]
                
                # Ensure we get exactly the target number of ideas
                new_ideas = new_ideas[:target_ideas]
                all_ideas.extend(new_ideas)
                
                # Add progress indicator
                progress = len(all_ideas) / 25
                st.progress(progress)
                
            except Exception as e:
                st.error(f"Error in iteration {iteration_num}: {str(e)}")
                time.sleep(2)
                continue
    
    return all_ideas

# Enhanced thematic analysis with more sophisticated grouping
def analyze_themes(ideas):
    # Expanded theme keywords for better categorization
    theme_keywords = {
        "Innovation & Technology": [
            "digital", "tech", "smart", "AI", "automation", "data", "platform",
            "app", "software", "system", "innovation", "blockchain"
        ],
        "Sustainability & Environment": [
            "green", "eco", "sustainable", "environmental", "renewable", "clean",
            "conservation", "energy", "waste", "recycling", "climate"
        ],
        "Social Impact & Community": [
            "community", "social", "public", "people", "citizen", "engagement",
            "participation", "collaboration", "education", "awareness"
        ],
        "Infrastructure & Systems": [
            "infrastructure", "system", "network", "framework", "structure",
            "platform", "architecture", "design", "integration"
        ],
        "Economic & Business": [
            "business", "economic", "market", "financial", "commercial",
            "enterprise", "profit", "revenue", "cost", "investment"
        ]
    }
    
    # Initialize theme groups
    themed_ideas = {theme: [] for theme in theme_keywords}
    themed_ideas["Cross-cutting & Others"] = []
    
    for idea in ideas:
        idea_lower = idea.lower()
        matched_themes = []
        
        # Check which themes the idea matches
        for theme, keywords in theme_keywords.items():
            if any(keyword in idea_lower for keyword in keywords):
                matched_themes.append(theme)
        
        # Assign idea to appropriate theme(s)
        if len(matched_themes) == 1:
            themed_ideas[matched_themes[0]].append(idea)
        elif len(matched_themes) > 1:
            # If idea matches multiple themes, put in cross-cutting
            themed_ideas["Cross-cutting & Others"].append(idea)
        else:
            themed_ideas["Cross-cutting & Others"].append(idea)
    
    # Remove empty themes
    return {k: v for k, v in themed_ideas.items() if v}


# Main application interface
st.title("AI-Driven Idea Generator")
st.markdown("""
Generate innovative concepts through iterative AI-powered ideation.
Each iteration builds upon previous ideas while exploring new directions.
""")

# User input
hmw_question = st.text_input(
    "Enter your How-Might-We question:",
    placeholder="E.g., How might we make urban transportation more sustainable?"
)

if st.button("Generate Ideas", type="primary"):
    if hmw_question:
        # Generate ideas through iterations
        ideas = generate_ideas(gemini_model, hmw_question)
        
        # Display iterations
        st.subheader("Generated Ideas by Iteration")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Iteration 1 (Foundation)")
            for idea in ideas[:10]:
                st.markdown(f"• {idea}")
                
        with col2:
            st.markdown("### Iteration 2 (Evolution)")
            for idea in ideas[10:18]:
                st.markdown(f"• {idea}")
                
        with col3:
            st.markdown("### Iteration 3 (Breakthrough)")
            for idea in ideas[18:25]:
                st.markdown(f"• {idea}")
        
        # Perform thematic analysis
        themed_ideas = analyze_themes(ideas)
        
        # Create themed table without asterisks
        st.subheader("Thematic Analysis")
        theme_data = []
        for theme, theme_ideas in themed_ideas.items():
            theme_data.append({
                "Theme": theme,  # Removed asterisks
                "Ideas": "<br>".join([f"• {idea}" for idea in theme_ideas]),
                "Count": len(theme_ideas)
            })
        
        # Display as formatted table
        df = pd.DataFrame(theme_data)
        st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        

        # Add theme distribution visualization with custom colors
        st.subheader("Theme Distribution")
        
        # Define a custom color scheme
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD']
        
        try:
            # First attempt: Try using Plotly Express
            fig = px.bar(
                df,
                x='Theme',
                y='Count',
                color='Theme',
                color_discrete_sequence=colors,
                title='Distribution of Ideas Across Themes'
            )
            
            # Customize the layout
            fig.update_layout(
                showlegend=False,
                xaxis_title="",
                yaxis_title="Number of Ideas",
                plot_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            # Update bar appearance
            fig.update_traces(
                marker_line_color='rgb(8,48,107)',
                marker_line_width=1.5,
                opacity=0.8
            )
            
            # Display the Plotly chart
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            # Fallback: Use Altair if Plotly fails
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Theme', sort='-y'),
                y='Count',
                color=alt.Color('Theme', scale=alt.Scale(range=colors))
            ).properties(
                height=400
            )
            
            # Display the Altair chart
            st.altair_chart(chart, use_container_width=True)

# Footer
st.markdown("""
---
<div style="text-align: center; color: #555555;">
Enhanced AI-Driven Idea Generator | Made with ❤️ by Michael Agyeman-Prempeh
</div>
""", unsafe_allow_html=True)