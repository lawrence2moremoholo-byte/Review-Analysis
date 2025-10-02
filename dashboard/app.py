import sys, os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from backend.database import get_all_reviews, add_review
from backend.ai_analysis import analyze_review

st.set_page_config(
    page_title="📊 MetaWell AI - Customer Review Insights",
    page_icon="🤖",
    layout="wide"
)

st.title("📊 MetaWell AI - Customer Review Insights")

# =========================
# Upload Section
# =========================
st.subheader("📂 Upload Reviews File")
uploaded_file = st.file_uploader("Upload a CSV file with a 'review' column", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "review" not in df.columns:
        st.error("❌ The CSV must have a column named 'review'")
    else:
        st.success(f"✅ {len(df)} reviews uploaded!")

        if st.button("Analyze & Save Reviews"):
            progress = st.progress(0)
            results = []

            for idx, row in df.iterrows():
                review_text = row["review"]

                # AI analysis
                analysis = analyze_review(review_text)

                if "error" not in analysis:
                    add_review(
                        review_text,
                        analysis["sentiment"],
                        analysis["category"],
                        analysis["ai_response"]
                    )
                    results.append(analysis)
                else:
                    results.append({"review": review_text, "error": analysis["error"]})

                progress.progress((idx + 1) / len(df))

            st.success("🎉 All reviews analyzed and saved to Supabase!")

            # Show results
            st.write(pd.DataFrame(results))

# =========================
# Database Viewer
# =========================
st.subheader("📖 Stored Reviews in Database")
reviews = get_all_reviews()
if reviews:
    st.dataframe(reviews)
else:
    st.info("No reviews found in the database.")
