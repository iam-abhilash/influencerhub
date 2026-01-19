import streamlit as st
import os
import requests
from supabase import create_client, Client

# Page Config
st.set_page_config(
    page_title="InfluencerHub | The Premium Creator Network",
    page_icon="✨",
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
ACCENT = "#FF6B6B"
BG_LIGHT = "#F8F9FD"

# Enhanced CSS for Modern Professional Look
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        
        .stApp {{
            background: linear-gradient(135deg, #FDFBFF 0%, #F4F7FF 100%);
            font-family: 'Outfit', sans-serif;
        }}

        /* Typography */
        h1, h2, h3 {{ 
            font-family: 'Outfit', sans-serif !important;
            color: {SECONDARY} !important;
            letter-spacing: -0.02em;
        }}

        /* Buttons Core */
        .stButton>button {{
            border-radius: 12px !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: none !important;
            padding: 0.6rem 1.5rem !important;
        }}

        /* Primary Buttons */
        div[data-testid="stButton"] button[key*="primary"] {{
            background: {PRIMARY} !important;
            color: white !important;
        }}
        
        div[data-testid="stButton"] button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(103, 76, 196, 0.2);
        }}

        /* Cards */
        .premium-card {{
            background: white;
            padding: 2.5rem;
            border-radius: 24px;
            border: 1px solid rgba(103, 76, 196, 0.1);
            box-shadow: 0 20px 40px rgba(0,0,0,0.03);
            transition: transform 0.3s ease;
        }}
        .premium-card:hover {{
            transform: translateY(-5px);
        }}

        /* Glassmorphism Auth Card */
        .auth-container {{
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            padding: 3rem;
            border-radius: 32px;
            border: 1px solid white;
            box-shadow: 0 30px 60px rgba(0,0,0,0.05);
            max-width: 500px;
            margin: 2rem auto;
        }}

        /* Navbar Header */
        .nav-text {{
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, {PRIMARY}, {SECONDARY});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

def render_navbar():
    cols = st.columns([2, 5, 2])
    with cols[0]:
        st.markdown(f'<p class="nav-text">InfluencerHub</p>', unsafe_allow_html=True)
    with cols[2]:
        if st.session_state.user:
            if st.button("Log Out", key="logout_btn"):
                supabase.auth.sign_out()
                st.session_state.user = None
                navigate_to("home")
        else:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Log In", key="nav_login"): navigate_to("login")
            with c2:
                if st.button("Join Now", key="nav_signup", type="primary"): navigate_to("signup")

def render_home():
    st.markdown('<div style="text-align: center; padding: 6rem 0;">', unsafe_allow_html=True)
    st.markdown(f'<h1 style="font-size: 4.5rem; margin-bottom: 1rem;">Scale Your Influence <span style="color: {PRIMARY}">Faster.</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.4rem; color: #64748b; margin-bottom: 3rem; max-width: 700px; margin-left: auto; margin-right: auto;">The elite operating system for world-class creators and brands. Automated campaigns, verified payments, and deep analytics.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started for Free", key="hero_cta", use_container_width=True, type="primary"):
            navigate_to("signup")
    st.markdown('</div>', unsafe_allow_html=True)

    # Trust Badges / Stats
    st.markdown("---")
    st.markdown('<div style="display: flex; justify-content: space-around; padding: 2rem 0; color: #94a3b8; text-align: center;"><div><h3>2.5k+</h3><p>Creators</p></div><div><h3>$1.2M+</h3><p>Paid</p></div><div><h3>500+</h3><p>Brands</p></div></div>', unsafe_allow_html=True)
    st.markdown("---")

def render_auth_form(mode="login"):
    st.markdown(f'<div class="auth-container">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="text-align: center; margin-bottom: 0.5rem;">{"Welcome Back" if mode=="login" else "Create Account"}</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; color: #64748b; margin-bottom: 2rem;">{"Log in to your dashboard" if mode=="login" else "Start your journey within seconds"}</p>', unsafe_allow_html=True)
    
    # Google SSO Button
    if st.button("Continue with Google", key="google_sso", use_container_width=True):
        try:
            # This triggers the Google OAuth flow via Supabase
            auth_response = supabase.auth.sign_in_with_oauth({
                "provider": "google",
                "options": {
                    "redirect_to": st.query_params.get("redirect_to", "https://frontend-production-4b9e.up.railway.app/")
                }
            })
            if auth_response and hasattr(auth_response, 'url'):
                st.markdown(f'<meta http-equiv="refresh" content="0; url={auth_response.url}">', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Google Login Error: {e}")

    st.markdown('<div style="text-align: center; margin: 1rem 0; color: #cbd5e1;">OR</div>', unsafe_allow_html=True)

    email = st.text_input("Email Address", placeholder="name@company.com")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    
    btn_label = "Log In" if mode == "login" else "Create Account"
    if st.button(btn_label, key="auth_submit", use_container_width=True, type="primary"):
        try:
            if mode == "login":
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                navigate_to("dashboard")
            else:
                res = supabase.auth.sign_up({"email": email, "password": password})
                st.success("Verification email sent! Check your inbox.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            
    st.markdown(f'<p style="text-align: center; margin-top: 1.5rem; color: #64748b;">{"Don\'t have an account?" if mode=="login" else "Already have an account?"} <a href="#" onclick="return false;" style="color: {PRIMARY}; font-weight: 600;">Contact Support</a></p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard():
    # Modern Sidebar Dashboard
    with st.sidebar:
        st.markdown(f"### 🟣 InfluencerHub")
        st.write(f"Logged in as: **{st.session_state.user.email}**")
        st.divider()
        st.button("Dashboard", use_container_width=True, type="primary")
        st.button("Campaigns", use_container_width=True)
        st.button("Wallet", use_container_width=True)
        st.button("Settings", use_container_width=True)

    st.header("Good Morning! 👋")
    
    # Summary Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Reach", "1.2M", "+12%")
    with m2: st.metric("Campaigns", "4", "0")
    with m3: st.metric("Earnings", "$4,250", "+$840")
    with m4: st.metric("Rating", "4.9/5", "+0.1")

    # System Link Status
    try:
        requests.get(f"{API_URL}/health", timeout=2)
        st.success("Core Systems Connected")
    except:
        st.info("Syncing with Global Node...")

def main():
    if not supabase:
        st.error("Missing SUPABASE_URL and SUPABASE_KEY in environment.")
        return

    # Check for OAuth Callback params in URL
    query_params = st.query_params
    if "access_token" in query_params or "code" in query_params:
        # Supabase handles tokens in the fragment/query, basic check
        st.session_state.user = supabase.auth.get_user()
        if st.session_state.user:
            navigate_to("dashboard")

    if st.session_state.page == "dashboard" and st.session_state.user:
        render_dashboard()
    else:
        render_navbar()
        if st.session_state.page == "home":
            render_home()
        elif st.session_state.page == "login":
            render_auth_form("login")
        elif st.session_state.page == "signup":
            render_auth_form("signup")

if __name__ == "__main__":
    main()
