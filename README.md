This README provides guidance on using the Jupyter notebook `dtk530_i13_bb+llms.ipynb`

## University Recommendation and Insights App

This Streamlit app helps international students find the best universities based on their preferences and gain insights into key metrics like academic reputation, international student ratio, and employment rate. It leverages Natural Language Processing (NLP) and machine learning for a comprehensive analysis.

### Table of Contents

  * [Installation](https://www.google.com/url?sa=E&source=gmail&q=#installation)
  * [Usage](https://www.google.com/url?sa=E&source=gmail&q=#usage)
  * [Features](https://www.google.com/url?sa=E&source=gmail&q=#features)
  * [Technologies Used](https://www.google.com/url?sa=E&source=gmail&q=#technologies-used)
  * [Deployment](https://www.google.com/url?sa=E&source=gmail&q=#deployment)

### Installation

This project requires the following Python libraries:

  * streamlit
  * pandas
  * numpy
  * scikit-learn
  * matplotlib
  * plotly.express
  * google.generativeai (optional)
  * PIL
  * re

You can install them using pip:

```bash
pip install streamlit pandas numpy scikit-learn matplotlib plotly.express google.generativeai PIL re
```

**Note:** Installing `google.generativeai` requires a Google Cloud Platform project with the Generative AI API enabled.

### Usage

1.  Clone this repository.
2.  Install the required libraries (see Installation).
3.  Run the app using:

```bash
streamlit run app.py
```

This will launch the Streamlit app in your web browser.

### Features

  * User-friendly interface to input preferences.
  * NLP for feature extraction from user text.
  * K-Means clustering for university recommendation.
  * 3D scatter plot visualization of university clusters.
  * Integration with Google's Generative AI API (optional) to fetch additional university details.
  * User Q&A functionality for further exploration (optional).

### Technologies Used

  * Python
  * Streamlit
  * Scikit-learn
  * Matplotlib
  * Plotly
  * Google Generative AI API (optional)

### Deployment
This app was deployed via [Streamlit Cloud](https://streamlit.io/cloud).

**Link to your deployed app here:**
[University Recommendation and Insights App](https://uni-recommend-app.streamlit.app/)