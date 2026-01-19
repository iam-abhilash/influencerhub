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
        
        /* Hide default Streamlit bits */
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

        /* Buttons Fix - No Global 100% width */
        .stButton>button {{
            border-radius: 8px !important;
            font-weight: 600 !important;
            background: {PRIMARY} !important;
            color: white !important;
            border: none !important;
            padding: 0.6rem 2rem !important;
            min-height: 3.2rem !important;
            transition: all 0.2s ease !important;
        }}
        .stButton>button:hover {{
            background: #7C3AED !important;
            box-shadow: 0 4px 15px rgba(103, 76, 196, 0.4) !important;
            transform: translateY(-1px);
        }}

        .logo-text {{
            font-size: 2.2rem !important; 
            background: linear-gradient(90deg, #FFFFFF 0%, {ACCENT} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: -0.04em;
        }}

        /* Clean Card Design */
        .excellence-card {{
            background: rgba(15, 15, 15, 0.85);
            backdrop-filter: blur(25px);
            border-radius: 20px;
            padding: 2.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
        }}

        /* Input styling */
        .stTextInput input {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border-radius: 8px !important;
            border: none !important;
            height: 3rem !important;
        }}
        
        /* Auth Background */
        .auth-bg-overlay {{
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                        url('https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=2601&auto=format&fit=crop');
            background-size: cover;
            z-index: -1;
        }}
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

def render_navbar():
    with st.container():
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.markdown(f'<div style="padding-left: 10%;"><p class="logo-text">InfluencerHub</p></div>', unsafe_allow_html=True)
        with col3:
            if not st.session_state.user:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Login", key="btn_nav_l"): navigate_to("login")
                with c2:
                    if st.button("Sign Up", key="btn_nav_s"): navigate_to("signup")
            else:
                if st.button("Dashboard", key="btn_nav_d"): navigate_to("dashboard")

def render_home():
    # Hero Section
    st.markdown(f"""
        <div style="background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                    url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2672&auto=format&fit=crop');
                    background-size: cover; background-position: center; padding: 12rem 10% 8rem 10%; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <h1 style="font-size: 5.5rem; font-weight: 800; line-height: 1; margin-bottom: 2rem;">SCALE YOUR <br><span style="color: {ACCENT}">LEVEL</span></h1>
            <p style="font-size: 1.5rem; color: rgba(255,255,255,0.7); max-width: 800px; margin: 0 auto 3.5rem auto;">
                Boutique campaign management for elite creators. verify influence and access institutional payouts.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Content
    st.markdown('<div style="padding: 6rem 10%;">', unsafe_allow_html=True)
    c1, c2 = st.columns([1.2, 1], gap="large")
    with c1:
        st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=2426&auto=format&fit=crop", use_container_width=True)
    with c2:
        st.markdown('<div style="margin-top: 3rem;">', unsafe_allow_html=True)
        st.markdown('<h2 style="font-size: 3.5rem; margin-bottom: 1rem;">Global Performance</h2>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.3rem; opacity: 0.7; margin-bottom: 2.5rem;">The only dashboard that tracks sentiment and conversion velocity in real-time across the entire social stack.</p>', unsafe_allow_html=True)
        if st.button("Join Now", key="btn_home_cta"): navigate_to("signup")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_auth(mode="login"):
    st.markdown('<div class="auth-bg-overlay"></div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
        _, col, _ = st.columns([1, 1.2, 1])
        with col:
            st.markdown('<div class="excellence-card">', unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; margin-bottom: 0.5rem;'>{mode.capitalize()}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; opacity: 0.5; margin-bottom: 2rem;'>InfluencerHub Secure Portal</p>", unsafe_allow_html=True)
            
            email = st.text_input("Corporate ID", placeholder="name@company.com", key=f"auth_email_{mode}")
            password = st.text_input("Access Token", type="password", placeholder="••••••••", key=f"auth_pass_{mode}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if mode == "signup":
                if st.button("Establish Identity", use_container_width=True, key="btn_auth_s"):
                    try:
                        res = supabase.auth.sign_up({"email": email, "password": password})
                        st.success("✅ Handshake initiated. Check your inbox.")
                    except Exception as e: st.error(str(e))
            else:
                if st.button("Verify & Enter", use_container_width=True, key="btn_auth_l"):
                    try:
                        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = res.user
                        navigate_to("dashboard")
                    except: st.error("Authentication Denied.")
            
            st.markdown("<div style='text-align:center; padding: 1.5rem 0; opacity: 0.2;'>——</div>", unsafe_allow_html=True)
            if mode == "login":
                if st.button("No account? Sign up", use_container_width=True, key="btn_to_s"): navigate_to("signup")
            else:
                if st.button("Have an account? Login", use_container_width=True, key="btn_to_l"): navigate_to("login")
            st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard():
    st.markdown(f'<div style="padding: 5rem 10%; min-height: 100vh; background: {DARK_BG};">', unsafe_allow_html=True)
    st.markdown(f"<h1>Mission Control</h1><p style='opacity: 0.5;'>AUTHORIZED_ACCESS: {st.session_state.user.email}</p>", unsafe_allow_html=True)
    st.divider()
    
    c1, c2, c3 = st.columns(3)
    metrics = [("Total Flow", "$14,200", "+5%"), ("Network Reach", "2.1M", "↑"), ("Rep Score", "98", "Elite")]
    for i, col in enumerate([c1, c2, c3]):
        with col:
            st.markdown('<div class="excellence-card" style="text-align: center; padding: 2rem;">', unsafe_allow_html=True)
            st.metric(metrics[i][0], metrics[i][1], metrics[i][2])
            st.markdown('</div>', unsafe_allow_html=True)
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Logout", key="btn_logout"):
        supabase.auth.sign_out()
        st.session_state.user = None
        navigate_to("home")
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    if not supabase: 
        st.error("System Keys Missing")
        return

    if st.session_state.page == "home":
        render_navbar()
        render_home()
    elif st.session_state.page == "login":
        render_auth("login")
    elif st.session_state.page == "signup":
        render_auth("signup")
    elif st.session_state.page == "dashboard":
        if not st.session_state.user:
            navigate_to("home")
        render_dashboard()

if __name__ == "__main__":
    main()
