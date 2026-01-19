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
        
        /* Remove top white space and streamlit header */
        [data-testid="stHeader"] {{
            display: none !important;
        }}
        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
        }}
        
        .stApp {{
            background-color: #0B0E14;
            color: #E2E8F0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}

        /* Logo Sizing - Massive & High Impact */
        .logo-text {{
            font-size: 3.5rem !important; 
            background: linear-gradient(135deg, #A78BFA 0%, #674CC4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: -0.05em;
            margin-bottom: 1rem;
            display: inline-block;
        }}

        /* Fix Inputs: Black text on white/light background as requested */
        .stTextInput input {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            padding: 12px !important;
            font-weight: 500 !important;
        }}
        .stTextInput label {{
            color: #8B949E !important;
            font-weight: 600 !important;
            margin-bottom: 8px !important;
        }}
        
        .stTextInput input:focus {{
            border-color: {PRIMARY} !important;
            box-shadow: 0 0 0 1px {PRIMARY} !important;
        }}

        /* Universal Button Styling (Force Purple) */
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
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(103, 76, 196, 0.4) !important;
            background: #7C3AED !important;
            color: white !important;
        }}

        /* Ghost Buttons for secondary actions */
        div[data-testid="stButton"] button[key*="secondary"] {{
            background: transparent !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
        }}
        
        /* Auth Container Sizing */
        .auth-box {{
            background: #161B22;
            border: 1px solid rgba(255,255,255,0.05);
            padding: 3rem;
            border-radius: 24px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.4);
            margin-top: 2rem;
        }}
        
        /* Hide decoration stripe */
        div[data-testid="stDecoration"] {{
            display: none !important;
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
            if st.button("Log Out", key="logout_btn_nav"):
                supabase.auth.sign_out()
                st.session_state.user = None
                navigate_to("home")
                st.rerun()
        elif st.session_state.page == "home":
             if st.button("Log In", key="login_btn_nav"):
                 navigate_to("login")
                 st.rerun()

def render_home():
    st.markdown('<div style="text-align: center; padding: 4rem 0;">', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 5rem; line-height: 1;">THE POWERHOUSE<br><span style="color: #A78BFA">FOR INFLUENCERS.</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.4rem; color: #94A3B8; margin: 2rem 0;">Automate campaigns, handle massive payments, and secure your brand.</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button("Start Your Journey", key="hero_signup_btn"):
            navigate_to("signup")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def render_auth(mode="login"):
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown(f'<div class="auth-box">', unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>{'Sign In' if mode=='login' else 'Create Account'}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #8B949E; margin-bottom: 2rem;'>The elite network for creators.</p>", unsafe_allow_html=True)
        
        email = st.text_input("Email Address", placeholder="name@email.com", key=f"{mode}_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key=f"{mode}_pass")
        
        if mode == "signup":
            if st.button("Register with Email", key="auth_signup_submit"):
                try:
                    # Explicitly using password login to avoid confusion
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("✅ Success! Please check your email inbox (and spam folder) for the verification link.")
                    st.info("Note: Free accounts have limited emails per hour. If it doesn't arrive, wait 5 mins or try a different email.")
                except Exception as e: 
                    st.error(f"Error: {str(e)}")
        else:
            if st.button("Log In to Dashboard", key="auth_login_submit"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = res.user
                    navigate_to("dashboard")
                    st.rerun()
                except Exception as e: 
                    st.error("Invalid credentials or unverified email. Check your link!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if mode == "login":
            if st.button("Don't have an account? Sign Up", key="goto_signup_secondary"):
                navigate_to("signup")
                st.rerun()
        else:
            if st.button("Already have an account? Log In", key="goto_login_secondary"):
                navigate_to("login")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard():
    st.markdown(f"# Welcome, Creator.")
    st.write(f"Identity: **{st.session_state.user.email}**")
    st.divider()
    if st.button("Logout Session", key="logout_dash_btn"):
        supabase.auth.sign_out()
        st.session_state.user = None
        navigate_to("home")
        st.rerun()

def main():
    if not supabase:
        st.error("Infrastructure Error: Missing configuration keys.")
        return

    render_navbar()
    
    if st.session_state.user and st.session_state.page != "home":
        render_dashboard()
        return

    if st.session_state.page == "home":
        render_home()
    elif st.session_state.page == "login":
        render_auth("login")
    elif st.session_state.page == "signup":
        render_auth("signup")

if __name__ == "__main__":
    main()
