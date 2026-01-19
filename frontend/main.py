import streamlit as st
import os
import requests
from supabase import create_client, Client

# Page Config
st.set_page_config(
    page_title="InfluencerHub | Elite Creator Network",
    page_icon="👑",
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

# Premium Color Palette
PRIMARY = "#674CC4" 
SECONDARY = "#2F1C6A"

# High-End CSS Injection
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
        
        [data-testid="stHeader"] {{ display: none !important; }}
        .block-container {{ padding-top: 1rem !important; }}
        
        .stApp {{
            background-color: #0B0E14;
            color: #E2E8F0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}

        .logo-text {{
            font-size: 3rem !important; 
            background: linear-gradient(135deg, #A78BFA 0%, #674CC4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: -0.05em;
            display: inline-block;
        }}

        .hero-card {{
            background: rgba(255, 255, 255, 0.03);
            border-radius: 32px;
            padding: 4rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 2rem;
            overflow: hidden;
            position: relative;
        }}

        .stButton>button {{
            width: 100% !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            background: {PRIMARY} !important;
            color: white !important;
            border: none !important;
            height: 3.5rem !important;
            transition: all 0.3s ease !important;
        }}
        .stButton>button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(103, 76, 196, 0.5) !important;
        }}

        .stTextInput input {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border-radius: 12px !important;
            padding: 12px !important;
        }}

        .feature-image {{
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            transition: transform 0.5s ease;
        }}
        .feature-image:hover {{
            transform: scale(1.02);
        }}
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.page = page_name

def render_navbar():
    cols = st.columns([3, 6, 2])
    with cols[0]:
        st.markdown('<p class="logo-text">InfluencerHub</p>', unsafe_allow_html=True)
    with cols[2]:
        if st.session_state.user:
            if st.button("Log Out", key="nav_logout"):
                supabase.auth.sign_out()
                st.session_state.user = None
                navigate_to("home")
                st.rerun()
        elif st.session_state.page == "home":
             if st.button("Log In", key="nav_login"):
                 navigate_to("login")
                 st.rerun()

def render_home():
    # Hero Section with Image
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown('<div style="padding: 4rem 0;">', unsafe_allow_html=True)
        st.markdown('<h1 style="font-size: 5rem; line-height: 1.1; margin-bottom: 1.5rem;">MONETIZE YOUR<br><span style="color: #A78BFA">CREATIVE EDGE.</span></h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.4rem; color: #94A3B8; margin-bottom: 3rem;">The all-in-one institutional engine for creators to manage massive campaigns, secure smart contracts, and track institutional-grade analytics.</p>', unsafe_allow_html=True)
        if st.button("Sign Up Now — It's Free", key="hero_cta"):
            navigate_to("signup")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.image("https://raw.githubusercontent.com/Abhibatch/InfluencerHub/main/creator_platform_hero.png", use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Feature Section with Dashboard Preview
    col_feat1, col_feat2 = st.columns([1, 1], gap="large")
    with col_feat1:
        st.image("https://raw.githubusercontent.com/Abhibatch/InfluencerHub/main/analytics_dashboard_preview.png", use_container_width=True)
    
    with col_feat2:
        st.markdown('<div style="padding: 4rem 0;">', unsafe_allow_html=True)
        st.markdown('## Institutional Analytics')
        st.markdown('<p style="font-size: 1.2rem; color: #94A3B8;">Stop guessing. Start growing with metrics that matter. Our AI-driven dashboard gives you the same tools used by billion-dollar brands.</p>', unsafe_allow_html=True)
        st.markdown('✔️ Real-time Reach Tracking<br>✔️ Audience Sentiment Analysis<br>✔️ Predictive Earnings Engine', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_auth(mode="login"):
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown(f'<div style="background: #161B22; padding: 3rem; border-radius: 24px; border: 1px solid rgba(255,255,255,0.05); margin-top: 4rem;">', unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>{'Welcome Back' if mode=='login' else 'Create Account'}</h2>", unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="name@email.com", key=f"{mode}_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key=f"{mode}_pass")
        
        if mode == "signup":
            if st.button("Get Started with Email"):
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("✅ Success! Please check your email (and spam) for the link.")
                except Exception as e: st.error(str(e))
        else:
            if st.button("Secure Login"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = res.user
                    navigate_to("dashboard")
                    st.rerun()
                except: st.error("Login failed. Check your credentials.")
        
        st.markdown("<br><p style='text-align:center;'>---</p>", unsafe_allow_html=True)
        if mode == "login":
            if st.button("No account? Sign up", key="go_signup"): navigate_to("signup"); st.rerun()
        else:
            if st.button("Have an account? Log in", key="go_login"): navigate_to("login"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard():
    st.markdown(f"# Mission Control")
    st.write(f"Identity: **{st.session_state.user.email}**")
    st.divider()
    if st.button("Logout Dashboard", key="logout_dash"):
        supabase.auth.sign_out(); st.session_state.user = None; navigate_to("home"); st.rerun()

def main():
    if not supabase: st.error("Infrustructure Keys Missing")
    render_navbar()
    if st.session_state.user and st.session_state.page != "home": render_dashboard(); return
    if st.session_state.page == "home": render_home()
    elif st.session_state.page == "login": render_auth("login")
    elif st.session_state.page == "signup": render_auth("signup")

if __name__ == "__main__": main()
