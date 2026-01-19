import streamlit as st
import os
import requests
from supabase import create_client, Client

# Page Config
st.set_page_config(
    page_title="InfluencerHub | The Global Standard for Creators",
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
        
        [data-testid="stHeader"] {{ display: none !important; }}
        .block-container {{ padding: 0 !important; max-width: 100% !important; }}
        
        .stApp {{
            background-color: {DARK_BG};
            color: #FFFFFF;
            font-family: 'Outfit', sans-serif;
        }}

        /* Hero Section Styling */
        .hero-bg {{
            background: linear-gradient(rgba(5,5,5,0.7), rgba(5,5,5,0.7)), 
                        url('https://images.unsplash.com/photo-1611162617474-5b21e879e113?q=80&w=2574&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            padding: 10rem 10%;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}

        .logo-text {{
            font-size: 3.5rem !important; 
            background: linear-gradient(90deg, #FFFFFF 0%, {ACCENT} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: -0.06em;
        }}

        .excellence-card {{
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 3rem;
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        .excellence-card:hover {{
            transform: translateY(-10px);
            border-color: {PRIMARY};
            background: rgba(255, 255, 255, 0.05);
        }}

        .stButton>button {{
            width: 100% !important;
            border-radius: 100px !important;
            font-weight: 700 !important;
            background: {PRIMARY} !important;
            color: white !important;
            border: none !important;
            height: 4rem !important;
            font-size: 1.2rem !important;
            transition: all 0.3s ease !important;
        }}
        
        /* Navigation Style */
        .nav-container {{
            padding: 1.5rem 10%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(5,5,5,0.8);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 1000;
        }}

        .stTextInput input {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border-radius: 15px !important;
            height: 3.5rem !important;
        }}
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.page = page_name

def render_navbar():
    cols = st.columns([4, 4, 3])
    with cols[0]:
        st.markdown('<p class="logo-text">InfluencerHub</p>', unsafe_allow_html=True)
    with cols[2]:
        if st.session_state.user:
            if st.button("Logout", key="nav_logout"):
                supabase.auth.sign_out()
                st.session_state.user = None
                navigate_to("home"); st.rerun()
        else:
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("Login", key="nav_login"): navigate_to("login"); st.rerun()
            with c2: 
                if st.button("Start Free", key="nav_signup"): navigate_to("signup"); st.rerun()

def render_home():
    # Hero Section
    st.markdown(f"""
        <div class="hero-bg">
            <h1 style="font-size: 6rem; font-weight: 800; line-height: 1; margin-bottom: 1rem;">ELITE OPERATING <br><span style="color: {ACCENT}">SYSTEM</span> FOR CREATORS.</h1>
            <p style="font-size: 1.6rem; color: rgba(255,255,255,0.7); max-width: 800px; margin: 0 auto 3rem auto;">
                Bridge the gap between influence and institutional income. Manage high-stakes campaigns with verified smart contracts and bank-grade analytics.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Values Section
    st.markdown('<div style="padding: 6rem 10%;">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; font-size: 3rem; margin-bottom: 4rem;">Built for Excellence</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown(f'<div class="excellence-card"><h1 style="font-size: 3.5rem;">🌎</h1><h3>Global Reach</h3><p style="color: rgba(255,255,255,0.6);">Connect with Tier-1 brands across North America, Europe, and Asia instantly.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="excellence-card"><h1 style="font-size: 3.5rem;">⛓️</h1><h3>Smart Identity</h3><p style="color: rgba(255,255,255,0.6);">Your metrics are on-chain verified. No more screenshots, no more manual reporting.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="excellence-card"><h1 style="font-size: 3.5rem;">💰</h1><h3>Instant Payouts</h3><p style="color: rgba(255,255,255,0.6);">Payments are escrowed. The moment you post, your funds are released.</p></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Immersive Feature Section
    col_img, col_txt = st.columns([1.2, 1], gap="large")
    with col_img:
        st.markdown('<div style="padding-left: 10%;">', unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=2426&auto=format&fit=crop", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_txt:
        st.markdown('<div style="padding-top: 5rem; padding-right: 15%;">', unsafe_allow_html=True)
        st.markdown('<h2 style="font-size: 3.5rem;">Institutional Analytics</h2>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.3rem; color: rgba(255,255,255,0.7);">Experience the power of real-time data ingestion. Track sentiment, engagement velocity, and conversion attribution in a single pane of glass.</p>', unsafe_allow_html=True)
        if st.button("Join the Ecosystem", key="feat_cta"):
            navigate_to("signup"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_auth(mode="login"):
    st.markdown('<div style="background-color: #000000; padding: 10rem 0; min-height: 100vh;">', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown(f'<div style="background: #111; padding: 4rem; border-radius: 40px; border: 1px solid rgba(255,255,255,0.05);">', unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; margin-bottom: 2rem;'>{'Welcome back' if mode=='login' else 'Create Identity'}</h1>", unsafe_allow_html=True)
        
        email = st.text_input("Corporate Email", placeholder="name@company.com", key=f"{mode}_email")
        password = st.text_input("Secret Key", type="password", placeholder="••••••••", key=f"{mode}_pass")
        
        if mode == "signup":
            if st.button("Establish Identity"):
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("Verification packet sent. Check your secure inbox.")
                except Exception as e: st.error(f"Handshake failed: {e}")
        else:
            if st.button("Access Mission Control"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = res.user
                    navigate_to("dashboard"); st.rerun()
                except: st.error("Access denied. Invalid credentials.")
        
        st.markdown("<br><p style='text-align:center; opacity: 0.3;'>———</p>", unsafe_allow_html=True)
        if mode == "login":
            if st.button("New to the network? Join here", key="go_s"): navigate_to("signup"); st.rerun()
        else:
            if st.button("Existing identifier? Login", key="go_l"): navigate_to("login"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard():
    # Modern Dashboard Layout
    st.markdown('<div style="padding: 4rem 10%;">', unsafe_allow_html=True)
    st.markdown(f"<h1>Mission Control <span style='font-size: 1.2rem; color: {ACCENT};'>v1.0.4</span></h1>", unsafe_allow_html=True)
    st.write(f"Authorized Participant: **{st.session_state.user.email}**")
    st.divider()
    
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Portfolio Value", "$24,580", "+12.4%")
    with m2: st.metric("Global Reach", "1.4M", "+3.1%")
    with m3: st.metric("Trust Score", "9.8/10", "+0.2")

    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    if st.button("Terminate Session", key="logout_dash"):
        supabase.auth.sign_out(); st.session_state.user = None; navigate_to("home"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    if not supabase: st.error("Core Infrustructure Missing")
    render_navbar()
    if st.session_state.user and st.session_state.page != "home": render_dashboard(); return
    if st.session_state.page == "home": render_home()
    elif st.session_state.page == "login": render_auth("login")
    elif st.session_state.page == "signup": render_auth("signup")

if __name__ == "__main__": main()
