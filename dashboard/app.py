import streamlit as st
import pandas as pd
from backend.database import get_all_reviews
from backend.ai_analysis import analyze_review
from backend.scraper_google import get_google_reviews
from backend.scraper_hellopeter import scrape_hellopeter
from dashboard.styles import *

st.set_page_config(page_title="MetaWell AI Dashboard", layout="wide")

st.markdown(f"<h1 style='color:{PRIMARY_COLOR}'>MetaWell AI Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# Collect reviews section
with st.expander("Collect Reviews"):
    place_id = st.text_input("Enter Google Place ID:")
    hellopeter_url = st.text_input("Enter HelloPeter Business URL:")
    if st.button("Fetch Reviews"):
        if place_id:
            get_google_reviews(place_id)
        if hellopeter_url:
            scrape_hellopeter(hellopeter_url)
        st.success("Reviews collected successfully!")

# Load reviews
reviews = get_all_reviews()
df = pd.DataFrame(reviews)

# Analyze reviews
if st.button("Analyze All Reviews") and not df.empty:
    for index, row in df.iterrows():
        analyze_review(row['id'], row['text'])
    st.success("Analysis complete!")
    df = pd.DataFrame(get_all_reviews())

# Display visual insights
if not df.empty and 'category' in df.columns and 'sentiment' in df.columns:
    st.subheader("Sentiment Distribution")
    st.bar_chart(df['sentiment'].value_counts(normalize=True) * 100)

    st.subheader("Complaint Categories")
    st.bar_chart(df['category'].value_counts(normalize=True) * 100)

    st.subheader("Latest Reviews")
    st.dataframe(df[['author','text','category','sentiment']])

