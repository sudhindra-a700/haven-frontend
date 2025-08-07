"""
HAVEN Crowdfunding Platform - Clean Authentication-First Frontend
Streamlit application with hidden navigation until after login
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime

# Import enhanced authentication and registration modules
from modules.workflow_auth_utils import (
    initialize_auth, is_authenticated, login_user, logout_user,
    is_individual, is_organization, can_donate, can_create_campaigns,
    needs_registration, get_user_role_display, get_allowed_features
)
from modules.workflow_registration_pages import show_registration_workflow

# ===== CONFIGURATION =====
st.set_page_config(
    page_title="HAVEN - Crowdfunding Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start with sidebar collapsed
)

# ===== CUSTOM CSS =====
def load_custom_css():
    """Load custom CSS for clean authentication-first design"""
    st.markdown("""
    <style>
    /* Hide sidebar completely for unauthenticated users */
    .css-1d391kg {
        display: none;
    }
    
    /* Hide sidebar toggle button for unauthenticated users */
    .css-1rs6os {
        display: none;
    }
    
    /* Main container styling */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Authentication landing page */
    .auth-landing {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .auth-landing h1 {
        font-size: 3rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    .auth-landing p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    /* Authentication cards */
    .auth-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid #e0e0e0;
    }
    
    .auth-card h3 {
        color: #333;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Role selection cards */
    .role-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
    }
    
    .role-card:hover {
        border-color: #4CAF50;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .role-card.individual {
        border-color: #2196F3;
    }
    
    .role-card.organization {
        border-color: #4CAF50;
    }
    
    .role-card h4 {
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .role-card.individual h4 {
        color: #2196F3;
    }
    
    .role-card.organization h4 {
        color: #4CAF50;
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 10px;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Social login buttons */
    .social-login {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin: 1rem 0;
    }
    
    .social-btn {
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        background: white;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: bold;
    }
    
    .social-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .social-btn.google {
        border-color: #db4437;
        color: #db4437;
    }
    
    .social-btn.facebook {
        border-color: #3b5998;
        color: #3b5998;
    }
    
    /* Dashboard styling */
    .dashboard-header {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .role-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        margin-top: 0.5rem;
    }
    
    .individual-badge {
        background: #2196F3;
        color: white;
    }
    
    .organization-badge {
        background: #4CAF50;
        color: white;
    }
    
    .admin-badge {
        background: #FF9800;
        color: white;
    }
    
    /* Navigation styling for authenticated users */
    .nav-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .nav-buttons {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .nav-btn {
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        background: white;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: bold;
        text-decoration: none;
        color: #333;
    }
    
    .nav-btn:hover {
        border-color: #4CAF50;
        background: #f8f9fa;
        transform: translateY(-1px);
    }
    
    .nav-btn.active {
        background: #4CAF50;
        color: white;
        border-color: #4CAF50;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .auth-landing h1 {
            font-size: 2rem;
        }
        
        .nav-buttons {
            flex-direction: column;
        }
        
        .social-login {
            flex-direction: column;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ===== AUTHENTICATION FUNCTIONS =====
def render_authentication_landing():
    """Render clean authentication landing page"""
    st.markdown("""
    <div class="auth-landing">
        <h1>🎯 Welcome to HAVEN</h1>
        <p>Empowering Communities Through Transparent Crowdfunding</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for login and register
    col1, col2 = st.columns(2)
    
    with col1:
        render_login_card()
    
    with col2:
        render_register_card()

def render_login_card():
    """Render login card"""
    st.markdown("""
    <div class="auth-card">
        <h3>🔐 Login to Your Account</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email Address", placeholder="your.email@example.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Your password", key="login_password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_submitted = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
        
        if login_submitted:
            if email and password:
                with st.spinner("Logging in..."):
                    success, message = login_user("email", {"email": email, "password": password})
                
                if success:
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
            else:
                st.error("❌ Please enter both email and password")
    
    # Social login section
    st.markdown("---")
    
    # Import OAuth integration
    from modules.oauth_integration import render_oauth_buttons
    render_oauth_buttons("individual")

def render_register_card():
    """Render registration card"""
    st.markdown("""
    <div class="auth-card">
        <h3>📝 Create New Account</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Choose Your Role")
    
    # Role selection
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👤 Register as Individual", use_container_width=True, type="secondary", key="register_individual"):
            st.session_state.show_registration = True
            st.session_state.registration_type = "individual"
            st.rerun()
        
        st.markdown("""
        <small>
        <strong>Individual:</strong><br>
        • Donate to campaigns<br>
        • Support causes you care about<br>
        • Track donation history<br>
        • Get tax receipts
        </small>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🏢 Register as Organization", use_container_width=True, type="secondary", key="register_organization"):
            st.session_state.show_registration = True
            st.session_state.registration_type = "organization"
            st.rerun()
        
        st.markdown("""
        <small>
        <strong>Organization:</strong><br>
        • Create fundraising campaigns<br>
        • Manage campaign updates<br>
        • Track donations received<br>
        • Engage with donors
        </small>
        """, unsafe_allow_html=True)

# ===== AUTHENTICATED USER INTERFACE =====
def render_authenticated_interface():
    """Render interface for authenticated users"""
    # Show role-based navigation
    render_role_based_navigation()
    
    # Show current page content
    current_page = st.session_state.get('current_page', 'dashboard')
    
    if current_page == 'dashboard':
        render_dashboard()
    elif current_page == 'campaigns':
        render_campaigns_page()
    elif current_page == 'donations':
        render_donations_page()
    elif current_page == 'create_campaign':
        render_create_campaign_page()
    elif current_page == 'my_campaigns':
        render_my_campaigns_page()
    elif current_page == 'profile':
        render_profile_page()
    else:
        render_dashboard()

def render_role_based_navigation():
    """Render navigation based on user role"""
    # User info header
    role_display = get_user_role_display()
    
    if is_individual():
        badge_class = "individual-badge"
        welcome_msg = f"Welcome back, {role_display}!"
    elif is_organization():
        badge_class = "organization-badge"
        welcome_msg = f"Welcome back, {role_display}!"
    else:
        badge_class = "admin-badge"
        welcome_msg = f"Welcome back, {role_display}!"
    
    st.markdown(f"""
    <div class="dashboard-header">
        <h2>{welcome_msg}</h2>
        <span class="role-badge {badge_class}">{role_display}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    # Get allowed features
    features = get_allowed_features()
    current_page = st.session_state.get('current_page', 'dashboard')
    
    # Create navigation buttons
    nav_cols = st.columns(6)
    
    with nav_cols[0]:
        if st.button("🏠 Dashboard", use_container_width=True, 
                    type="primary" if current_page == 'dashboard' else "secondary"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with nav_cols[1]:
        if st.button("👀 Browse Campaigns", use_container_width=True,
                    type="primary" if current_page == 'campaigns' else "secondary"):
            st.session_state.current_page = 'campaigns'
            st.rerun()
    
    # Role-specific navigation
    if features.get('donate', False):
        with nav_cols[2]:
            if st.button("❤️ My Donations", use_container_width=True,
                        type="primary" if current_page == 'donations' else "secondary"):
                st.session_state.current_page = 'donations'
                st.rerun()
    
    if features.get('create_campaigns', False):
        with nav_cols[2]:
            if st.button("➕ Create Campaign", use_container_width=True,
                        type="primary" if current_page == 'create_campaign' else "secondary"):
                st.session_state.current_page = 'create_campaign'
                st.rerun()
        
        with nav_cols[3]:
            if st.button("📊 My Campaigns", use_container_width=True,
                        type="primary" if current_page == 'my_campaigns' else "secondary"):
                st.session_state.current_page = 'my_campaigns'
                st.rerun()
    
    with nav_cols[4]:
        if st.button("👤 Profile", use_container_width=True,
                    type="primary" if current_page == 'profile' else "secondary"):
            st.session_state.current_page = 'profile'
            st.rerun()
    
    with nav_cols[5]:
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout_user()
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard():
    """Render role-based dashboard"""
    if is_individual():
        st.markdown("### 👤 Individual Dashboard")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            #### 💝 Your Impact
            - Browse active campaigns
            - Make secure donations
            - Track your contribution history
            - Download tax receipts
            """)
            
            if st.button("🔍 Browse Campaigns", use_container_width=True, type="primary"):
                st.session_state.current_page = 'campaigns'
                st.rerun()
        
        with col2:
            st.markdown("""
            #### 📊 Quick Stats
            - Total donations: Coming soon
            - Campaigns supported: Coming soon
            - Impact created: Coming soon
            """)
            
            if st.button("📈 View My Donations", use_container_width=True):
                st.session_state.current_page = 'donations'
                st.rerun()
    
    elif is_organization():
        st.markdown("### 🏢 Organization Dashboard")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            #### 🎯 Campaign Management
            - Create new fundraising campaigns
            - Manage active campaigns
            - Post updates to donors
            - Track donation progress
            """)
            
            if st.button("➕ Create New Campaign", use_container_width=True, type="primary"):
                st.session_state.current_page = 'create_campaign'
                st.rerun()
        
        with col2:
            st.markdown("""
            #### 📊 Performance Overview
            - Active campaigns: Coming soon
            - Total raised: Coming soon
            - Donor engagement: Coming soon
            """)
            
            if st.button("📊 Manage Campaigns", use_container_width=True):
                st.session_state.current_page = 'my_campaigns'
                st.rerun()
    
    else:
        st.markdown("### 🛡️ Admin Dashboard")
        st.info("Admin features coming soon!")

def render_campaigns_page():
    """Render campaigns listing page"""
    st.markdown("### 🎯 Browse Active Campaigns")
    
    if is_individual():
        st.info("💡 As an individual, you can donate to any active campaign!")
    elif is_organization():
        st.info("💡 As an organization, you can view campaigns for inspiration!")
    
    st.markdown("#### Featured Campaigns")
    st.info("📋 Campaign listing functionality will be implemented here.")

def render_donations_page():
    """Render donations page for individuals"""
    if not can_donate():
        st.error("🚫 Access denied. Only individuals can view donation history.")
        return
    
    st.markdown("### ❤️ My Donation History")
    st.info("📊 Your donation history will be displayed here.")

def render_create_campaign_page():
    """Render campaign creation page for organizations"""
    if not can_create_campaigns():
        st.error("🚫 Access denied. Only organizations can create campaigns.")
        return
    
    st.markdown("### ➕ Create New Campaign")
    st.info("📝 Campaign creation form will be implemented here.")

def render_my_campaigns_page():
    """Render campaign management page for organizations"""
    if not can_create_campaigns():
        st.error("🚫 Access denied. Only organizations can manage campaigns.")
        return
    
    st.markdown("### 📊 My Campaigns")
    st.info("📈 Your campaign management interface will be implemented here.")

def render_profile_page():
    """Render profile page"""
    st.markdown("### 👤 Profile Settings")
    st.info("⚙️ Profile management will be implemented here.")

# ===== MAIN APPLICATION =====
def main():
    """Main application function with clean authentication flow"""
    # Load custom CSS
    load_custom_css()
    
    # Initialize authentication
    initialize_auth()
    
    # Check for OAuth callback first
    from modules.oauth_integration import check_oauth_callback
    if check_oauth_callback():
        st.rerun()
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    
    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False
    
    # Check if user wants to register
    if st.session_state.show_registration:
        show_registration_workflow()
        
        # Back to main button
        if st.button("← Back to Login", key="back_to_login"):
            st.session_state.show_registration = False
            st.session_state.registration_type = None
            st.rerun()
        return
    
    # Check authentication status
    if not is_authenticated():
        # Show clean authentication landing page (NO SIDEBAR)
        render_authentication_landing()
        return
    
    # Check if user needs to complete registration
    if needs_registration():
        st.warning("📋 Please complete your registration to access all features.")
        if st.button("Complete Registration", type="primary"):
            st.session_state.show_registration = True
            st.rerun()
        return
    
    # Show authenticated interface with navigation
    render_authenticated_interface()

if __name__ == "__main__":
    main()

