
# 📈 Popularity Trend Explorer

## Introduction
This project is a Streamlit web application that allows users to explore the popularity of keywords over time based on Google Trends data. It provides both historical and forecasted trends for the keywords. Additionally, the app incorporates a chatbot trained to answer questions about the trend data.

## Features
- Explore keyword popularity using Google Trends data by country.
- Forecast future keyword trends using the Prophet model.
- Ask the chatbot questions related to the trends or the methodology used.
- Allows for multiple keywords to be searched and compared simultaneously.

## Installation
1. **Clone the repository**
   ```
   git clone https://github.com/ErnestAu/gpt4-trends-forecast 
   ```
2. **Navigate to the project directory**
   ```
   cd gpt4-trends-forecast
   ```
3. **Create a new virtual environment named `venv`**
   - For Windows:
     ```
     python -m venv venv
     ```
   - For macOS/Linux:
     ```
     python3 -m venv venv
     ```
4. **Activate the virtual environment**
   - For Windows:
     ```
     .\venv\Scripts\activate
     ```
   - For macOS/Linux:
     ```
     source venv/bin/activate
     ```
5. **Install the requirements from `requirements.txt`**
   ```
   pip install -r requirements.txt
   ```
6. **Set up the `.env` file from the `.env.example` template**
   - Copy the `.env.example` file to a new file named `.env` in the same directory. You can do this from the command line as follows:
     - For Windows:
       ```
       copy .env.example .env
       ```
     - For macOS/Linux:
       ```
       cp .env.example .env
       ```
7. **Add your OpenAI API key to the `.env` file**
   - Open the `.env` file in a text editor of your choice.
   - You will see a line that looks like this:
     ```
     openai_api_key = ""
     ```
   - Place your OpenAI API key between the quotes. For example:
     ```
     openai_api_key = "your_api_key_here"
     ```

## Usage
To run the Streamlit app locally, execute the following command in your terminal:
```
streamlit run popularity_trend_explorer.py
```

## Get an OpenAI API key
You can get your own OpenAI API key by following the instructions below:

1. Go to https://platform.openai.com/account/api-keys.
2. Click on the "+ Create new secret key" button.
3. Next, enter an identifier name (optional) and click on the "Create secret key" button.
