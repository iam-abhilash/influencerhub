import streamlit as st
import os
import requests
from supabase import create_client, Client

# Page Config
st.set_page_config(
    page_title="InfluencerHub | The Global Standard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Constants
API_URL = os.getenv("API_URL", "http://localhost:8000")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase Client
@st.cache_resource
def get_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

# Initialize Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user" not in st.session_state:
    st.session_state.user = None

# Excellence Color Palette
PRIMARY = "#674CC4"
ACCENT = "#A78BFA"
DARK_BG = "#050505"

# Ultra-Premium CSS
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');
        
        /* Hide default Streamlit bits for a clean app feel */
        [data-testid="stHeader"], [data-testid="stDecoration"], [data-testid="stSidebar"] {{
            display: none !important;
        }}
        .block-container {{ 
            padding: 0 !important; 
            max-width: 100% !important; 
        }}
        
        .stApp {{
            background-color: {DARK_BG};
            color: #FFFFFF;
            font-family: 'Outfit', sans-serif;
        }}

        /* Buttons Fix - Professional Rounded Corners */
        .stButton>button {{
            width: 100% !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            background: {PRIMARY} !important;
            color: white !important;
            border: none !important;
            height: 3.2rem !important;
            font-size: 1rem !important;
            transition: all 0.2s ease !important;
            text-transform: none !important;
        }}
        .stButton>button:hover {{
            background: #7C3AED !important;
            box-shadow: 0 5px 15px rgba(103, 76, 196, 0.3) !important;
            transform: translateY(-1px);
        }}
        
        /* Outline variant for secondary buttons */
        div[data-testid="stButton"] button[key*="secondary"] {{
            background: transparent !important;
            border: 1.5px solid rgba(255,255,255,0.15) !important;
        }}
        div[data-testid="stButton"] button[key*="secondary"]:hover {{
            border-color: #FFFFFF !important;
            background: rgba(255,255,255,0.05) !important;
        }}

        /* Navbar Layout Fix */
        .nav-wrapper {{
            padding: 1.5rem 10%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            z-index: 99;
        }}

        .logo-text {{
            font-size: 2.2rem !important; 
            background: linear-gradient(90deg, #FFFFFF 0%, {ACCENT} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: -0.04em;
        }}

        /* Cards/Containers */
        .excellence-card {{
            background: rgba(20, 20, 20, 0.6);
            backdrop-filter: blur(25px);
            border-radius: 24px;
            padding: 2.5rem;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        /* Input styling */
        .stTextInput input {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border-radius: 10px !important;
            height: 3rem !important;
            border: none !important;
            padding-left: 15px !important;
        }}
        .stTextInput label {{
            color: rgba(255,255,255,0.7) !important;
            font-size: 0.9rem !important;
            margin-bottom: 5px !important;
        }}

        /* Feature Section Images */
        .feature-img {{
            border-radius: 20px;
            box-shadow: 0 30px 60px rgba(0,0,0,0.5);
        }}
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

def render_navbar():
    # We use a proper container to avoid "black boxes" or layout ghosts
    cols = st.columns([1, 2, 1])
    with cols[0]:
        st.markdown('<p class="logo-text">InfluencerHub</p>', unsafe_allow_html=True)
    with cols[2]:
        if not st.session_state.user:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Login", key="nav_login_secondary"): navigate_to("login")
            with c2:
                if st.button("Start Free", key="nav_signup"): navigate_to("signup")
        else:
            if st.button("Dashboard", key="nav_dash_secondary"): navigate_to("dashboard")

def render_home():
    # Hero Section
    st.markdown(f"""
        <div style="background: linear-gradient(rgba(5,5,5,0.6), rgba(5,5,5,0.6)), 
                    url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2672&auto=format&fit=crop');
                    background-size: cover; background-position: center; padding: 12rem 10% 8rem 10%; text-align: center;">
            <h1 style="font-size: 5rem; font-weight: 800; line-height: 1.1; margin-bottom: 1.5rem; color: #FFF;">POWERING THE <br><span style="color: {ACCENT}">CREATOR ECONOMY</span></h1>
            <p style="font-size: 1.4rem; color: rgba(255,255,255,0.7); max-width: 800px; margin: 0 auto 3rem auto;">
                The elite operating system to manage campaigns, verify influence, and unlock institutional income globally.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Content Grid
    st.markdown('<div style="padding: 6rem 10%;">', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1], gap="large")
    with col1:
        st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=2426&auto=format&fit=crop", use_container_width=True)
    with col2:
        st.markdown('<div style="padding-top: 2rem;">', unsafe_allow_html=True)
        st.markdown('<h2 style="font-size: 3rem;">Global Scale</h2>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.2rem; color: rgba(255,255,255,0.6); line-height: 1.6;">Experience the power of real-time data ingestion. Track sentiment, engagement velocity, and conversion attribution in a single pane of glass.</p>', unsafe_allow_html=True)
        if st.button("Join the Ecosystem", key="cta_home"): navigate_to("signup")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_auth(mode="login"):
    # Clean background for auth
    bg_img = "https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=2601&auto=format&fit=crop"
    st.markdown(f"""
        <div style="background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url('{bg_img}'); 
                    background-size: cover; min-height: 100vh; display: flex; align-items: center; justify-content: center; padding-top: 10vh;">
    """, unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown('<div class="excellence-card">', unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; margin-bottom: 0.5rem;'>{mode.capitalize()}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; opacity: 0.5; margin-bottom: 2rem;'>InfluencerHub Secure Portal</p>", unsafe_allow_html=True)
        
        email = st.text_input("Corporate ID", placeholder="name@company.com", key=f"{mode}_email")
        password = st.text_input("Access Token", type="password", placeholder="••••••••", key=f"{mode}_pass")
        
        if mode == "signup":
            if st.button("Establish Identity", key="auth_btn_main"):
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("✅ Handshake initiated. Check your inbox.")
                except Exception as e: st.error(f"Failed: {e}")
        else:
            if st.button("Authorize Access", key="auth_btn_main"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = res.user
                    navigate_to("dashboard")
                except: st.error("Access Denied. Check credentials.")
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        if mode == "login":
            if st.button("Create New Account", key="auth_toggle_secondary"): navigate_to("signup")
        else:
            if st.button("Return to Login", key="auth_toggle_secondary"): navigate_to("login")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard():
    st.markdown(f"""
        <div style="padding: 4rem 10%; background: {DARK_BG}; min-height: 100vh;">
            <h1 style="margin-bottom: 0.5rem;">Mission Control</h1>
            <p style="opacity: 0.5; margin-bottom: 3rem;">Authorized User: {st.session_state.user.email}</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    metrics = [("Campaigns", "12", "+2"), ("Verified Earnings", "$4.2k", "↑"), ("Global Rank", "#452", "-")]
    for i, col in enumerate([col1, col2, col3]):
        with col:
            st.markdown(f'<div class="excellence-card" style="padding: 1.5rem; text-align: center;">', unsafe_allow_html=True)
            st.metric(metrics[i][0], metrics[i][1], metrics[i][2])
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Sign Out", key="logout_btn"):
        supabase.auth.sign_out()
        st.session_state.user = None
        navigate_to("home")
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    if not supabase: st.error("Core Infrastructure Missing")
    
    if st.session_state.page == "home":
        render_navbar()
        render_home()
    elif st.session_state.page == "login":
        render_auth("login")
    elif st.session_state.page == "signup":
        render_auth("signup")
    elif st.session_state.page == "dashboard":
        if not st.session_state.user: navigate_to("home")
        render_dashboard()

if __name__ == "__main__": main()
