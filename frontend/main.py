import streamlit as st
import os
import requests
from supabase import create_client, Client

# Page Config
st.set_page_config(
    page_title="InfluencerHub | Sovereign",
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

# Theme Colors
PRIMARY = "#674CC4"
ACCENT = "#A78BFA"
DARK_BG = "#050505"

# Premium CSS
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

        /* Buttons Fix */
        div.stButton > button {{
            border-radius: 8px !important;
            font-weight: 600 !important;
            background-color: {PRIMARY} !important;
            color: white !important;
            border: none !important;
            padding: 0.8rem 2rem !important;
            min-height: 3.2rem !important;
            width: auto !important;
            display: block !important;
            margin: 0 auto !important;
            transition: 0.2s all ease;
        }}
        div.stButton > button:hover {{
            background-color: #7C3AED !important;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(103, 76, 196, 0.4);
        }}

        /* Glassmorphism Card Styling */
        div[data-testid="stVerticalBlock"] > div[style*="border"] {{
            background: rgba(15, 15, 15, 0.85) !important;
            backdrop-filter: blur(40px) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 24px !important;
            padding: 3.5rem !important;
        }}

        .logo-text {{
            font-size: 2.2rem !important; 
            background: linear-gradient(90deg, #FFFFFF 0%, {ACCENT} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }}

        /* Improved Full Screen Background Injection */
        .page-bg-fixed {{
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                              url('https://images.unsplash.com/photo-1497215728101-856f4ea42174?q=80&w=2670&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            z-index: -999;
        }}
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

def render_navbar():
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    col1, _, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown(f'<div style="padding-left: 10%;"><p class="logo-text">InfluencerHub</p></div>', unsafe_allow_html=True)
    with col3:
        if not st.session_state.user:
            inner_c1, inner_c2 = st.columns(2)
            with inner_c1:
                if st.button("Login", key="nav_l"): navigate_to("login")
            with inner_c2:
                if st.button("Sign Up", key="nav_s"): navigate_to("signup")

def render_home():
    # New Variation of Text: SOVEREIGN CREATOR COMMAND
    st.markdown(f"""
        <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2670&auto=format&fit=crop');
                    background-size: cover; background-position: center; padding: 15rem 10% 10rem 10%; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <h1 style="font-size: 5.5rem; font-weight: 900; line-height: 1; margin: 0; letter-spacing: -2px;">THE SOVEREIGN</h1>
            <h1 style="font-size: 5.5rem; font-weight: 900; line-height: 1; margin: 1rem 0 2.5rem 0; color: {ACCENT}; letter-spacing: -2px;">CREATOR COMMAND</h1>
            <p style="font-size: 1.6rem; color: rgba(255,255,255,0.7); max-width: 850px; margin: 0 auto 4.5rem auto; line-height: 1.5;">
                A high-performance ecosystem for the world's most influential voices. Verify your impact and automate institutional flow.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Access Mission Control", key="home_cta_sov"):
        navigate_to("signup")

    # Features
    st.markdown('<div style="padding: 7rem 10%;">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        with st.container(border=True):
            st.markdown("### 💠 Verified Flow")
            st.markdown("Automated smart contracts that release payments the millisecond your content hits its targets.")
    with c2:
        with st.container(border=True):
            st.markdown("### 📊 Real-time Ingest")
            st.markdown("Institutional-grade analytics tracking sentiment and reach velocity across the global social stack.")
    with c3:
        with st.container(border=True):
            st.markdown("### 🔐 Secure Identity")
            st.markdown("Your digital footprint is on-chain verified, protecting your worth from fraud and imitation.")
    st.markdown('</div>', unsafe_allow_html=True)

def render_auth(mode="login"):
    # Fix: Ensure background is injected correctly
    st.markdown('<div class="page-bg-fixed"></div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    
    with col:
        with st.container(border=True):
            st.markdown(f"<h1 style='text-align: center; font-size: 3rem; margin-bottom: 0.5rem;'>{mode.capitalize()}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; opacity: 0.5; margin-bottom: 3rem;'>Accessing Secure Central Infrastructure</p>", unsafe_allow_html=True)
            
            email = st.text_input("Identity ID", placeholder="email@example.com", key=f"id_{mode}", label_visibility="collapsed")
            password = st.text_input("Access Token", placeholder="Password", type="password", key=f"tok_{mode}", label_visibility="collapsed")
            
            st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
            if mode == "signup":
                if st.button("Establish Account", use_container_width=True):
                    try:
                        # Explicitly tell Supabase to redirect to the live site after email confirmation
                        res = supabase.auth.sign_up({
                            "email": email, 
                            "password": password,
                            "options": {
                                "email_redirect_to": "https://frontend-production-4b9e.up.railway.app"
                            }
                        })
                        st.success("✅ Handshake initiated. Check your inbox.")
                    except Exception as e: st.error(str(e))
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Existing Node? Login", use_container_width=True, key="to_login"): navigate_to("login")
            else:
                if st.button("Authorize Entry", use_container_width=True):
                    try:
                        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = res.user
                        navigate_to("dashboard")
                    except: st.error("Access Denied. Invalid Authorization.")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("New Participant? Sign Up", use_container_width=True, key="to_signup"): navigate_to("signup")

def render_dashboard():
    # Keep dashboard background dark and clean
    st.markdown(f'<div style="padding: 5rem 10%; background: {DARK_BG}; min-height: 100vh;">', unsafe_allow_html=True)
    st.markdown(f"<h1>Mission Control</h1><p style='opacity: 0.5;'>AUTHORIZED_SESSION: {st.session_state.user.email}</p>", unsafe_allow_html=True)
    st.divider()
    
    c1, c2, c3 = st.columns(3)
    for title, val in [("Campaigns", "0"), ("Earnings", "$0.00"), ("Status", "NOMINAL")]:
        with c1 if title == "Campaigns" else c2 if title == "Earnings" else c3:
            with st.container(border=True):
                st.metric(title, val)
                
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Terminate Session"):
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
        if not st.session_state.user: navigate_to("home")
        render_dashboard()

if __name__ == "__main__":
    main()
