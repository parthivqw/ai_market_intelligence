import streamlit as st
import json
import pandas as pd
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Market Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading Functions ---
@st.cache_data # Cache the data for performance
def load_all_data():
    # Phase 1-4 Data
    insights_path = 'insights.json'
    combined_data_path = 'data/processed/combined_market_data.csv'
    
    insights_data = None
    if os.path.exists(insights_path):
        with open(insights_path, 'r', encoding='utf-8') as f:
            insights_data = json.load(f)
            
    combined_df = pd.read_csv(combined_data_path) if os.path.exists(combined_data_path) else None

    # Phase 5 Data
    d2c_insights_path = 'phase5_extension/d2c_insights.json'
    d2c_creative_path = 'phase5_extension/d2c_creative_outputs.json'

    d2c_insights = None
    if os.path.exists(d2c_insights_path):
        with open(d2c_insights_path, 'r') as f:
            d2c_insights = json.load(f)

    d2c_creative = None
    if os.path.exists(d2c_creative_path):
        with open(d2c_creative_path, 'r') as f:
            d2c_creative = json.load(f)
            
    return insights_data, combined_df, d2c_insights, d2c_creative

# Load all potential data
app_insights, combined_df, d2c_insights, d2c_creative = load_all_data()

# --- Sidebar Navigation ---
st.sidebar.title("Dashboard Navigation")
st.sidebar.info("Select which analysis you would like to view.")
page = st.sidebar.radio("Choose a section:", ["App Market Intelligence", "D2C Marketing Extension"])


# --- Main Page Content ---

if page == "App Market Intelligence":
    st.title("📊 App Market Intelligence Dashboard (Phases 1-4)")
    st.markdown("An automated analysis of the top 100 Android and iOS mobile applications.")

    if app_insights:
        st.markdown("---")
        st.header("💡 Key Strategic Insights")
        for insight in app_insights:
            st.subheader(insight['title'])
            st.metric(label="Insight Type", value=insight['insight_type'])
            st.info(f"**Summary:** {insight['summary']}")
            st.warning(f"**Recommendation:** {insight['recommendation']}")
            st.progress(insight['confidence_score'], text=f"Confidence: {int(insight['confidence_score']*100)}%")
            with st.expander("Show Supporting Data"):
                st.json(insight['supporting_data'])
    else:
        st.error("Could not find 'insights.json'. Please run the Phase 3 script.")
        
    if st.checkbox("Show Combined App Market Raw Data"):
        if combined_df is not None:
            st.dataframe(combined_df)
        else:
            st.error("Could not find 'combined_market_data.csv'. Please run the Phase 2 script.")

elif page == "D2C Marketing Extension":
    st.title("🚀 D2C Marketing Extension (Phase 5)")
    st.markdown("An analysis of D2C campaign data and AI-generated creative content.")

    if d2c_insights and d2c_creative:
        st.markdown("---")
        st.header("📈 Key D2C Insights")
        
        # Display D2C Insights
        roas_insight = d2c_insights['best_roas_campaign']
        seo_insight = d2c_insights['top_seo_opportunity']
        st.success(f"**Best Campaign:** '{roas_insight['id']}' on {roas_insight['channel']} had a massive ROAS of **{roas_insight['roas']}**.")
        st.info(f"**Top SEO Opportunity:** The category '{seo_insight['category']}' has high search volume but a low ranking, making it a prime target for growth.")
        
        st.markdown("---")
        st.header("🤖 AI-Generated Creative Content")

        st.subheader("Generated Ad Headlines")
        st.markdown(d2c_creative['ad_headlines'].replace('\n', '\n\n'))
        
        st.subheader("Generated SEO Meta Description")
        st.markdown(d2c_creative['seo_description'])
    else:
        st.error("Could not find Phase 5 output files. Please run both Phase 5 scripts first.")