import streamlit as st
import os
import requests

# Page Config
st.set_page_config(
    page_title="InfluencerHub - Your Creative Journey Starts Here",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Constants
API_URL = os.getenv("API_URL", "http://localhost:8000")
HOSTINGER_PURPLE = "#674CC4"
HOSTINGER_DARK = "#2F1C6A"

# Custom CSS for Hostinger Look & Feel
st.markdown(f"""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;500;700&display=swap');

        /* General Body */
        .stApp {{
            background-color: #F4F5F7;
            font-family: 'DM Sans', sans-serif;
            color: #2F1C6A;
        }}
        
        /* Headers */
        h1, h2, h3 {{
            font-family: 'DM Sans', sans-serif !important;
            color: #2F1C6A !important;
            font-weight: 700 !important;
        }}

        /* Buttons (Hostinger Purple) */
        .stButton>button {{
            background-color: {HOSTINGER_PURPLE} !important;
            color: white !important;
            border-radius: 50px !important;
            padding: 0.75rem 2rem !important;
            font-size: 1.1rem !important;
            border: none !important;
            font-weight: 700 !important;
            transition: all 0.3s ease !important;
        }}
        .stButton>button:hover {{
            background-color: {HOSTINGER_DARK} !important;
            transform: scale(1.05);
            box-shadow: 0 4px 14px 0 rgba(103, 76, 196, 0.39) !important;
        }}

        /* Cards/Containers */
        .css-1r6slb0, .css-12oz5g7 {{  /* Streamlit container classes vary, using generic styling strategies */
            background-color: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        }}
        
        div[data-testid="stMetricValue"] {{
            color: {HOSTINGER_PURPLE} !important;
        }}

        /* Custom Hero Section Class */
        .hero-title {{
            font-size: 3.5rem;
            line-height: 1.2;
            margin-bottom: 1rem;
            text-align: center;
        }}
        .hero-subtitle {{
            font-size: 1.5rem;
            color: #545778;
            margin-bottom: 2rem;
            text-align: center;
        }}
    </style>
""", unsafe_allow_html=True)

def main():
    # Navbar (Simulated)
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.write("🟣 **InfluencerHub**")
    with col3:
        st.button("Log In")

    # Hero Section
    st.markdown('<div style="padding: 4rem 0;">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Turn Your Influence<br>Into Verified Income</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">The all-in-one platform for creators. Everything you need to manage campaigns, payments, and growth.</p>', unsafe_allow_html=True)
    
    col_cta1, col_cta2, col_cta3 = st.columns([1, 1, 1])
    with col_cta2:
       st.button("Start Now", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Features / Pricing Cards Style
    st.markdown("### Choose your path")
    
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        with st.container(border=True):
            st.markdown(f"#### 🚀 Creator Starter")
            st.markdown("Everything you need to start your journey.")
            st.markdown(f"<h2 style='color: {HOSTINGER_PURPLE}'>Free</h2>", unsafe_allow_html=True)
            st.write("✔️ Basic Analytics")
            st.write("✔️ 1 Active Campaign")
            st.write("✔️ Standard Support")
            st.button("Select Starter", key="btn_starter")

    with col_b:
         with st.container(border=True):
            st.markdown(f"#### ⭐ Premium Influencer")
            st.markdown("For professional creators scaling up.")
            st.markdown(f"<h2 style='color: {HOSTINGER_PURPLE}'>$29.99/mo</h2>", unsafe_allow_html=True)
            st.write("✔️ Advanced Analytics")
            st.write("✔️ Unlimited Campaigns")
            st.write("✔️ Priority Support")
            st.button("Select Premium", key="btn_premium")

    with col_c:
         with st.container(border=True):
            st.markdown(f"#### 🏢 Brand Business")
            st.markdown("Optimized for agencies and brands.")
            st.markdown(f"<h2 style='color: {HOSTINGER_PURPLE}'>$99.99/mo</h2>", unsafe_allow_html=True)
            st.write("✔️ Dedicated Account Manager")
            st.write("✔️ API Access")
            st.write("✔️ Custom Contracts")
            st.button("Select Business", key="btn_business")

    # API Status Section (Original Functionality Preserved)
    st.markdown("---")
    st.subheader("System Status")
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            st.success("✅ All Systems Operational")
        else:
            st.error("⚠️ System Issues Detected")
    except:
        st.warning("⚠️ Connecting to backend...")

if __name__ == "__main__":
    main()
