import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from backend.database import get_all_reviews, add_review
from backend.ai_analysis import analyze_review

st.set_page_config(
    page_title="MetaWell AI Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 MetaWell AI - Customer Review Insights")

# Load reviews
reviews = get_all_reviews()
df = pd.DataFrame(reviews)

if not df.empty:
    st.subheader("Overall Sentiment")
    sentiment_counts = df["sentiment"].value_counts(normalize=True) * 100
    st.bar_chart(sentiment_counts)

    st.subheader("Category Breakdown")
    category_counts = df["category"].value_counts(normalize=True) * 100
    st.bar_chart(category_counts)

    st.subheader("Raw Reviews")
    st.dataframe(df)
else:
    st.info("No reviews found yet. Add one below!")

# Manual test input
st.subheader("Test Review Analysis")
new_review = st.text_area("Enter a customer review")
if st.button("Analyze"):
    result = analyze_review(new_review)
    st.write("### Result")
    st.write(f"Sentiment: **{result['sentiment']}**")
    st.write(f"Category: **{result['category']}**")

    # Save to DB
    add_review(new_review, result["sentiment"], result["category"])
    st.success("✅ Saved to database!")
