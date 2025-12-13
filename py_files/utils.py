"""
Shared utilities and styling for the University Insights App
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import PIL.Image
import google.generativeai as genai
from gemini_api import the_api_key

# Brand colors - Optimized for accessibility and design balance
BLUE_DARK = "#073763"      # Primary background
BLUE_MEDIUM = "#0A4F8E"    # Sidebar, cards
BLUE_LIGHT = "#1A5FA8"     # Hover states, accents
GOLD = "#f0c244"           # Primary accent, CTAs
GOLD_LIGHT = "#FFE082"     # Subtle highlights
WHITE = "#FFFFFF"          # Text on dark backgrounds
GRAY_LIGHT = "#FFFFFF"     # Changed to white for better visibility
GRAY_MEDIUM = "#FFFFFF"    # Changed to white for better visibility

def set_page_config(page_title="University Insights App"):
    """Configure the Streamlit page settings"""
    st.set_page_config(
        page_title=page_title,
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    """Apply custom CSS styling with professional design and accessibility"""
    st.markdown(f"""
    <style>
    /* Import Google Fonts for better typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global styling */
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}

    /* Main app background */
    .stApp {{
        background: linear-gradient(135deg, {BLUE_DARK} 0%, {BLUE_MEDIUM} 100%);
        color: {WHITE};
    }}

    /* ==================== SIDEBAR STYLING ==================== */

    /* Sidebar background with gradient */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {BLUE_MEDIUM} 0%, {BLUE_DARK} 100%);
        border-right: 3px solid {GOLD};
        box-shadow: 4px 0 12px rgba(0, 0, 0, 0.3);
    }}

    /* Sidebar content */
    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 2rem;
    }}

    /* Sidebar text - all elements white */
    [data-testid="stSidebar"] {{
        color: {WHITE} !important;
    }}

    [data-testid="stSidebar"] * {{
        color: {WHITE} !important;
    }}

    [data-testid="stSidebar"] .stMarkdown {{
        color: {WHITE} !important;
    }}

    [data-testid="stSidebar"] p {{
        color: {WHITE} !important;
    }}

    [data-testid="stSidebar"] span {{
        color: {WHITE} !important;
    }}

    [data-testid="stSidebar"] label {{
        color: {WHITE} !important;
    }}

    /* Sidebar headers - keep gold */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: {GOLD} !important;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}

    /* Sidebar navigation links - white text */
    [data-testid="stSidebar"] .stRadio > label {{
        background-color: rgba(255, 255, 255, 0.05);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.25rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        color: {WHITE} !important;
    }}

    [data-testid="stSidebar"] .stRadio > label:hover {{
        background-color: rgba(240, 194, 68, 0.15);
        transform: translateX(5px);
    }}

    /* Page navigation links styling */
    [data-testid="stSidebar"] ul {{
        list-style: none;
        padding: 0;
    }}

    [data-testid="stSidebar"] li {{
        margin: 0;
    }}

    [data-testid="stSidebar"] li a {{
        color: {WHITE} !important;
        text-decoration: none;
        padding: 0.75rem 1rem;
        display: block;
        border-radius: 8px;
        transition: all 0.3s ease;
        border-left: 3px solid transparent;
        font-weight: 500;
    }}

    [data-testid="stSidebar"] li a:hover {{
        background-color: rgba(240, 194, 68, 0.15);
        border-left-color: {GOLD};
        padding-left: 1.25rem;
    }}

    /* Active/selected page link */
    [data-testid="stSidebar"] li a[aria-current="page"] {{
        background-color: rgba(240, 194, 68, 0.2);
        border-left-color: {GOLD};
        color: {GOLD} !important;
        font-weight: 600;
    }}

    /* All sidebar links */
    [data-testid="stSidebar"] a {{
        color: {WHITE} !important;
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] a {{
        color: {WHITE} !important;
        text-decoration: none;
        padding: 0.75rem 1rem;
        display: block;
        border-radius: 8px;
        transition: all 0.3s ease;
        border-left: 3px solid transparent;
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] a:hover {{
        background-color: rgba(240, 194, 68, 0.1);
        border-left-color: {GOLD};
        padding-left: 1.5rem;
    }}

    /* Sidebar divider */
    [data-testid="stSidebar"] hr {{
        border-color: rgba(240, 194, 68, 0.3);
        margin: 1.5rem 0;
    }}

    /* ==================== BUTTON STYLING ==================== */

    /* Primary buttons */
    .stButton>button {{
        background: linear-gradient(135deg, {GOLD} 0%, #FFB300 100%);
        color: {BLUE_DARK};
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.65rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(240, 194, 68, 0.3);
        letter-spacing: 0.5px;
        text-transform: uppercase;
        font-size: 0.9rem;
    }}

    .stButton>button:hover {{
        background: linear-gradient(135deg, {WHITE} 0%, {GOLD_LIGHT} 100%);
        color: {BLUE_DARK};
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(240, 194, 68, 0.4);
    }}

    .stButton>button:active {{
        transform: translateY(0);
    }}

    /* Download button */
    .stDownloadButton>button {{
        background-color: {BLUE_LIGHT};
        color: {WHITE};
        border: 2px solid {GOLD};
    }}

    .stDownloadButton>button:hover {{
        background-color: {GOLD};
        color: {BLUE_DARK};
    }}

    /* ==================== FORM INPUTS ==================== */

    /* Text inputs */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {{
        background-color: {WHITE};
        color: {BLUE_DARK};
        border: 2px solid {GRAY_MEDIUM};
        border-radius: 6px;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }}

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stNumberInput>div>div>input:focus {{
        border-color: {GOLD};
        box-shadow: 0 0 0 2px rgba(240, 194, 68, 0.2);
        outline: none;
    }}

    /* Selectbox and multiselect */
    .stSelectbox>div>div>div,
    .stMultiSelect>div>div>div {{
        background-color: {WHITE};
        color: {BLUE_DARK};
        border-radius: 6px;
    }}

    /* Slider */
    .stSlider>div>div>div>div {{
        background-color: {GOLD};
    }}

    /* Date input */
    .stDateInput>div>div>input {{
        background-color: {WHITE};
        color: {BLUE_DARK};
        border: 2px solid {GRAY_MEDIUM};
        border-radius: 6px;
    }}

    /* ==================== CONTENT ELEMENTS ==================== */

    /* Headers with better hierarchy */
    h1 {{
        color: {GOLD};
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }}

    h2 {{
        color: {GOLD};
        font-weight: 600;
        font-size: 2rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid rgba(240, 194, 68, 0.3);
        padding-bottom: 0.5rem;
    }}

    h3 {{
        color: {GOLD_LIGHT};
        font-weight: 500;
        font-size: 1.5rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }}

    /* Paragraph text - better readability */
    p {{
        color: {WHITE};
        line-height: 1.7;
        font-weight: 400;
    }}

    /* Links */
    a {{
        color: {GOLD};
        text-decoration: none;
        transition: all 0.3s ease;
        border-bottom: 1px dotted {GOLD};
    }}

    a:hover {{
        color: {GOLD_LIGHT};
        border-bottom-style: solid;
    }}

    /* ==================== CARDS & CONTAINERS ==================== */

    /* University cards with elevated design */
    .university-card {{
        background: linear-gradient(135deg, rgba(26, 95, 168, 0.2) 0%, rgba(7, 55, 99, 0.4) 100%);
        border: 2px solid rgba(240, 194, 68, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }}

    .university-card:hover {{
        border-color: {GOLD};
        box-shadow: 0 8px 24px rgba(240, 194, 68, 0.2);
        transform: translateY(-2px);
    }}

    /* Metric cards */
    [data-testid="stMetricValue"] {{
        color: {GOLD};
        font-size: 2.5rem;
        font-weight: 700;
    }}

    [data-testid="stMetricLabel"] {{
        color: {WHITE};
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem;
    }}

    [data-testid="stMetricDelta"] {{
        color: {GOLD_LIGHT};
    }}

    /* ==================== ALERTS & MESSAGES ==================== */

    /* Info boxes with balanced colors */
    .stAlert {{
        background-color: rgba(26, 95, 168, 0.3);
        border-left: 4px solid {GOLD};
        color: {WHITE};
        border-radius: 6px;
        padding: 1rem;
    }}

    .stSuccess {{
        background-color: rgba(46, 125, 50, 0.2);
        border-left-color: #4CAF50;
    }}

    .stWarning {{
        background-color: rgba(237, 108, 2, 0.2);
        border-left-color: #FF9800;
    }}

    .stError {{
        background-color: rgba(211, 47, 47, 0.2);
        border-left-color: #F44336;
    }}

    /* ==================== DATAFRAMES & TABLES ==================== */

    /* Dataframe styling */
    .stDataFrame {{
        background-color: {WHITE};
        border-radius: 8px;
        overflow: hidden;
    }}

    .stDataFrame [data-testid="stDataFrameResizable"] {{
        border: 2px solid {GRAY_MEDIUM};
    }}

    /* ==================== TABS ==================== */

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.05);
        padding: 0.5rem;
        border-radius: 8px;
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        color: {WHITE};
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgba(240, 194, 68, 0.1);
        color: {GOLD};
    }}

    .stTabs [aria-selected="true"] {{
        background-color: rgba(240, 194, 68, 0.2);
        border: 2px solid {GOLD};
        color: {GOLD};
        font-weight: 600;
    }}

    /* ==================== PROGRESS & LOADING ==================== */

    /* Progress bar */
    .stProgress > div > div {{
        background-color: {GOLD};
        border-radius: 10px;
    }}

    /* Spinner */
    .stSpinner > div {{
        border-top-color: {GOLD};
    }}

    /* ==================== EXPANDER ==================== */

    /* Expander styling */
    .streamlit-expanderHeader {{
        background-color: rgba(26, 95, 168, 0.3);
        color: {GOLD};
        font-weight: 600;
        border-radius: 6px;
        padding: 1rem;
        border: 1px solid rgba(240, 194, 68, 0.3);
    }}

    .streamlit-expanderHeader:hover {{
        background-color: rgba(240, 194, 68, 0.1);
        border-color: {GOLD};
    }}

    /* ==================== FOOTER ==================== */

    /* Footer styling */
    .footer {{
        text-align: center;
        color: {GOLD};
        padding: 2rem 0;
        margin-top: 4rem;
        border-top: 2px solid rgba(240, 194, 68, 0.3);
        font-weight: 500;
    }}

    /* ==================== SCROLLBAR ==================== */

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}

    ::-webkit-scrollbar-track {{
        background: {BLUE_DARK};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {GOLD};
        border-radius: 5px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {GOLD_LIGHT};
    }}

    /* ==================== ACCESSIBILITY ==================== */

    /* Focus indicators for keyboard navigation */
    *:focus {{
        outline: 2px solid {GOLD};
        outline-offset: 2px;
    }}

    /* High contrast for better readability */
    strong, b {{
        color: {GOLD_LIGHT};
        font-weight: 600;
    }}

    /* List styling */
    ul, ol {{
        color: {WHITE};
        line-height: 1.8;
    }}

    li {{
        margin-bottom: 0.5rem;
    }}

    /* Code blocks */
    code {{
        background-color: rgba(255, 255, 255, 0.1);
        color: {GOLD_LIGHT};
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
    }}

    /* ==================== ALIGNMENT & SPACING ==================== */

    /* Main content container alignment */
    .main .block-container {{
        padding: 2rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }}

    /* Column alignment */
    [data-testid="column"] {{
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: stretch;
    }}

    /* Streamlit columns equal height */
    .row-widget.stHorizontalBlock {{
        align-items: stretch;
    }}

    /* Center alignment for specific elements */
    .center-content {{
        text-align: center;
        margin: 0 auto;
    }}

    /* Tab alignment */
    .stTabs {{
        width: 100%;
    }}

    /* Ensure full width for containers */
    .element-container {{
        width: 100%;
    }}

    /* ==================== RESPONSIVE DESIGN ==================== */

    /* Tablet and Mobile */
    @media (max-width: 1024px) {{
        .main .block-container {{
            padding: 1.5rem 1rem;
        }}

        /* Sidebar on tablets */
        [data-testid="stSidebar"] {{
            min-width: 250px;
        }}
    }}

    /* Mobile Devices */
    @media (max-width: 768px) {{
        /* Typography adjustments */
        h1 {{
            font-size: 1.75rem !important;
            line-height: 1.3;
        }}

        h2 {{
            font-size: 1.4rem !important;
            line-height: 1.4;
        }}

        h3 {{
            font-size: 1.1rem !important;
        }}

        p {{
            font-size: 0.95rem;
            line-height: 1.6;
        }}

        /* Main container */
        .main .block-container {{
            padding: 1rem 0.75rem;
        }}

        /* Cards responsive */
        .university-card {{
            padding: 1rem !important;
            margin: 0.75rem 0;
        }}

        /* Buttons full width on mobile */
        .stButton>button {{
            width: 100% !important;
            margin: 0.5rem 0 !important;
            padding: 0.75rem 1rem !important;
            font-size: 0.85rem !important;
        }}

        /* Form inputs */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stNumberInput>div>div>input {{
            font-size: 16px !important; /* Prevents zoom on iOS */
            padding: 0.75rem !important;
        }}

        .stSelectbox>div>div>div {{
            font-size: 16px !important;
        }}

        /* Tabs stack better on mobile */
        .stTabs [data-baseweb="tab-list"] {{
            flex-wrap: wrap;
            gap: 4px;
        }}

        .stTabs [data-baseweb="tab"] {{
            padding: 0.5rem 1rem !important;
            font-size: 0.85rem;
            flex: 1 1 auto;
            min-width: 120px;
        }}

        /* Metrics responsive */
        [data-testid="stMetricValue"] {{
            font-size: 1.75rem !important;
        }}

        [data-testid="stMetricLabel"] {{
            font-size: 0.75rem !important;
        }}

        /* Sidebar adjustments */
        [data-testid="stSidebar"] {{
            min-width: 100%;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 1rem;
        }}

        /* Columns stack on mobile */
        [data-testid="column"] {{
            width: 100% !important;
            flex: 1 1 100% !important;
        }}

        /* Dataframes scroll horizontally */
        .stDataFrame {{
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }}

        /* Charts responsive */
        .js-plotly-plot {{
            width: 100% !important;
            height: auto !important;
            min-height: 300px;
        }}

        /* Expander mobile friendly */
        .streamlit-expanderHeader {{
            padding: 0.75rem !important;
            font-size: 0.95rem;
        }}

        /* Footer */
        .footer {{
            padding: 1.5rem 0.5rem;
            font-size: 0.85rem;
        }}

        /* Logo sizing */
        img {{
            max-width: 100%;
            height: auto;
        }}

        /* Progress bar */
        .stProgress {{
            width: 100%;
        }}

        /* Alert boxes */
        .stAlert {{
            padding: 0.75rem;
            font-size: 0.9rem;
        }}
    }}

    /* Small Mobile (< 480px) */
    @media (max-width: 480px) {{
        h1 {{
            font-size: 1.5rem !important;
        }}

        h2 {{
            font-size: 1.2rem !important;
        }}

        h3 {{
            font-size: 1rem !important;
        }}

        .main .block-container {{
            padding: 0.75rem 0.5rem;
        }}

        .university-card {{
            padding: 0.75rem !important;
        }}

        .stButton>button {{
            padding: 0.65rem 0.85rem !important;
            font-size: 0.8rem !important;
        }}

        .stTabs [data-baseweb="tab"] {{
            padding: 0.4rem 0.75rem !important;
            font-size: 0.8rem;
            min-width: 100px;
        }}

        [data-testid="stMetricValue"] {{
            font-size: 1.5rem !important;
        }}
    }}

    /* Landscape orientation on mobile */
    @media (max-width: 768px) and (orientation: landscape) {{
        .main .block-container {{
            padding: 0.75rem;
        }}

        h1 {{
            font-size: 1.5rem !important;
        }}

        .university-card {{
            padding: 0.75rem !important;
        }}
    }}

    /* High DPI displays */
    @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {{
        /* Sharper text rendering */
        * {{
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
    }}

    /* Print styles */
    @media print {{
        [data-testid="stSidebar"] {{
            display: none;
        }}

        .stButton {{
            display: none;
        }}

        .main .block-container {{
            max-width: 100%;
        }}

        .university-card {{
            page-break-inside: avoid;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def display_logo():
    """Display the app logo"""
    try:
        logo_path = Path(__file__).parents[1] / 'images/UR&IA.png'
        logo_image = PIL.Image.open(logo_path)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo_image, use_container_width=True)
    except Exception as e:
        st.error(f"Logo not found: {e}")

def display_footer():
    """Display the app footer"""
    st.markdown(f"""
    <div class="footer">
        Made with ❤️ by theoriginialmapd © Copyright 2024 @ Duke in DESIGNTK530
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def load_university_data():
    """Load and cache the university dataset"""
    try:
        csv_path = Path(__file__).parents[1] / 'datasets/clean/qs2023_worlduni_rank_cleandata.csv'
        data = pd.read_csv(csv_path)
        return data
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

@st.cache_resource
def get_gemini_model():
    """Initialize and cache the Gemini model"""
    try:
        genai.configure(api_key=the_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model
    except Exception as e:
        st.error(f"Error initializing Gemini: {e}")
        return None

def recode_columns(data):
    """
    Encode score columns into categorical bins for clustering.

    Args:
        data: DataFrame with university data

    Returns:
        DataFrame with encoded columns added
    """
    ranges = [0, 20, 40, 60, 80, 100]
    labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
    map_dict = {
        'Very Low': 0,
        'Low': 1,
        'Medium': 2,
        'High': 3,
        'Very High': 4
    }

    # Create encoded columns
    data['Academic Reputation Score Encoded'] = pd.cut(
        data['Academic Reputation Score'],
        bins=ranges,
        include_lowest=True,
        labels=labels
    )
    data['International Students Ratio Score Encoded'] = pd.cut(
        data['International Students Ratio Score'],
        bins=ranges,
        include_lowest=True,
        labels=labels
    )
    data['Graduate Employment Rate Score Encoded'] = pd.cut(
        data['Graduate Employment Rate Score'],
        bins=ranges,
        include_lowest=True,
        labels=labels
    )

    # Map to numeric codes
    data['Academic Reputation Score Encoded'] = data['Academic Reputation Score Encoded'].map(map_dict)
    data['International Students Ratio Score Encoded'] = data['International Students Ratio Score Encoded'].map(map_dict)
    data['Graduate Employment Rate Score Encoded'] = data['Graduate Employment Rate Score Encoded'].map(map_dict)

    return data

def initialize_session_state():
    """Initialize session state variables"""
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {}

    if 'recommended_universities' not in st.session_state:
        st.session_state.recommended_universities = None

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    if 'bookmarked_universities' not in st.session_state:
        st.session_state.bookmarked_universities = []

    if 'comparison_list' not in st.session_state:
        st.session_state.comparison_list = []

    if 'application_deadlines' not in st.session_state:
        st.session_state.application_deadlines = {}

def create_metric_card(title, value, delta=None):
    """Create a styled metric card"""
    if delta:
        st.metric(label=title, value=value, delta=delta)
    else:
        st.metric(label=title, value=value)

def show_info_box(message, type="info"):
    """Display an info/warning/success box"""
    if type == "info":
        st.info(message)
    elif type == "warning":
        st.warning(message)
    elif type == "success":
        st.success(message)
    elif type == "error":
        st.error(message)

def format_country_list(data):
    """Get unique sorted list of countries"""
    return sorted(data['Country'].dropna().unique().tolist())

def get_score_category(score):
    """Convert numeric score to category label"""
    if score >= 80:
        return "Very High"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    elif score >= 20:
        return "Low"
    else:
        return "Very Low"
