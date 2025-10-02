import sys, os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# dashboard/app.py
import streamlit as st
import pandas as pd
from backend.ai_analysis import analyze_review
from backend.database import get_all_reviews, add_review

st.set_page_config(page_title="MetaWell AI", layout="wide")

st.markdown(
    """
    <style>
    .main {background-color:#111827; color:white; font-family:sans-serif;}
    table {border:1px solid #ccc; border-collapse:collapse;}
    th, td {border:1px solid #444; padding:8px; text-align:center;}
    </style>
    """, unsafe_allow_html=True
)

st.title("📊 MetaWell AI - Customer Review Insights")

# --- CSV upload ---
uploaded_file = st.file_uploader("Upload CSV with reviews", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'review' not in df.columns:
        st.error("CSV must have a 'review' column.")
    else:
        st.success(f"✅ {len(df)} reviews uploaded!")
        processed_reviews = []
        for _, row in df.iterrows():
            review_text = row['review']
            analysis = analyze_review(review_text)
            add_review(
                review_text,
                analysis.get("sentiment", "Unknown"),
                analysis.get("category", "Other"),
                analysis.get("ai_response", "")
            )
            processed_reviews.append({
                "review": review_text,
                **analysis
            })
        result_df = pd.DataFrame(processed_reviews)
        st.subheader("📖 AI Analyzed Reviews")
        st.dataframe(result_df)

        # Summary stats
        st.subheader("📊 Summary")
        st.write("**Sentiment distribution:**")
        st.bar_chart(result_df['sentiment'].value_counts())
        st.write("**Category distribution:**")
        st.bar_chart(result_df['category'].value_counts())

        # --- CSV download ---
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Results CSV",
            data=csv,
            file_name="analyzed_reviews.csv",
            mime="text/csv"
        )




