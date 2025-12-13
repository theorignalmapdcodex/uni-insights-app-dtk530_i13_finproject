# University Recommendation and Insights App

**Enhancing the University Application Journey of Undergraduate and Graduate Students All Around the World**

A comprehensive Streamlit web application that helps international students navigate the complex university application process with data-driven insights, AI-powered guidance, and personalized recommendations.

---

## 🎯 Mission

This application leverages the **2023 QS World University Ranking Dataset** to analyze key factors influencing international student decisions when applying to universities. Our goal is to provide actionable insights for students navigating the university application process, helping them understand institutional dynamics, and make informed decisions regarding scholarships and school selection.

---

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Research Foundation](#research-foundation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### 🏠 Home Page
- Welcome dashboard with mission statement
- Feature overview and navigation guide
- Research-based approach explanation

### 🎯 Discovery & Matching
- **Natural Language Input**: Describe preferences in plain English
- **Advanced Filters**: Precise control over academic reputation, diversity, and employment scores
- **ML-Powered Recommendations**: K-Means clustering with 25 clusters for personalized matches
- **3D Visualization**: Interactive Plotly chart showing university landscape
- **AI Insights**: Get instant insights about recommended universities
- **Comparison Tools**: Side-by-side comparison of top matches
- **Bookmark Feature**: Save universities for later review

### 📋 Application Journey Planner
- **University Tracking**: Add and manage target universities
- **Personalized Timeline**: AI-generated month-by-month application roadmap
- **Document Checklist**: Comprehensive checklist covering:
  - Transcripts and academic records
  - Test scores (SAT, GRE, TOEFL, etc.)
  - Essays and writing samples
  - Letters of recommendation
  - Financial documents
  - Application forms
- **Deadline Tracker**: Set and monitor application deadlines
- **Progress Monitoring**: Visual progress bars for completion tracking
- **Application Tips**: Institution-specific advice from AI

### 💰 Scholarship & Funding Hub
- **Scholarship Finder**: Search for scholarships by university, degree level, and type
- **External Resources**: Discover Fulbright, Chevening, and other major programs
- **Cost Calculator**: Estimate total cost of attendance including:
  - Tuition and fees
  - Housing and living expenses
  - Books and supplies
  - Personal expenses
- **Funding Sources**: Track scholarships, work-study, family contributions, and loans
- **Financial Projections**: Multi-year cost and funding visualization
- **ROI Analysis**: Calculate return on investment with:
  - Break-even year estimation
  - Lifetime earnings projection
  - Net gain calculation
  - Interactive charts and insights

### 📊 Success Insights Dashboard
- **Global Trends**: Analyze university distribution by country
- **Score Distributions**: Understand where you stand globally
- **Regional Comparisons**: Compare countries on key metrics
- **Competitiveness Tiers**: Universities categorized from "Highly Competitive" to "Less Competitive"
- **Acceptance Rate Insights**: AI-powered analysis of admission chances
- **Program-Specific Data**: Deep dive into individual programs
- **Field Comparisons**: Compare programs across multiple universities
- **Success Predictor**: AI analysis of your admission chances based on:
  - GPA and test scores
  - Extracurricular activities
  - Work experience
  - Unique achievements
- **Alternative Recommendations**: Reach, target, and safety school suggestions

### 🤖 AI Assistant
- **Conversational Interface**: Chat with AI about any application question
- **Context-Aware Responses**: Personalized based on your situation
- **Suggested Questions**: Quick access to common queries
- **Chat History**: Review and export previous conversations
- **Quick Guides**: Comprehensive guides on:
  - Writing application essays
  - Document checklists
  - Interview preparation
  - International student resources
- **24/7 Availability**: Get answers anytime you need them

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Google Gemini API key (for AI features)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd uni-insights-app-dtk530_i13_finproject
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the `py_files` directory:
```bash
DTK530_I13_GEMINI_AI_API_KEY=your_gemini_api_key_here
```

To get a Gemini API key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste into your `.env` file

---

## 💻 Usage

### Running Locally
Navigate to the `py_files` directory and run:
```bash
cd py_files
streamlit run Home.py
```

The app will open in your default web browser at `http://localhost:8501`

### Navigation
- Use the **sidebar** to navigate between different pages
- Start with the **Home** page for an overview
- Visit **Discovery & Matching** to find universities
- Plan your journey in **Application Journey**
- Explore funding in **Scholarship Hub**
- Analyze success rates in **Success Insights**
- Ask questions anytime in **AI Assistant**

---

## 📁 Project Structure

```
uni-insights-app-dtk530_i13_finproject/
├── py_files/
│   ├── Home.py                          # Main entry point
│   ├── utils.py                         # Shared utilities and styling
│   ├── gemini_api.py                    # API key configuration
│   ├── gemini_ai_call.py                # Gemini API wrapper
│   ├── pages/
│   │   ├── 1_🎯_Discovery_&_Matching.py
│   │   ├── 2_📋_Application_Journey.py
│   │   ├── 3_💰_Scholarship_Hub.py
│   │   ├── 4_📊_Success_Insights.py
│   │   └── 5_🤖_AI_Assistant.py
│   └── .env                             # Environment variables (not in git)
├── datasets/
│   ├── clean/
│   │   └── qs2023_worlduni_rank_cleandata.csv
│   └── raw/
│       └── 2023_qs_world-uni_rank.csv
├── images/
│   ├── UR&IA.png                        # App logo
│   └── ...                              # Other branding assets
├── dtk530_i13_bb+llms_fp.ipynb         # Research notebook
├── requirements.txt                     # Python dependencies
├── README.md                            # This file
└── .gitignore
```

---

## 🛠️ Technologies Used

### Core Framework
- **Streamlit 1.40.2** - Web application framework
- **Python 3.8+** - Programming language

### Machine Learning & Data Science
- **scikit-learn 1.5.2** - K-Means clustering
- **pandas 2.2.3** - Data manipulation
- **numpy 2.0.2** - Numerical computing
- **scipy 1.14.1** - Scientific computing

### Visualization
- **plotly 5.24.1** - Interactive 3D charts
- **matplotlib 3.9.2** - Statistical plotting
- **altair 5.5.0** - Declarative visualizations

### AI Integration
- **google-generativeai 0.8.3** - Gemini AI API
- **torch 2.5.1** - Deep learning framework
- **keras 3.6.0** - Neural networks

### Utilities
- **python-dotenv 1.0.1** - Environment variable management
- **Pillow 11.0.0** - Image processing
- **requests 2.32.3** - HTTP requests

---

## 🔬 Research Foundation

This application is built on rigorous academic research with the following objectives:

### Research Brief
Leveraging the **2023 QS World University Ranking Dataset** from Kaggle to develop a Streamlit web app focusing on the journey and experiences of undergraduate and graduate students worldwide, especially international students navigating university applications.

### Research Objectives
1. **Analyze International Student Intake**: How intake rates at various institutions influence application success and guide students in selecting schools aligned with their goals

2. **Identify Institutional Offerings**: Programs and funding options that enhance students' chances of acceptance

3. **Develop AI-Powered Insights**: Streamlit web app delivering personalized insights supported by Gemini LLM API for real-time guidance

4. **Improve Student Success**: Provide data-driven insights to improve student success rates through the application process

5. **Support Institutions**: Help universities understand trends to improve recruitment strategies and ensure positive student experiences

### Methodology
- **Data**: 2023 QS World University Rankings (1,422 universities, 13 key metrics)
- **ML Algorithm**: K-Means Clustering with 25 clusters
- **Features**: Academic Reputation, International Student Diversity, Graduate Employment Rate
- **AI Enhancement**: Google Gemini 1.5 Flash for contextual insights
- **Validation**: Research documented in Jupyter notebook (`dtk530_i13_bb+llms_fp.ipynb`)

---

## 🌐 Deployment

### Streamlit Cloud (Recommended)
This app is optimized for deployment on Streamlit Cloud:

1. Push your code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Select your repository and `py_files/Home.py` as the entry point
4. Add your `DTK530_I13_GEMINI_AI_API_KEY` in Secrets management
5. Deploy!

### Live Demo
**[University Recommendation and Insights App](https://uni-recommend-app.streamlit.app/)**

### Local Deployment
For local testing and development:
```bash
cd py_files
streamlit run Home.py
```

---

## 🎨 Design & Branding

### Color Scheme
- **Primary Blue**: #073763 (Background)
- **Accent Gold**: #f0c244 (Text, highlights, buttons)
- **White**: #FFFFFF (Content text)

### Typography
- Clean, modern sans-serif fonts
- Accessible font sizes and line heights
- High contrast for readability

### User Experience
- Multi-page navigation via sidebar
- Responsive layout for all screen sizes
- Interactive visualizations
- Progress indicators and feedback
- Consistent styling across all pages

---

## 👥 Contributing

This is an academic research project for Duke University's DESIGNTK530 course. Contributions, suggestions, and feedback are welcome!

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

© Copyright 2024 @ Duke in DESIGNTK530

Made with ❤️ by theoriginialmapd

---

## 🆘 Support

For questions, issues, or feedback:
- Open an issue on GitHub
- Contact: [Your contact information]
- Documentation: See the Jupyter notebook for detailed research methodology

---

## 🙏 Acknowledgments

- **Data Source**: QS World University Rankings 2023
- **AI Provider**: Google Gemini AI
- **Framework**: Streamlit
- **Institution**: Duke University, DESIGNTK530 Course
- **Inspiration**: International students navigating the complex university application process

---

## 📚 Citation

If you use this application or research in your work, please cite:

```
University Recommendation and Insights App
Author: theoriginialmapd
Year: 2024
Institution: Duke University
Course: DESIGNTK530
URL: https://uni-recommend-app.streamlit.app/
```

---

**Built to help students worldwide make informed decisions about their educational future.**
