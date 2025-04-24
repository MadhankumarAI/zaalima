import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime
import seaborn as sns

# MongoDB config
MONGO_URI = "mongodb+srv://MadhanKumarR:mypassword@cluster0.kgklnih.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["news_project"]
collection = db["news_cleaned"]

# Streamlit page config
st.set_page_config(page_title="📰 News Sentiment Dashboard", layout="wide")

# Custom CSS with improved styling and responsive design
st.markdown("""
    <style>
        /* Base styling */
        body {
            background-color: black;
            font-family: 'Inter', sans-serif;
            color: #333;
        }
        
        /* Main container */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
    
        
        .dashboard-title {
            color: white;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            letter-spacing: -0.5px;
        }
        
        .dashboard-subtitle {
            color: #B5A8D5;
            font-size: 1.1rem;
        }
        
        /* Two-column card layout */
        .row {
            display: flex;
            flex-wrap: wrap;
            margin: -10px;
            clear: both;
        }
        
        .column {
            flex: 0 0 50%;
            max-width: 50%;
            padding: 10px;
            box-sizing: border-box;
        }
        
        /* Card styling */
        .card {
            height: 100%;
            background-color: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            display: flex;
            flex-direction: column;
            border-top: 4px solid #4D55CC;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 20px rgba(33, 28, 132, 0.2);
        }
        
        .card-header {
            padding: 1.5rem 1.5rem 0.75rem;
            position: relative;
        }
        
        .card-topic {
            position: absolute;
            top: 1.25rem;
            right: 1.25rem;
            background-color: #7A73D1;
            color: white;
            padding: 0.35rem 0.85rem;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 500;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 4px rgba(122, 115, 209, 0.2);
        }
        
        .card-date {
            font-size: 0.8rem;
            color: #7A73D1;
            margin-bottom: 0.75rem;
            display: block;
        }
        
        .card-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #211C84;
            line-height: 1.4;
            margin-bottom: 0.75rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        .card-source {
            display: inline-block;
            font-size: 0.85rem;
            color: #7A73D1;
            margin-bottom: 0.75rem;
            font-weight: 500;
        }
        
        .card-body {
            padding: 0 1.5rem 1rem;
            flex-grow: 1;
        }
        
        .card-description {
            color: #555;
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 1rem;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        .card-footer {
            padding: 1rem 1.5rem;
            border-top: 1px solid rgba(181, 168, 213, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #F8F9FE;
        }
        
        .sentiment-badge {
            padding: 0.4rem 0.9rem;
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.3px;
        }
        
        .sentiment-positive {
            background-color: rgba(77, 85, 204, 0.12);
            color: #211C84;
        }
        
        .sentiment-negative {
            background-color: rgba(122, 115, 209, 0.12);
            color: #211C84;
        }
        
        .sentiment-neutral {
            background-color: rgba(181, 168, 213, 0.12);
            color: #211C84;
        }
        
        .card-link {
            font-size: 0.9rem;
            color: #4D55CC;
            text-decoration: none;
            font-weight: 600;
            display: flex;
            align-items: center;
            transition: all 0.2s ease;
        }
        
        .card-link:hover {
            color: #211C84;
            text-decoration: underline;
        }
        
        /* Visualization section */
        .viz-section {
            background-color: white;
            border-radius: 12px;
            padding: 2.5rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
            margin-top: 2.5rem;
            border-top: 4px solid #4D55CC;
        }
        
        .viz-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #211C84;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #EAECF3;
        }
        
        .sidebar-header {
            font-size: 1.25rem;
            font-weight: 700;
            color: #211C84;
            margin: 1rem 0;
            padding-left: 1rem;
        }
        
        .filter-section {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border-left: 4px solid #7A73D1;
        }
        
        /* Streamlit element customization */
        .stButton > button {
            background-color: #4D55CC;
            color: white;
            border: none;
            padding: 0.6rem 1rem;
            font-weight: 600;
            border-radius: 8px;
            width: 100%;
            transition: background-color 0.2s ease;
        }
        
        .stButton > button:hover {
            background-color: #211C84;
        }
        
        div[data-testid="stDateInput"] > div {
            width: 100%;
        }
        
        /* Responsive design */
        @media (max-width: 992px) {
            .column {
                flex: 0 0 100%;
                max-width: 100%;
            }
            
            .dashboard-title {
                font-size: 1.8rem;
            }
            
            .dashboard-subtitle {
                font-size: 1rem;
            }
            
            .viz-section {
                padding: 1.5rem;
            }
        }
        
        /* Mobile optimization */
        @media (max-width: 768px) {
            .dashboard-header {
                padding: 1.5rem 1rem;
            }
            
            .card-header, .card-body, .card-footer {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            
            .card-title {
                font-size: 1.2rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar filters with improved styling
with st.sidebar:
    st.markdown('<div class="sidebar-header">📅 Filter Options</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        selected_date = st.date_input("Select a date", value=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        reset_button = st.button("🔄 Reset Filters", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Load data from MongoDB
if selected_date:
    start_dt = datetime.combine(selected_date, datetime.min.time())
    end_dt = datetime.combine(selected_date, datetime.max.time())
    query = {"publishedAt": {"$gte": start_dt.isoformat(), "$lte": end_dt.isoformat()}}
else:
    query = {}

docs = list(collection.find(query))
df = pd.DataFrame(docs)

# If no articles are found from MongoDB, load from CSV
if df.empty:
    
    # Load the CSV file as a fallback
    csv_file_path = "news_cleaned.csv"
    df = pd.read_csv(csv_file_path)

# If reset button is clicked, reload all
if reset_button:
    df = pd.DataFrame(list(collection.find({})))  # Reload from MongoDB
    selected_date = None

# Filtering logic for articles based on date
if selected_date:
    filtered_articles = [article for article in df.to_dict(orient='records') if article['publishedAt'][:10] == selected_date.strftime('%Y-%m-%d')]
else:
    filtered_articles = df.to_dict(orient='records')

# Dashboard Header
st.markdown('<div class="dashboard-header">', unsafe_allow_html=True)
if selected_date:
    st.markdown(f'<div class="dashboard-title">📰 News from {selected_date.strftime("%B %d, %Y")}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="dashboard-title">📰 Latest News Dashboard</div>', unsafe_allow_html=True)
st.markdown(f'<div class="dashboard-subtitle">Displaying {len(filtered_articles)} articles with sentiment analysis</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sentiment data
sentiment_emojis = {"positive": "😊", "negative": "😞", "neutral": "😐"}

# No articles message
if not filtered_articles:
    st.warning("No articles found for the selected date.")
else:
    # Create row container
    st.markdown('<div class="row">', unsafe_allow_html=True)
    
    # Loop through articles
    for i, article in enumerate(filtered_articles):
        # Format date for display
        try:
            article_date = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
            formatted_date = article_date.strftime("%b %d, %Y • %I:%M %p")
        except:
            formatted_date = article['publishedAt']
        
        # Get topic
        topic = article.get('topic', 'General')
        
        # Get sentiment class
        sentiment = article.get('sentiment', 'neutral')
        sentiment_class = f"sentiment-{sentiment}"
        
        # Truncate title and description if needed
        title = article.get('title', 'No Title')
        description = article.get('description', 'No description available')
        source = article.get('source', 'Unknown Source')
        
        # Open column div
        st.markdown('<div class="column">', unsafe_allow_html=True)
        
        # Build the card HTML
        st.markdown(f"""
        <div class="card">
            <div class="card-header">
                <div class="card-topic">{topic.capitalize()}</div>
                <span class="card-date">{formatted_date}</span>
                <h3 class="card-title">{title}</h3>
                <span class="card-source">Source: {source}</span>
            </div>
            <div class="card-body">
                <p class="card-description">{description}</p>
            </div>
            <div class="card-footer">
                <span class="sentiment-badge {sentiment_class}">{sentiment_emojis.get(sentiment, '')} {sentiment.capitalize()}</span>
                <a href="{article.get('url', '#')}" target="_blank" class="card-link">Read Article →</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Close column div
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Close row container
    st.markdown('</div>', unsafe_allow_html=True)

    # Visualizations section with updated color palette
    st.markdown('<div class="viz-section">', unsafe_allow_html=True)
    st.markdown('<div class="viz-title">📊 Sentiment Analysis Overview</div>', unsafe_allow_html=True)
    
    # Calculate sentiment distribution
    sentiment_counts = pd.Series([article.get('sentiment', 'neutral') for article in filtered_articles]).value_counts()
    
    # Define colors for visualization using the specified color palette
    sentiment_colors = {
        "positive": "#211C84", 
        "negative": "#4D55CC", 
        "neutral": "#7A73D1"
    }
    colors = [sentiment_colors.get(s, "#B5A8D5") for s in sentiment_counts.index]
    
    # Create visualizations in columns
    col1, col2 = st.columns(2)
    
    with col1:
        fig1, ax1 = plt.subplots(figsize=(8, 8))
        # Set figure background color
        fig1.patch.set_facecolor('#FFFFFF')
        
        # Create the pie chart
        wedges, texts, autotexts = ax1.pie(
            sentiment_counts, 
            labels=sentiment_counts.index, 
            autopct='%1.1f%%',
            colors=colors, 
            startangle=90,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'antialiased': True},
            textprops={'color': '#211C84', 'fontweight': 'bold', 'fontsize': 12}
        )
        
        # Style the percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax1.axis("equal")
        plt.title("Sentiment Distribution", fontsize=18, pad=20, color='#211C84', fontweight='bold')
        st.pyplot(fig1)
    
    with col2:
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        # Set figure background color
        fig2.patch.set_facecolor('#FFFFFF')
        
        # Create bar chart with custom styling
        bars = sns.barplot(
            x=sentiment_counts.index, 
            y=sentiment_counts.values, 
            palette=colors, 
            ax=ax2
        )
        
        # Add a subtle grid
        ax2.grid(axis='y', linestyle='--', alpha=0.3)
        
        # Customize bar chart appearance
        ax2.set_ylabel("Number of Articles", fontsize=12, fontweight='bold', color='#211C84')
        ax2.set_xlabel("Sentiment", fontsize=12, fontweight='bold', color='#211C84')
        ax2.set_title("Sentiment Distribution", fontsize=18, pad=20, color='#211C84', fontweight='bold')
        
        # Remove top and right spines
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_color('#B5A8D5')
        ax2.spines['bottom'].set_color('#B5A8D5')
        ax2.tick_params(colors='#4D55CC')
        
        # Add count labels on top of bars
        for i, v in enumerate(sentiment_counts):
            ax2.text(i, v + 0.5, str(v), ha='center', fontsize=14, color='#211C84', fontweight='bold')
            
        st.pyplot(fig2)
    
    st.markdown('</div>', unsafe_allow_html=True)