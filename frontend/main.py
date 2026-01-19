import streamlit as st
import os
import requests
from supabase import create_client, Client

# Page Config
st.set_page_config(
    page_title="InfluencerHub | Elite",
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

        /* Buttons Fix - Professional Sizing */
        div.stButton > button {{
            border-radius: 8px !important;
            font-weight: 600 !important;
            background-color: {PRIMARY} !important;
            color: white !important;
            border: none !important;
            padding: 0.6rem 1.5rem !important;
            min-height: 2.8rem !important;
            width: auto !important;
            display: inline-block !important;
            transition: 0.2s all ease;
        }}
        div.stButton > button:hover {{
            background-color: #7C3AED !important;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(103, 76, 196, 0.4);
        }}

        /* Navbar Gap Fix - Flexbox approach */
        .nav-container {{
            padding: 1.5rem 10%;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .nav-buttons {{
            display: flex;
            gap: 1rem;
            align-items: center;
        }}

        /* Glassmorphism Card Styling */
        div[data-testid="stVerticalBlock"] > div[style*="border"] {{
            background: rgba(15, 15, 15, 0.9) !important;
            backdrop-filter: blur(30px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 20px !important;
            padding: 3rem !important;
        }}

        .logo-text {{
            font-size: 2.2rem !important; 
            background: linear-gradient(90deg, #FFFFFF 0%, {ACCENT} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }}

        /* Fixed Background for Auth Pages */
        .auth-bg-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                        url('https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=2601&auto=format&fit=crop');
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
    # Use columns but keep them tight
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    col_logo, col_empty, col_btns = st.columns([4, 4, 3])
    with col_logo:
        st.markdown(f'<div style="padding-left: 10%;"><p class="logo-text">InfluencerHub</p></div>', unsafe_allow_html=True)
    with col_btns:
        if not st.session_state.user:
            # Side by side with tight gap
            c1, c2 = st.columns([1, 1], gap="small")
            with c1:
                if st.button("Login", key="nav_l"): navigate_to("login")
            with c2:
                if st.button("Sign Up", key="nav_s"): navigate_to("signup")
        else:
            if st.button("Dashboard", key="nav_d"): navigate_to("dashboard")

def render_home():
    # Restore: ELITE OPERATING SYSTEM
    st.markdown(f"""
        <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2672&auto=format&fit=crop');
                    background-size: cover; background-position: center; padding: 14rem 10% 8rem 10%; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <h1 style="font-size: 5.5rem; font-weight: 800; line-height: 1.1; margin: 0;">ELITE OPERATING</h1>
            <h1 style="font-size: 5.5rem; font-weight: 800; line-height: 1.1; margin: 0.5rem 0 2rem 0; color: {ACCENT};">SYSTEM</h1>
            <p style="font-size: 1.5rem; color: rgba(255,255,255,0.7); max-width: 800px; margin: 0 auto 3.5rem auto;">
                Bridge the gap between influence and institutional income. Manage high-stakes campaigns with verified smart contracts and bank-grade analytics.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Restore "Start Now" button text
    _, col_cta, _ = st.columns([2, 1, 2])
    with col_cta:
        if st.button("Start Now — It's Free", key="home_cta_restored"):
            navigate_to("signup")

    # Features Section
    st.markdown('<div style="padding: 6rem 10%;">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        with st.container(border=True):
            st.markdown("### 🌎 Global Reach")
            st.markdown("Connect with Tier-1 brands across North America, Europe, and Asia instantly.")
    with c2:
        with st.container(border=True):
            st.markdown("### ⛓️ Smart Identity")
            st.markdown("Your metrics are on-chain verified. No more screenshots, no more manual reporting.")
    with c3:
        with st.container(border=True):
            st.markdown("### 💰 Instant Payouts")
            st.markdown("Payments are escrowed. The moment you post, your funds are released.")
    st.markdown('</div>', unsafe_allow_html=True)

def render_auth(mode="login"):
    # Fix: Ensure background is visible
    st.markdown('<div class="auth-bg-overlay"></div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    
    with col:
        with st.container(border=True):
            st.markdown(f"<h1 style='text-align: center; margin-bottom: 0.5rem;'>{mode.capitalize()}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; opacity: 0.5; margin-bottom: 2.5rem;'>Secure Access Portal</p>", unsafe_allow_html=True)
            
            email = st.text_input("Identity ID", placeholder="email@example.com", key=f"id_{mode}", label_visibility="collapsed")
            password = st.text_input("Access Token", placeholder="Password", type="password", key=f"tok_{mode}", label_visibility="collapsed")
            
            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
            if mode == "signup":
                if st.button("Create Account", use_container_width=True):
                    try:
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
                if st.button("Return to Login", use_container_width=True, key="to_login"): navigate_to("login")
            else:
                if st.button("Secure Login", use_container_width=True):
                    try:
                        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = res.user
                        navigate_to("dashboard")
                    except: st.error("Access Denied. Invalid Authorization.")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("New to Hub? Sign Up", use_container_width=True, key="to_signup"): navigate_to("signup")

def render_dashboard():
    st.markdown(f'<div style="padding: 5rem 10%; background: {DARK_BG}; min-height: 100vh;">', unsafe_allow_html=True)
    st.markdown(f"<h1>Mission Control</h1><p style='opacity: 0.5;'>AUTHORIZED: {st.session_state.user.email}</p>", unsafe_allow_html=True)
    st.divider()
    
    c1, c2, c3 = st.columns(3)
    metrics = [("Campaigns", "0"), ("Earnings", "$0.00"), ("Status", "Active")]
    for i, col in enumerate([c1, c2, c3]):
        with col:
            with st.container(border=True):
                st.metric(metrics[i][0], metrics[i][1])
                
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Terminate Session"):
        supabase.auth.sign_out()
        st.session_state.user = None
        navigate_to("home")
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    if not supabase: return

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
