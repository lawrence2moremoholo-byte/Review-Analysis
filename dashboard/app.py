import sys, os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from io import BytesIO
from backend.database import add_review, get_all_reviews
from backend.ai_analysis import analyze_review

# ====== Page Config ======
st.set_page_config(
    page_title="📊 MetaWell AI - Customer Review Insights",
    page_icon="🤖",
    layout="wide"
)

# ====== CSS for modern styling ======
st.markdown("""
    <style>
        .main {
            background-color: #1f1f2e;
            color: #e0e0e0;
            padding: 30px;
            font-family: 'Segoe UI', sans-serif;
        }
        .block-container {
            max-width: 1200px;
            margin: auto;
            padding: 20px;
            border: 1px solid #444;
            border-radius: 10px;
            background-color: #2c2c3e;
        }
        h1 {
            text-align: center;
            color: #00f0ff;
        }
        .stButton button {
            background-color: #00f0ff;
            color: #000;
            font-weight: bold;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #444;
            padding: 8px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="block-container">', unsafe_allow_html=True)
st.title("📊 MetaWell AI - Customer Review Insights")

# ====== Upload CSV ======
st.subheader("📂 Upload Reviews CSV (up to 100 reviews)")
uploaded_file = st.file_uploader("Drag and drop your CSV here", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "review" not in df.columns:
        st.error("❌ CSV must have a column named 'review'")
    else:
        if len(df) > 100:
            st.warning("⚠️ Only the first 100 reviews will be analyzed.")
            df = df.head(100)

        st.success(f"✅ {len(df)} reviews loaded!")

        if st.button("Analyze & Save Reviews"):
            progress = st.progress(0)
            results = []

            for idx, row in df.iterrows():
                review_text = row["review"]

                # AI analysis
                analysis = analyze_review(review_text)

                add_review(
                    review_text,
                    analysis.get("sentiment", "Unknown"),
                    analysis.get("category", "Other"),
                    analysis.get("ai_response", "")
                )

                # Store for display
                results.append({
                    "review": review_text,
                    "sentiment": analysis.get("sentiment", "Unknown"),
                    "category": analysis.get("category", "Other"),
                    "ai_response": analysis.get("ai_response", "")
                })

                progress.progress((idx + 1) / len(df))

            st.success("🎉 All reviews analyzed and saved!")

            # Show results on dashboard
            result_df = pd.DataFrame(results)
            st.dataframe(result_df)

            # ====== Download buttons ======
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name='analyzed_reviews.csv',
                mime='text/csv'
            )

            try:
                from fpdf import FPDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for i, row in result_df.iterrows():
                    pdf.multi_cell(0, 8, f"Review: {row['review']}\nSentiment: {row['sentiment']}\nCategory: {row['category']}\nAI Response: {row['ai_response']}\n\n")
                pdf_output = BytesIO()
                pdf.output(pdf_output)
                pdf_output.seek(0)
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_output,
                    file_name="analyzed_reviews.pdf",
                    mime="application/pdf"
                )
            except:
                st.warning("⚠️ PDF download requires fpdf library. Install with pip install fpdf")

# ====== Show stored reviews ======
st.subheader("📖 Stored Reviews in Database")
reviews = get_all_reviews()
if reviews:
    st.dataframe(reviews)
else:
    st.info("No reviews found in the database yet.")

st.markdown('</div>', unsafe_allow_html=True)

