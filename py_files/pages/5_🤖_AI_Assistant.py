"""
Page 5: AI Assistant & Q&A
Conversational AI assistant for personalized guidance
"""
import streamlit as st
from datetime import datetime

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
set_page_config(page_title="AI Assistant")
apply_custom_css()
initialize_session_state()

# Display logo
display_logo()

st.markdown(f"<h1 style='color: {GOLD}; text-align: center;'>🤖 AI Assistant</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color: {WHITE}; text-align: center; font-size: 1.1rem;'>Your personal guide for university application questions</p>", unsafe_allow_html=True)

# Get Gemini model
gemini_model = get_gemini_model()

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'assistant_context' not in st.session_state:
    st.session_state.assistant_context = ""

# Context setting
with st.expander("⚙️ Set Context (Optional)", expanded=False):
    st.markdown(f"<p style='color: {WHITE};'>Provide context about your situation to get more personalized responses.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        context_universities = st.text_input(
            "Universities you're considering:",
            placeholder="E.g., Stanford, MIT, Harvard",
            key="context_unis"
        )

        context_field = st.text_input(
            "Field of study:",
            placeholder="E.g., Computer Science",
            key="context_field"
        )

    with col2:
        context_level = st.selectbox(
            "Degree level:",
            ["Not specified", "Undergraduate", "Master's", "PhD"],
            key="context_level"
        )

        context_nationality = st.text_input(
            "Your nationality (optional):",
            placeholder="E.g., India, China, Brazil",
            key="context_nationality"
        )

    if st.button("💾 Save Context", key="save_context"):
        context_parts = []
        if context_universities:
            context_parts.append(f"considering {context_universities}")
        if context_field:
            context_parts.append(f"interested in {context_field}")
        if context_level != "Not specified":
            context_parts.append(f"pursuing {context_level}")
        if context_nationality:
            context_parts.append(f"from {context_nationality}")

        if context_parts:
            st.session_state.assistant_context = "Student is " + ", ".join(context_parts) + "."
            st.success("✅ Context saved! Your answers will now be more personalized.")
        else:
            st.session_state.assistant_context = ""

# Suggested questions
st.markdown(f"<h3 style='color: {GOLD};'>💡 Suggested Questions</h3>", unsafe_allow_html=True)

suggested_questions = [
    "What are the typical application deadlines for Fall 2026?",
    "How important are extracurricular activities in university admissions?",
    "What's the difference between need-based and merit-based scholarships?",
    "How can I improve my chances of getting into a top university?",
    "What should I include in my statement of purpose?",
    "How do I choose between multiple university offers?",
    "What are the visa requirements for international students in the US?",
    "How can I find research opportunities as an undergraduate?",
]

col1, col2, col3, col4 = st.columns(4)
columns = [col1, col2, col3, col4]

for idx, question in enumerate(suggested_questions):
    with columns[idx % 4]:
        if st.button(question, key=f"suggest_{idx}", use_container_width=True):
            st.session_state.current_question = question

# Chat interface
st.markdown(f"<h3 style='color: {GOLD}; margin-top: 2rem;'>💬 Chat with AI Assistant</h3>", unsafe_allow_html=True)

# Display chat history
chat_container = st.container()

with chat_container:
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div style='background-color: rgba(240, 194, 68, 0.1); border-left: 3px solid {GOLD}; padding: 1rem; margin: 1rem 0; border-radius: 5px;'>
                    <p style='color: {GOLD}; font-weight: bold; margin: 0;'>You</p>
                    <p style='color: {WHITE}; margin: 0.5rem 0 0 0;'>{message['content']}</p>
                    <p style='color: rgba(255,255,255,0.5); font-size: 0.8rem; margin: 0.5rem 0 0 0;'>{message['timestamp']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background-color: rgba(255, 255, 255, 0.05); border-left: 3px solid {WHITE}; padding: 1rem; margin: 1rem 0; border-radius: 5px;'>
                    <p style='color: {WHITE}; font-weight: bold; margin: 0;'>🤖 AI Assistant</p>
                    <div style='color: {WHITE}; margin: 0.5rem 0 0 0;'>{message['content']}</div>
                    <p style='color: rgba(255,255,255,0.5); font-size: 0.8rem; margin: 0.5rem 0 0 0;'>{message['timestamp']}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("👋 Hi! I'm your AI assistant. Ask me anything about university applications, admissions, scholarships, or student life!")

# Chat input
st.markdown("<br>", unsafe_allow_html=True)

# Check if there's a suggested question selected
if 'current_question' in st.session_state and st.session_state.current_question:
    user_question = st.session_state.current_question
    st.session_state.current_question = None  # Reset
else:
    user_question = st.text_area(
        "Your question:",
        placeholder="Type your question here... (e.g., How do I write a compelling personal statement?)",
        height=100,
        key="user_input"
    )

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    send_button = st.button("📤 Send", key="send_btn", use_container_width=True)

with col2:
    clear_button = st.button("🗑️ Clear Chat", key="clear_btn", use_container_width=True)

with col3:
    export_button = st.button("💾 Export Chat", key="export_btn", use_container_width=True)

# Handle send button
if send_button and user_question:
    # Add user message to history
    timestamp = datetime.now().strftime("%I:%M %p")
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_question,
        'timestamp': timestamp
    })

    # Generate response
    with st.spinner("🤔 Thinking..."):
        if gemini_model:
            try:
                # Build context-aware prompt
                if st.session_state.assistant_context:
                    full_prompt = f"""
                    Context: {st.session_state.assistant_context}

                    Question: {user_question}

                    Provide a helpful, detailed, and personalized response. Be encouraging but realistic.
                    If the question is about specific universities or programs, provide factual information.
                    If giving advice, be practical and actionable.
                    """
                else:
                    full_prompt = f"""
                    Question: {user_question}

                    Provide a helpful, detailed response about university applications, admissions, or student life.
                    Be encouraging but realistic. Give practical, actionable advice.
                    """

                response = gemini_model.generate_content(full_prompt)
                assistant_response = response.text

                # Add assistant response to history
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': assistant_response,
                    'timestamp': timestamp
                })

                st.rerun()

            except Exception as e:
                st.error(f"Error generating response: {e}")
        else:
            st.error("Gemini model not available. Please check your API configuration.")

# Handle clear button
if clear_button:
    st.session_state.chat_history = []
    st.success("✅ Chat history cleared!")
    st.rerun()

# Handle export button
if export_button and st.session_state.chat_history:
    # Create export text
    export_text = "University Insights App - Chat Export\n"
    export_text += "=" * 50 + "\n\n"

    for message in st.session_state.chat_history:
        role = "You" if message['role'] == 'user' else "AI Assistant"
        export_text += f"{role} ({message['timestamp']}):\n"
        export_text += f"{message['content']}\n\n"
        export_text += "-" * 50 + "\n\n"

    st.download_button(
        label="📥 Download Chat History",
        data=export_text,
        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

# Quick guides section
st.markdown("<hr style='border: 1px solid #f0c244; margin: 3rem 0;'>", unsafe_allow_html=True)

st.markdown(f"<h2 style='color: {GOLD}; text-align: center;'>📚 Quick Guides</h2>", unsafe_allow_html=True)

guide_tab1, guide_tab2, guide_tab3, guide_tab4 = st.tabs([
    "📝 Application Essays",
    "📋 Documents Checklist",
    "💡 Interview Tips",
    "🌍 International Students"
])

with guide_tab1:
    st.markdown(f"""
    <div class="university-card">
        <h3 style='color: {GOLD};'>Writing Compelling Application Essays</h3>
        <ul style='color: {WHITE}; font-size: 1.05rem; line-height: 1.8;'>
            <li><strong>Be Authentic:</strong> Write in your own voice, not what you think admissions wants to hear</li>
            <li><strong>Show, Don't Tell:</strong> Use specific examples and anecdotes to illustrate your points</li>
            <li><strong>Answer the Question:</strong> Make sure you're directly addressing the prompt</li>
            <li><strong>Start Strong:</strong> Hook the reader with a compelling opening</li>
            <li><strong>Be Specific:</strong> Avoid generic statements; focus on unique experiences</li>
            <li><strong>Reflect and Grow:</strong> Show self-awareness and what you learned from experiences</li>
            <li><strong>Proofread:</strong> Eliminate typos and grammatical errors</li>
            <li><strong>Get Feedback:</strong> Have teachers, mentors, or friends review your essay</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎯 Get Essay Topic Ideas", key="essay_ideas"):
        with st.spinner("Generating ideas..."):
            if gemini_model:
                essay_query = "Generate 10 unique and compelling personal statement essay topics for university applications. Each should prompt deep reflection and allow students to showcase their personality, values, and growth."
                try:
                    response = gemini_model.generate_content(essay_query)
                    st.info(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

with guide_tab2:
    st.markdown(f"""
    <div class="university-card">
        <h3 style='color: {GOLD};'>Essential Documents Checklist</h3>

        <h4 style='color: {GOLD}; margin-top: 1.5rem;'>Academic Records</h4>
        <ul style='color: {WHITE};'>
            <li>Official transcripts (high school and/or undergraduate)</li>
            <li>Transcript evaluation (for international credentials)</li>
            <li>Degree certificates (if applicable)</li>
            <li>Class rank or GPA statement</li>
        </ul>

        <h4 style='color: {GOLD}; margin-top: 1.5rem;'>Test Scores</h4>
        <ul style='color: {WHITE};'>
            <li>SAT/ACT (undergraduate) or GRE/GMAT (graduate)</li>
            <li>TOEFL/IELTS/Duolingo (international students)</li>
            <li>Subject tests (if required)</li>
            <li>AP/IB scores (if applicable)</li>
        </ul>

        <h4 style='color: {GOLD}; margin-top: 1.5rem;'>Essays & Statements</h4>
        <ul style='color: {WHITE};'>
            <li>Personal statement / Statement of purpose</li>
            <li>Supplemental essays</li>
            <li>Diversity statement (if applicable)</li>
            <li>Writing samples (for certain programs)</li>
        </ul>

        <h4 style='color: {GOLD}; margin-top: 1.5rem;'>Recommendations</h4>
        <ul style='color: {WHITE};'>
            <li>2-3 letters of recommendation</li>
            <li>Resume/CV</li>
            <li>List of activities and honors</li>
        </ul>

        <h4 style='color: {GOLD}; margin-top: 1.5rem;'>Financial Documents</h4>
        <ul style='color: {WHITE};'>
            <li>Bank statements (international students)</li>
            <li>FAFSA/CSS Profile (US students)</li>
            <li>Scholarship applications</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with guide_tab3:
    st.markdown(f"""
    <div class="university-card">
        <h3 style='color: {GOLD};'>Acing University Interviews</h3>

        <h4 style='color: {GOLD}; margin-top: 1.5rem;'>Before the Interview</h4>
        <ul style='color: {WHITE}; font-size: 1.05rem; line-height: 1.8;'>
            <li>Research the university and program thoroughly</li>
            <li>Review your application materials</li>
            <li>Prepare answers to common questions</li>
            <li>Prepare thoughtful questions to ask the interviewer</li>
            <li>Practice with a friend or mentor</li>
        </ul>

        <h4 style='color: {GOLD}; margin-top: 1.5rem;'>Common Interview Questions</h4>
        <ul style='color: {WHITE}; font-size: 1.05rem; line-height: 1.8;'>
            <li>Why do you want to attend this university?</li>
            <li>What are your academic interests and career goals?</li>
            <li>Tell me about a challenge you've overcome</li>
            <li>What will you contribute to our campus community?</li>
            <li>What do you do outside of academics?</li>
            <li>Where do you see yourself in 10 years?</li>
        </ul>

        <h4 style='color: {GOLD}; margin-top: 1.5rem;'>During the Interview</h4>
        <ul style='color: {WHITE}; font-size: 1.05rem; line-height: 1.8;'>
            <li>Be punctual (arrive 10-15 minutes early)</li>
            <li>Dress professionally</li>
            <li>Make eye contact and smile</li>
            <li>Be authentic and enthusiastic</li>
            <li>Use specific examples from your experiences</li>
            <li>Ask thoughtful questions</li>
            <li>Send a thank-you note afterward</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎤 Practice Interview Questions", key="practice_interview"):
        with st.spinner("Generating interview questions..."):
            if gemini_model:
                interview_query = "Generate 10 unique and challenging university interview questions that go beyond the common ones. Include questions that test critical thinking, values, and self-reflection."
                try:
                    response = gemini_model.generate_content(interview_query)
                    st.info(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

with guide_tab4:
    st.markdown(f"""
    <div class="university-card">
        <h3 style='color: {GOLD};'>Guide for International Students</h3>

        <h4 style='color: {GOLD}; margin-top: 1.5rem;'>Application Process</h4>
        <ul style='color: {WHITE}; font-size: 1.05rem; line-height: 1.8;'>
            <li><strong>Start Early:</strong> International applications take longer due to credential evaluation</li>
            <li><strong>English Proficiency:</strong> Most universities require TOEFL (80+) or IELTS (6.5+)</li>
            <li><strong>Credential Evaluation:</strong> Use services like WES or ECE to evaluate foreign transcripts</li>
            <li><strong>Financial Documentation:</strong> Prove you can afford tuition and living expenses</li>
        </ul>

        <h4 style='color: {GOLD}; margin-top: 1.5rem;'>Visa Requirements (F-1 Student Visa for USA)</h4>
        <ul style='color: {WHITE}; font-size: 1.05rem; line-height: 1.8;'>
            <li>Form I-20 from your university</li>
            <li>SEVIS fee payment</li>
            <li>Valid passport</li>
            <li>Visa application (DS-160)</li>
            <li>Visa interview at US embassy/consulate</li>
            <li>Financial proof (bank statements, sponsorship letters)</li>
        </ul>

        <h4 style='color: {GOLD}; margin-top: 1.5rem;'>Financial Considerations</h4>
        <ul style='color: {WHITE}; font-size: 1.05rem; line-height: 1.8;'>
            <li><strong>Tuition:</strong> $20,000 - $60,000+ per year depending on university</li>
            <li><strong>Living Expenses:</strong> $10,000 - $20,000 per year</li>
            <li><strong>Health Insurance:</strong> Often mandatory ($1,000 - $3,000 per year)</li>
            <li><strong>Work Opportunities:</strong> On-campus work (up to 20 hrs/week), CPT, OPT</li>
            <li><strong>Scholarships:</strong> Limited for international students but available at some universities</li>
        </ul>

        <h4 style='color: {GOLD}; margin-top: 1.5rem;'>Cultural Adjustment Tips</h4>
        <ul style='color: {WHITE}; font-size: 1.05rem; line-height: 1.8;'>
            <li>Join international student organizations</li>
            <li>Attend orientation programs</li>
            <li>Build relationships with domestic and international students</li>
            <li>Utilize university support services (counseling, writing centers, etc.)</li>
            <li>Stay connected with home while embracing new experiences</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
display_footer()
