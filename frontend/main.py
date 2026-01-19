import streamlit as st
import os
import requests
from supabase import create_client, Client

# Page Config
st.set_page_config(
    page_title="InfluencerHub | Premium Creator Ecosystem",
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
PRIMARY = "#674CC4" # Hostinger Purple
SECONDARY = "#2F1C6A" # Deep Indigo
ACCENT = "#6366f1"
BG_MAIN = "#0F172A" # Dark mode background

# Modern CSS Injection
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        .stApp {{
            background-color: #0B0E14;
            color: #E2E8F0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}

        /* Typography */
        h1, h2, h3, h4 {{ 
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            letter-spacing: -0.04em !important;
        }}

        /* High-Impact Logo Font */
        .logo-text {{
            font-size: 2.8rem !important; /* SIGNIFICANTLY LARGER */
            background: linear-gradient(135deg, #A78BFA 0%, #674CC4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            margin: 0;
            padding: 0;
            display: inline-block;
        }}

        /* Buttons */
        .stButton>button {{
            border-radius: 14px !important;
            font-weight: 700 !important;
            padding: 0.8rem 2.2rem !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            background: rgba(255,255,255,0.05) !important;
            color: white !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }}
        
        /* Action Button */
        div[data-testid="stButton"] button[key*="primary"] {{
            background: {PRIMARY} !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(103, 76, 196, 0.4);
        }}

        .stButton>button:hover {{
            transform: scale(1.05);
            background: {PRIMARY} !important;
            box-shadow: 0 10px 25px rgba(103, 76, 196, 0.5) !important;
        }}

        /* Premium Cards */
        .card-box {{
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(12px);
            border-radius: 28px;
            padding: 3rem;
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: border 0.3s ease;
        }}
        .card-box:hover {{
            border-color: {PRIMARY};
        }}

        /* Custom Section Wrappers */
        .hero-container {{
            padding: 8rem 0 4rem 0;
            text-align: center;
        }}
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

def render_navbar():
    cols = st.columns([4, 4, 3])
    with cols[0]:
        # Branding Header
        st.markdown('<p class="logo-text">InfluencerHub</p>', unsafe_allow_html=True)
    
    with cols[2]:
        if st.session_state.user:
            if st.button("Log Out", key="logout_btn", use_container_width=True):
                supabase.auth.sign_out()
                st.session_state.user = None
                navigate_to("home")
        else:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Log In", key="nav_login_btn", use_container_width=True): navigate_to("login")
            with c2:
                if st.button("Join Now", key="nav_join_primary", type="primary", use_container_width=True): navigate_to("signup")

def render_home():
    # Massive Hero Section
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 5.5rem; line-height: 0.9; margin-bottom: 2rem;">EVERYTHING ENGINES<br><span style="color: #A78BFA">FOR CREATORS.</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.6rem; color: #94A3B8; max-width: 800px; margin: 0 auto 3rem auto; line-height: 1.5;">The professional-grade platform to manage campaigns, verify payments, and scale your brand identity with institutional security.</p>', unsafe_allow_html=True)
    
    col_c1, col_c2, col_c3 = st.columns([1.2, 1, 1.2])
    with col_c2:
        if st.button("Start Building Now", key="hero_start_primary", type="primary", use_container_width=True):
            navigate_to("signup")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # Feature Grid
    st.markdown('<div style="margin-top: 4rem;">', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    features = [
        ("🚀", "Hyper-Growth", "Tools designed to double your creator reach."),
        ("💎", "Verified Contracts", "Smart agreements that guarantee your payment."),
        ("🛡️", "Institutional Safety", "Bank-grade security for your data and earnings.")
    ]
    for i, col in enumerate([f1, f2, f3]):
        with col:
            st.markdown(f"""
            <div class="card-box" style="text-align: center;">
                <h1 style="font-size: 3rem;">{features[i][0]}</h1>
                <h3>{features[i][1]}</h3>
                <p style="color: #94A3B8;">{features[i][2]}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_auth(mode="login"):
    st.markdown('<div style="max-width: 500px; margin: 4rem auto;">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align: center;'>{'Login' if mode=='login' else 'Create Account'}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #94A3B8;'>Enterprise-grade access</p>", unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        if mode == "signup":
            if st.button("Register with Email", key="auth_reg_primary", type="primary", use_container_width=True):
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("Verification link sent! Check your inbox.")
                except Exception as e: st.error(str(e))
        else:
            if st.button("Enter Dashboard", key="auth_login_primary", type="primary", use_container_width=True):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = res.user
                    navigate_to("dashboard")
                except Exception as e: st.error("Invalid credentials. Try again.")
        
        st.markdown("---")
        if mode == "login":
            if st.button("Need an account? Sign Up"): navigate_to("signup")
        else:
            if st.button("Have an account? Log In"): navigate_to("login")
    st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard():
    # High-End Content Dashboard
    with st.sidebar:
        st.markdown("# 👑")
        st.markdown(f"**Identity**<br>{st.session_state.user.email}", unsafe_allow_html=True)
        st.divider()
        if st.button("Exit Session", key="side_logout"):
            supabase.auth.sign_out()
            st.session_state.user = None
            navigate_to("home")

    st.markdown("# Mission Control")
    cols = st.columns(3)
    metric_data = [("Net Value", "$12,450", "+4.2%"), ("Active Deals", "8", "0"), ("Reach Index", "94.2", "+1.1%")]
    for i, col in enumerate(cols):
        with col:
            with st.container(border=True):
                st.metric(metric_data[i][0], metric_data[i][1], metric_data[i][2])
    
    st.markdown("---")
    st.subheader("Active Tasks")
    st.info("No active campaigns yet. Connect your social accounts to start.")

def main():
    if not supabase:
        st.error("Infrastructure Error: Missing configuration keys.")
        return

    # Check for authenticated session (for page refresh/persistence)
    if not st.session_state.user:
        try:
            user_res = supabase.auth.get_user()
            if user_res and user_res.user:
                st.session_state.user = user_res.user
        except: pass

    if st.session_state.user and st.session_state.page != "home":
        render_dashboard()
        return

    render_navbar()
    if st.session_state.page == "home":
        render_home()
    elif st.session_state.page == "login":
        render_auth("login")
    elif st.session_state.page == "signup":
        render_auth("signup")

if __name__ == "__main__":
    main()
