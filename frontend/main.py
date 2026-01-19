import streamlit as st
import os
import requests
from supabase import create_client, Client

# Page Config
st.set_page_config(
    page_title="InfluencerHub - Your Creative Journey Starts Here",
    page_icon="🚀",
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

HOSTINGER_PURPLE = "#674CC4"
HOSTINGER_DARK = "#2F1C6A"

# Custom CSS for Hostinger Look & Feel
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;500;700&display=swap');
        .stApp {{
            background-color: #F4F5F7;
            font-family: 'DM Sans', sans-serif;
            color: #2F1C6A;
        }}
        h1, h2, h3 {{ color: #2F1C6A !important; font-weight: 700 !important; }}
        .stButton>button {{
            background-color: {HOSTINGER_PURPLE} !important;
            color: white !important;
            border-radius: 50px !important;
            padding: 0.5rem 2rem !important;
            border: none !important;
            font-weight: 700 !important;
            transition: all 0.3s ease !important;
        }}
        .stButton>button:hover {{
            background-color: {HOSTINGER_DARK} !important;
            transform: scale(1.02);
        }}
        .hero-title {{ font-size: 3.5rem; line-height: 1.2; text-align: center; margin-bottom: 1rem; }}
        .hero-subtitle {{ font-size: 1.5rem; color: #545778; text-align: center; margin-bottom: 2rem; }}
        .auth-card {{
            background-color: white;
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            max-width: 450px;
            margin: auto;
        }}
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

def render_navbar():
    col1, col2, col3 = st.columns([2, 5, 2])
    with col1:
        if st.button("🟣 **InfluencerHub**", key="nav_home_logo"):
            navigate_to("home")
    with col3:
        if st.session_state.user:
            if st.button("Log Out"):
                supabase.auth.sign_out()
                st.session_state.user = None
                navigate_to("home")
        else:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Log In"): navigate_to("login")
            with c2:
                if st.button("Sign Up"): navigate_to("signup")

def render_home():
    # Hero Section
    st.markdown('<div style="padding: 4rem 0;">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Turn Your Influence<br>Into Verified Income</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">The all-in-one platform for creators. Everything you need to manage campaigns, payments, and growth.</p>', unsafe_allow_html=True)
    
    col_cta1, col_cta2, col_cta3 = st.columns([1, 1, 1])
    with col_cta2:
       if st.button("Start Now", use_container_width=True):
           navigate_to("signup")
    st.markdown('</div>', unsafe_allow_html=True)

    # Features / Pricing Cards Style
    st.markdown("### Choose your path")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        with st.container(border=True):
            st.markdown("#### 🚀 Creator Starter")
            st.markdown(f"<h2 style='color: {HOSTINGER_PURPLE}'>Free</h2>", unsafe_allow_html=True)
            st.write("✔️ Basic Analytics")
            st.button("Select Starter", on_click=lambda: navigate_to("signup"), key="p1")
    with col_b:
         with st.container(border=True):
            st.markdown("#### ⭐ Premium Influencer")
            st.markdown(f"<h2 style='color: {HOSTINGER_PURPLE}'>$29.99/mo</h2>", unsafe_allow_html=True)
            st.write("✔️ Unlimited Campaigns")
            st.button("Select Premium", on_click=lambda: navigate_to("signup"), key="p2")
    with col_c:
         with st.container(border=True):
            st.markdown("#### 🏢 Brand Business")
            st.markdown(f"<h2 style='color: {HOSTINGER_PURPLE}'>$99.99/mo</h2>", unsafe_allow_html=True)
            st.write("✔️ Custom Contracts")
            st.button("Select Business", on_click=lambda: navigate_to("signup"), key="p3")

def render_login():
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.subheader("Welcome Back")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Log In", use_container_width=True):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state.user = res.user
            st.success("Logged in successfully!")
            navigate_to("dashboard")
        except Exception as e:
            st.error(f"Login failed: {str(e)}")
    st.markdown("---")
    st.write("Don't have an account?")
    if st.button("Sign Up here"): navigate_to("signup")
    st.markdown('</div>', unsafe_allow_html=True)

def render_signup():
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.subheader("Join InfluencerHub")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Create Account", use_container_width=True):
        try:
            res = supabase.auth.sign_up({"email": email, "password": password})
            st.success("Success! Please check your email to verify your account.")
            st.info("Once verified, you can log in.")
        except Exception as e:
            st.error(f"Signup failed: {str(e)}")
    st.markdown("---")
    st.write("Already have an account?")
    if st.button("Log In here"): navigate_to("login")
    st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard():
    st.header(f"Welcome, {st.session_state.user.email}!")
    st.write("You are now in your dashboard. Full creator statistics and campaign tools will appear here.")
    
    # Check backend healthy
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            st.success("✅ Backend Connection Secure")
        else:
            st.warning("⚠️ Backend connection issue, but your session is active.")
    except:
        st.warning("⚠️ Connecting to backend services...")

def main():
    if not supabase:
        st.error("⚠️ Supabase credentials missing. Please check your environment variables (SUPABASE_URL, SUPABASE_KEY).")
        return

    render_navbar()
    st.markdown("---")

    if st.session_state.page == "home":
        render_home()
    elif st.session_state.page == "login":
        render_login()
    elif st.session_state.page == "signup":
        render_signup()
    elif st.session_state.page == "dashboard":
        if not st.session_state.user:
            navigate_to("login")
        render_dashboard()

if __name__ == "__main__":
    main()
