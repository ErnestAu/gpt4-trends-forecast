# Popularity Trend Explorer with Chatbot

## Introduction
This project is a Streamlit web application that allows users to explore the popularity of keywords over time based on Google Trends data. 
It provides both historical and forecasted trends for the keywords. 
Additionally, the app incorporates a chatbot trained to answer questions about the trend data.

## Features
- Explore keyword popularity using Google Trends data by country.
- Forecast future keyword trends using the Prophet model.
- Ask the chatbot questions related to the trends or the methodology used.
- Allows for multiple keywords to be searched and compared simultaneously.

## Installation
1. Clone the repository
    git clone https://github.com/ErnestAu/gpt4-trends-forecast
2. Navigate to the project directory
    cd gpt4-trends-forecast
3. Install the requirements from `requirements.txt`
    pip install -r requirements.txt
  
## Usage
To run the Streamlit app locally, execute the following command in your terminal:
streamlit run app.py

##Get an OpenAI API key
You can get your own OpenAI API key by following the following instructions:

1.Go to https://platform.openai.com/account/api-keys.
2.Click on the + Create new secret key button.
3.Next, enter an identifier name (optional) and click on the Create secret key button.