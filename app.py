"""
FIXED Frontend Application for HAVEN Crowdfunding Platform
This file contains the corrected Streamlit application that fixes:
1. OAuth integration with proper error handling
2. Environment variable usage
3. User interface improvements
4. Session management
"""

import streamlit as st
import os
import logging
from datetime import datetime
from oauth_integration import (
    render_oauth_buttons, 
    handle_oauth_callback, 
    check_authentication_status,
    get_user_info,
    logout,
    OAuthManager
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Haven - Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #4CAF50, #45a049);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .role-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    
    .oauth-section {
        background: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .status-card {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #4CAF50;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Handle OAuth callback first
    handle_oauth_callback()
    
    # Check authentication status
    if check_authentication_status():
        show_dashboard()
    else:
        show_login_page()

def show_login_page():
    """Display login page with OAuth options"""
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🏠 Welcome to Haven</h1>
        <h3>Empowering Communities Through Crowdfunding</h3>
        <p>Connect, Support, and Make a Difference</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if OAuth is enabled
    oauth_enabled = os.getenv("FEATURES_OAUTH_ENABLED", "false").lower() == "true"
    
    if not oauth_enabled:
        st.warning("⚠️ OAuth authentication is currently disabled. Please contact the administrator.")
        return
    
    # Role selection section
    st.markdown("## 👥 Choose Your Role")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="role-card">
            <h4>👤 Individual</h4>
            <ul>
                <li>🎯 Donate to campaigns</li>
                <li>❤️ Support causes you care about</li>
                <li>📊 Track donation history</li>
                <li>🧾 Get tax receipts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Register as Individual", key="individual_role", use_container_width=True, type="primary"):
            st.session_state.selected_role = "individual"
            st.experimental_rerun()
    
    with col2:
        st.markdown("""
        <div class="role-card">
            <h4>🏢 Organization</h4>
            <ul>
                <li>🚀 Create fundraising campaigns</li>
                <li>📈 Manage campaign updates</li>
                <li>💰 Track donations received</li>
                <li>🤝 Engage with donors</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Register as Organization", key="organization_role", use_container_width=True, type="primary"):
            st.session_state.selected_role = "organization"
            st.experimental_rerun()
    
    # Show OAuth buttons if role is selected
    if st.session_state.get("selected_role"):
        st.markdown("---")
        
        # OAuth section
        st.markdown("""
        <div class="oauth-section">
        """, unsafe_allow_html=True)
        
        selected_role = st.session_state.selected_role
        st.markdown(f"### 🔐 Login as {selected_role.title()}")
        
        # Display OAuth buttons
        render_oauth_buttons(selected_role)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Back button
        if st.button("⬅️ Back to Role Selection", key="back_to_roles"):
            if "selected_role" in st.session_state:
                del st.session_state.selected_role
            st.experimental_rerun()
    
    # Footer information
    st.markdown("---")
    st.markdown("""
    ### 🔒 Security & Privacy
    - Your data is encrypted and secure
    - We never store your social media passwords
    - OAuth authentication is handled by trusted providers
    - You can revoke access at any time
    """)
    
    # System status (for debugging)
    if st.checkbox("🔧 Show System Status"):
        show_system_status()

def show_dashboard():
    """Display main dashboard for authenticated users"""
    
    user_info = get_user_info()
    
    # Dashboard header
    st.markdown(f"""
    <div class="main-header">
        <h1>🏠 Haven Dashboard</h1>
        <p>Welcome back! You're logged in via {user_info['provider'].title()}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User info card
    st.markdown("""
    <div class="status-card">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔐 Authentication", user_info['provider'].title())
    
    with col2:
        st.metric("👤 User Type", user_info['user_type'].title())
    
    with col3:
        auth_time = datetime.fromtimestamp(user_info['auth_time'])
        st.metric("⏰ Login Time", auth_time.strftime("%H:%M:%S"))
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Main dashboard content
    st.markdown("## 🚀 What would you like to do?")
    
    if user_info['user_type'] == "individual":
        show_individual_dashboard()
    else:
        show_organization_dashboard()
    
    # Logout section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🚪 Logout", key="logout_btn", use_container_width=True, type="secondary"):
            logout()

def show_individual_dashboard():
    """Dashboard for individual users"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Discover Campaigns
        - Browse active fundraising campaigns
        - Filter by category and location
        - Read campaign stories and updates
        """)
        
        if st.button("🔍 Browse Campaigns", use_container_width=True):
            st.info("🚧 Campaign browsing feature coming soon!")
    
    with col2:
        st.markdown("""
        ### 📊 Your Activity
        - View your donation history
        - Track supported campaigns
        - Download tax receipts
        """)
        
        if st.button("📈 View Activity", use_container_width=True):
            st.info("🚧 Activity tracking feature coming soon!")

def show_organization_dashboard():
    """Dashboard for organization users"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚀 Create Campaign
        - Start a new fundraising campaign
        - Set goals and deadlines
        - Add compelling stories and media
        """)
        
        if st.button("➕ Create Campaign", use_container_width=True):
            st.info("🚧 Campaign creation feature coming soon!")
    
    with col2:
        st.markdown("""
        ### 📈 Manage Campaigns
        - View your active campaigns
        - Track donations and progress
        - Post updates to supporters
        """)
        
        if st.button("⚙️ Manage Campaigns", use_container_width=True):
            st.info("🚧 Campaign management feature coming soon!")

def show_system_status():
    """Display system status for debugging"""
    
    oauth_manager = OAuthManager()
    
    st.markdown("### 🔧 System Status")
    
    # Backend connection test
    backend_connected = oauth_manager.test_backend_connection()
    
    status_data = {
        "Backend Connection": "✅ Connected" if backend_connected else "❌ Disconnected",
        "Backend URL": oauth_manager.backend_url,
        "Frontend URL": oauth_manager.frontend_url,
        "OAuth Enabled": os.getenv("FEATURES_OAUTH_ENABLED", "false"),
        "Google Configured": "✅ Yes" if oauth_manager.google_client_id else "❌ No",
        "Facebook Configured": "✅ Yes" if oauth_manager.facebook_app_id else "❌ No",
        "Environment": os.getenv("ENVIRONMENT", "development")
    }
    
    for key, value in status_data.items():
        st.text(f"{key}: {value}")
    
    # OAuth configuration check
    if backend_connected:
        config_status = oauth_manager.check_oauth_config()
        st.json(config_status)
    
    # Session state
    if st.checkbox("Show Session State"):
        st.json(dict(st.session_state))

if __name__ == "__main__":
    main()

