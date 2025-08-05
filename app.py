"""
HAVEN Crowdfunding Platform - Main Streamlit Application
Fixed version with proper API integration, authentication, and no placeholder links
"""

import streamlit as st
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import utilities
from utils.config import config_manager
from utils.api_client import APIClient
from utils.auth_utils import AuthUtils

# Import pages
from pages.home import render_home_page
from pages.login import render_login_page, render_forgot_password_page, check_session_expiry, handle_oauth_callback
from pages.footer import render_footer, render_help_section, render_security_notice

# Page configuration
st.set_page_config(
    page_title="HAVEN - Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:support@haven.org',
        'Report a bug': 'mailto:support@haven.org',
        'About': "HAVEN - Empowering Communities Through Crowdfunding"
    }
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .sidebar-content {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #c8e6c9;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ddd;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .warning-message {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .footer-section {
        background-color: #f0f8f0;
        padding: 2rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid #c8e6c9;
    }
    
    .stButton > button {
        background-color: #4caf50;
        color: white;
        border: none;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #45a049;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    if 'api_client' not in st.session_state:
        backend_url = config_manager.get_backend_url()
        st.session_state.api_client = APIClient(backend_url)
    
    if 'auth_utils' not in st.session_state:
        st.session_state.auth_utils = AuthUtils(st.session_state.api_client)

def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        # Platform logo and title
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="color: #4caf50; margin: 0;">🏠 HAVEN</h1>
            <p style="color: #666; margin: 0; font-size: 0.9rem;">Crowdfunding Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu
        if st.session_state.authenticated:
            render_authenticated_sidebar()
        else:
            render_guest_sidebar()
        
        st.markdown("---")
        
        # Platform information
        render_platform_info()
        
        # Help section
        render_help_section()

def render_authenticated_sidebar():
    """Render sidebar for authenticated users"""
    user = st.session_state.get('user', {})
    
    # User info
    st.markdown(f"""
    <div class="sidebar-content">
        <h4>👤 Welcome, {user.get('full_name', 'User')}!</h4>
        <p style="color: #666; font-size: 0.9rem;">
            Role: {user.get('role', 'user').title()}<br>
            Email: {user.get('email', 'N/A')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main navigation
    if st.button("🏠 Home", key="nav_home", use_container_width=True):
        st.session_state.current_page = 'home'
        st.experimental_rerun()
    
    if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
        st.session_state.current_page = 'dashboard'
        st.experimental_rerun()
    
    if st.button("🎯 Campaigns", key="nav_campaigns", use_container_width=True):
        st.session_state.current_page = 'campaigns'
        st.experimental_rerun()
    
    if st.button("➕ Create Campaign", key="nav_create", use_container_width=True):
        st.session_state.current_page = 'create_campaign'
        st.experimental_rerun()
    
    if st.button("👤 Profile", key="nav_profile", use_container_width=True):
        st.session_state.current_page = 'profile'
        st.experimental_rerun()
    
    st.markdown("---")
    
    # Logout button
    if st.button("🚪 Logout", key="logout", use_container_width=True):
        st.session_state.auth_utils.logout_user()
        st.experimental_rerun()

def render_guest_sidebar():
    """Render sidebar for guest users"""
    # Welcome message
    st.markdown("""
    <div class="sidebar-content">
        <h4>👋 Welcome to HAVEN!</h4>
        <p style="color: #666; font-size: 0.9rem;">
            Join our community to create campaigns or support causes you care about.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    if st.button("🏠 Home", key="nav_home", use_container_width=True):
        st.session_state.current_page = 'home'
        st.experimental_rerun()
    
    if st.button("🎯 Browse Campaigns", key="nav_campaigns", use_container_width=True):
        st.session_state.current_page = 'campaigns'
        st.experimental_rerun()
    
    st.markdown("---")
    
    # Authentication buttons
    if st.button("🔐 Login", key="nav_login", use_container_width=True):
        st.session_state.current_page = 'login'
        st.experimental_rerun()
    
    if st.button("📝 Register", key="nav_register", use_container_width=True):
        st.session_state.current_page = 'register'
        st.experimental_rerun()

def render_platform_info():
    """Render platform information in sidebar"""
    st.markdown("### ℹ️ Platform Info")
    
    # Platform statistics (mock data)
    st.markdown("""
    <div class="metric-card">
        <strong>150+</strong><br>
        <small>Active Campaigns</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <strong>₹2.5M+</strong><br>
        <small>Total Raised</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <strong>1,200+</strong><br>
        <small>Community Members</small>
    </div>
    """, unsafe_allow_html=True)

def render_main_content():
    """Render the main content area"""
    current_page = st.session_state.current_page
    
    try:
        if current_page == 'home':
            render_home_page(st.session_state.api_client)
        
        elif current_page == 'login':
            render_login_page(st.session_state.api_client, st.session_state.auth_utils)
        
        elif current_page == 'forgot_password':
            render_forgot_password_page(st.session_state.api_client)
        
        elif current_page == 'register':
            render_register_page()
        
        elif current_page == 'dashboard':
            render_dashboard_page()
        
        elif current_page == 'campaigns':
            render_campaigns_page()
        
        elif current_page == 'create_campaign':
            render_create_campaign_page()
        
        elif current_page == 'profile':
            render_profile_page()
        
        else:
            st.error(f"Page '{current_page}' not found. Redirecting to home...")
            st.session_state.current_page = 'home'
            st.experimental_rerun()
    
    except Exception as e:
        logger.error(f"Error rendering page '{current_page}': {e}")
        st.error("An error occurred while loading the page. Please try again.")
        
        if st.button("🏠 Go to Home"):
            st.session_state.current_page = 'home'
            st.experimental_rerun()

def render_register_page():
    """Render registration page placeholder"""
    st.markdown("# 📝 Register for HAVEN")
    
    st.info("""
    🚧 **Registration page is under development**
    
    We're working hard to bring you a seamless registration experience with:
    - Email verification
    - KYC document upload
    - Profile customization
    - Security features
    
    **For now, please contact us directly:**
    - Email: support@haven.org
    - We'll create your account manually and send you login credentials
    """)
    
    if st.button("← Back to Login"):
        st.session_state.current_page = 'login'
        st.experimental_rerun()

def render_dashboard_page():
    """Render dashboard page placeholder"""
    st.markdown("# 📊 User Dashboard")
    
    st.info("""
    🚧 **Dashboard is under development**
    
    Your personalized dashboard will include:
    - Campaign management tools
    - Donation history
    - Analytics and insights
    - Quick actions
    - Notification center
    
    **Coming soon!**
    """)

def render_campaigns_page():
    """Render campaigns page placeholder"""
    st.markdown("# 🎯 Browse Campaigns")
    
    st.info("""
    🚧 **Campaign browsing is under development**
    
    The campaigns page will feature:
    - Advanced search and filtering
    - Category-based browsing
    - Featured campaigns
    - Campaign details and progress
    - Donation functionality
    
    **Coming soon!**
    """)

def render_create_campaign_page():
    """Render create campaign page placeholder"""
    st.markdown("# ➕ Create Campaign")
    
    st.info("""
    🚧 **Campaign creation is under development**
    
    The campaign creation wizard will include:
    - Step-by-step campaign setup
    - Media upload (images, videos)
    - Goal setting and timeline
    - Category selection
    - Preview and submission
    
    **For now, please contact us to create a campaign:**
    - Email: support@haven.org
    - We'll help you set up your campaign manually
    """)

def render_profile_page():
    """Render profile page placeholder"""
    st.markdown("# 👤 User Profile")
    
    st.info("""
    🚧 **Profile management is under development**
    
    Your profile page will include:
    - Personal information management
    - KYC document upload
    - Security settings
    - Notification preferences
    - Account statistics
    
    **Coming soon!**
    """)

def main():
    """Main application function"""
    try:
        # Initialize session state
        initialize_session_state()
        
        # Handle OAuth callback if present
        handle_oauth_callback()
        
        # Check session expiry for authenticated users
        if st.session_state.authenticated:
            check_session_expiry()
        
        # Render sidebar
        render_sidebar()
        
        # Render main content
        render_main_content()
        
        # Render footer
        render_footer()
        
        # Security notice
        render_security_notice()
        
    except Exception as e:
        logger.error(f"Critical error in main application: {e}")
        st.error("A critical error occurred. Please refresh the page.")
        
        # Emergency reset button
        if st.button("🔄 Reset Application"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()

if __name__ == "__main__":
    main()

