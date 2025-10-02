import streamlit as st
from backend.database import get_all_reviews, add_review
from backend.ai_analysis import analyze_review

# =====================================================
# 🎨 Custom Styling for Modern AI Dashboard
# =====================================================
st.set_page_config(
    page_title="📊 MetaWell AI - Customer Review Insights",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        /* Title */
        .css-10trblm, .css-1avcm0n {
            font-size: 2.4rem !important;
            color: #00f5d4 !important;
            font-weight: 800 !important;
        }

        /* Subheaders */
        h2, h3 {
            color: #4af1c9 !important;
        }

        /* Review Cards */
        .review-card {
            background: linear-gradient(145deg, #161b22, #0d1117);
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
            transition: 0.3s;
        }
        .review-card:hover {
            transform: scale(1.01);
            box-shadow: 0px 6px 20px rgba(0,0,0,0.7);
        }

        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #00f5d4, #0affb8) !important;
            color: #0d1117 !important;
            font-weight: bold !important;
            border-radius: 12px !important;
            border: none;
            padding: 0.6rem 1.2rem;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #0affb8, #00f5d4) !important;
            transform: translateY(-2px);
        }

        /* Inputs */
        .stTextArea textarea, .stTextInput input {
            background: #161b22 !important;
            border-radius: 10px !important;
            color: #e6edf3 !important;
            border: 1px solid #30363d !important;
        }

        /* Alerts */
        .stAlert {
            border-radius: 12px !important;
        }
    </style>
""", unsafe_allow_html=True)

# =====================================================
# 📊 Main Dashboard
# =====================================================
st.title("📊 MetaWell AI - Customer Review Insights")
st.write("Gain AI-powered insights from customer feedback across categories like **Network, Billing, Delivery, Service, Fraud, and more.**")

# =====================================================
# 🗂 Show Reviews Section
# =====================================================
st.subheader("📝 Customer Reviews")
reviews = get_all_reviews()

if not reviews:
    st.info("No reviews found yet. Add one below!")
else:
    for r in reviews:
        st.markdown(f"""
            <div class="review-card">
                <b style="color:#00f5d4;">{r['category']} | {r['sentiment']}</b><br>
                {r['text']} <br>
                <small style="color: #8b949e;">{r['created_at']}</small>
            </div>
        """, unsafe_allow_html=True)

# =====================================================
# ➕ Add New Review Section
# =====================================================
st.subheader("➕ Add a New Review")

with st.form("add_review_form"):
    new_review = st.text_area("Enter a customer review", placeholder="Type your review here...")
    submitted = st.form_submit_button("Analyze & Add")

    if submitted and new_review.strip():
        try:
            # Analyze review with AI
            result = analyze_review(new_review)
            sentiment = result["sentiment"]
            category = result["category"]

            # Save to database
            add_review(new_review, sentiment, category)

            st.success(f"✅ Review added! Sentiment: **{sentiment}**, Category: **{category}**")
        except Exception as e:
            st.error(f"❌ Error analyzing review: {str(e)}")
