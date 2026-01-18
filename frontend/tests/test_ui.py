import re
from playwright.sync_api import Page, expect

def test_homepage_loads(page: Page):
    # Depending on how the frontend is served in CI, this URL might change
    # e.g. http://localhost:8501
    page.goto("http://localhost:8501")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("InfluencerHub"))

    # Check for main header
    header = page.get_by_text("InfluencerHub 🚀")
    expect(header).to_be_visible()

def test_navigation_sidebar(page: Page):
    page.goto("http://localhost:8501")
    
    # Click on 'Campaigns' in sidebar
    # Note: Streamlit radio buttons can be tricky to target by exact text depending on DOM
    # This is a generic example
    page.get_by_label("Go to").click() 
    # In real Streamlit, you might target specific elements based on tested DOM structure
