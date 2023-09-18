import streamlit as st
from pytrends.request import TrendReq
from prophet import Prophet
import pandas as pd
import plotly.graph_objects as go

country_list = [
    ("Worldwide", ""),
    ("United States", "US"),
    ("United Kingdom", "GB"),
    ("India", "IN"),
    ("Canada", "CA")
]

today = pd.Timestamp.now().strftime("%Y-%m-%d")

def fit_and_forecast(df):
    m = Prophet()
    m.fit(df[['ds', 'y']])
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    return forecast

def plot_trend(fig, df, forecast, keyword, color):
    # Actual 
    fig.add_trace(go.Scatter(
        x=df['ds'][df['ds'] <= today],
        y=df['y'][df['ds'] <= today],
        mode='lines',
        name=f'Actual for {keyword}',
        line=dict(color=color['Actual']),
        hovertemplate='Date: %{x}<br>Value: %{y}'
    ))

    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast['ds'][forecast['ds'] > today],
        y=forecast['yhat'][forecast['ds'] > today],
        mode='lines',
        name=f'Forecast for {keyword}',
        line=dict(color=color['Forecast']),
        hovertemplate='Date: %{x}<br>Value: %{y}'
    ))

    # Confidence interval
    fig.add_trace(go.Scatter(
        x=forecast['ds'][forecast['ds'] > today],
        y=forecast['yhat_upper'][forecast['ds'] > today],
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        fillcolor=color['ConfidenceInterval'],
        fill='tonexty',
        hoverinfo='skip'
    ))

    fig.add_trace(go.Scatter(
        x=forecast['ds'][forecast['ds'] > today],
        y=forecast['yhat_lower'][forecast['ds'] > today],
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        fillcolor=color['ConfidenceInterval'],
        fill='tonexty',
        hoverinfo='skip'
    ))
    
    return fig

# Initialize color dictionary for graph
color_dict = {
    'Keyword1': {'Actual': '#2E86C1', 'Forecast': '#5DADE2', 'ConfidenceInterval': 'rgba(93, 173, 226, 0.3)'},
    'Keyword2': {'Actual': '#BFC9CA', 'Forecast': '#D5DBDB', 'ConfidenceInterval': 'rgba(213, 219, 219, 0.3)'},
    'Keyword3': {'Actual': '#58D68D', 'Forecast': '#7DCEA0', 'ConfidenceInterval': 'rgba(125, 206, 160, 0.3)'}
}

st.title("📈 Popularity Trend Explorer")

st.markdown("""
Welcome to the Popularity Trend Explorer! Ever wondered how popular certain keywords are over time?

With this tool, you can:

- 📊 Discover the historical popularity of up to 3 keywords of your choice.
- 🚀 Get forecasts for keyword trends for the next year.
- 🌍 See how these trends differ from country to country.

---

- **Data Source**: Google Trends
- **Forecasting Model**: Prophet
""")

col1, col2 = st.columns(2)

# Number of keywords selector
with col1:
    num_keywords = st.selectbox("Number of Keywords", [1, 2, 3], format_func=lambda x: f"{x} Keyword{'s' if x > 1 else ''}")

# Country selector 
with col2:
    selected_country, selected_country_code = st.selectbox("Country", country_list, format_func=lambda x: x[0])

# Keywords
keyword1 = st.text_input("Enter first keyword", "")
keyword2, keyword3 = "", ""
if num_keywords >= 2:
    keyword2 = st.text_input("Enter second keyword", "")
if num_keywords == 3:
    keyword3 = st.text_input("Enter third keyword", "")

# Initialize a text string to hold the data
text_data = ""

# Button
if st.button("Check Popularity"):
    pytrends = TrendReq(hl='en-US', tz=360)
    keywords = [keyword1]
    if keyword2:
        keywords.append(keyword2)
    if keyword3:
        keywords.append(keyword3)
    
    pytrends.build_payload(keywords, cat=0, timeframe='today 5-y', geo=selected_country_code, gprop='')
    data = pytrends.interest_over_time()

    fig = go.Figure()

    for i, keyword in enumerate(keywords):
        color = color_dict[f'Keyword{i+1}']
        df = data.reset_index().rename(columns={'date': 'ds', keyword: 'y'})
        forecast = fit_and_forecast(df)

        # Add to text_data with rounding to the nearest whole number and sampling every 2nd point
        text_data += f"{i+1}K|{keyword}|"
        text_data += "|A|" + ','.join(map(lambda x: str(round(x)), df['y'][df['ds'] <= pd.Timestamp.now().strftime("%Y-%m-%d")][::2].tolist()))
        text_data += "|F|" + ','.join(map(lambda x: str(round(x)), forecast['yhat'][forecast['ds'] > pd.Timestamp.now().strftime("%Y-%m-%d")][::2].tolist()))
        text_data += "|CI_Upper|" + ','.join(map(lambda x: str(round(x)), forecast['yhat_upper'][forecast['ds'] > pd.Timestamp.now().strftime("%Y-%m-%d")][::2].tolist()))
        text_data += "|CI_Lower|" + ','.join(map(lambda x: str(round(x)), forecast['yhat_lower'][forecast['ds'] > pd.Timestamp.now().strftime("%Y-%m-%d")][::2].tolist()))
        text_data += "|"

        fig = plot_trend(fig, df, forecast, keyword, color)

    # Add vertical line to indicate 'today'
    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=today,
            x1=today,
            y0=0,
            y1=1,
            yref="paper",
            line=dict(color="rgba(255, 255, 255, 0.2)", width=2) 
        )
    )

    # Add annotation to label 'today' 
    fig.add_annotation(
        x=today,
        y=1,
        yref="paper",
        xanchor="left",
        yanchor="bottom",  
        text="Today",
        showarrow=False,
        font=dict(size=12, color="rgba(255, 255, 255, 0.7)")  
    )

    keywords = [keyword.capitalize() for keyword in keywords]

    if len(keywords) == 1:
        title = f"Popularity Trend Forecast for {keywords[0]} ({selected_country})"
    elif len(keywords) == 2:
        title = f"Popularity Trend Forecast for {keywords[0]} and {keywords[1]} ({selected_country})"
    else:
        title = f"Popularity Trend Forecast for {keywords[0]}, {keywords[1]}, and {keywords[2]} ({selected_country})"

    fig.update_layout(title=title)
    st.plotly_chart(fig)

# Remove the last separator 
text_data = text_data.rstrip("|")

# Write to text_data.txt 
with open("text_data/text_data.txt", "w") as f:
    f.write(text_data)

# Write to selected_country.txt
with open("text_data/selected_country.txt", "w") as f:
    f.write(selected_country)
