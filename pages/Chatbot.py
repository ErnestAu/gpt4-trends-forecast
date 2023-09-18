import os
import openai 
import streamlit as st

# Load the text data
try:
    with open("text_data/text_data.txt", "r") as f:
        text_data = f.read()
except FileNotFoundError:
    text_data = ""

try:
    with open("text_data/selected_country.txt", "r") as f:
        selected_country = f.read().strip()
except FileNotFoundError:
    selected_country = "Worldwide"

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    model_version = st.selectbox("Model Version", ["gpt-3.5-turbo-16k", "gpt-4"])
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("💬 Chatbot")

st.markdown("""
This AI chatbot is trained to answer your queries based on Google Trends data. 

To get contextual responses, please ensure you have visited the 'Check Popularity Trend' page and entered some keywords for analysis.
            
#### Sample Questions You Can Ask:

1. "What do the trend graphs mean?"
2. "Can you explain how the forecasting works?"
3. "What does the confidence interval indicate?"
4. "Can you give me more information about the data granularity?"
5. "How can I make the most of this tool for market research?"
6. "What are some limitations of this trend analysis?"
""")

# Initialize the session state messages if not already initialized
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": f"Google Trends data for {selected_country}.\n"
                    "Key:\n"
                    "- A: Actual\n"
                    "- F: Forecast\n"
                    "- CI_Upper: Upper CI\n"
                    "- CI_Lower: Lower CI\n"
                    "Data rounded to whole numbers, sampled every 2nd point.\n"
                    "Timeframe: Past 5 years, 1 year future.\n"
                    "Forecast: Prophet model.\n"
                    "CI: Confidence range.\n"
                    f"Data: {text_data if text_data else 'No keywords.'}"
        },
        {
            "role": "assistant",
            "content": "How may I help you today?"
        }
    ]

# Display the messages, skipping system messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# Input and interaction handling
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    if not text_data:
        st.info("Please enter keywords in Popularity Trend Explorer to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.spinner('Generating response...'):  # Display a spinner while the chatbot is generating a response
        response = openai.ChatCompletion.create(model=model_version, messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg["content"])
