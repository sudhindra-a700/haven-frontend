"""
HAVEN Crowdfunding Platform - Login First Design
Modified to show login page first while maintaining the sidebar design and layout from the image
"""

import streamlit as st
import requests
import logging
from typing import Dict, Any, List, Optional, Tuple
import time
import uuid
import random
import hashlib
import secrets
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HAVEN Logo SVG
HAVEN_LOGO_SVG = """
<svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="60" height="60" rx="12" fill="#4CAF50"/>
    <path d="M15 20h30v5H15z" fill="white"/>
    <path d="M20 25h20v15H20z" fill="white" opacity="0.8"/>
    <path d="M25 30h10v5H25z" fill="white"/>
    <circle cx="30" cy="45" r="3" fill="white"/>
</svg>
"""

# ============================================================================
# AUTHENTICATION UTILITIES
# ============================================================================

class AuthenticationManager:
    """Manages authentication state and operations"""
    
    def __init__(self):
        self.backend_url = self._get_backend_url()
        self.session_timeout = 3600  # 1 hour
        self.max_login_attempts = 5
    
    def _get_backend_url(self) -> str:
        """Get backend URL from configuration"""
        try:
            return st.secrets.get("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")
        except:
            return "https://haven-fastapi-backend.onrender.com"
    
    def initialize_auth_state(self):
        """Initialize authentication-related session state"""
        if 'auth_token' not in st.session_state:
            st.session_state.auth_token = None
        
        if 'auth_expires' not in st.session_state:
            st.session_state.auth_expires = 0
        
        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = 0
        
        if 'last_login_attempt' not in st.session_state:
            st.session_state.last_login_attempt = 0
    
    def check_authentication(self) -> bool:
        """Check if user is currently authenticated"""
        if not st.session_state.get('authenticated', False):
            return False
        
        # Check token expiration
        if st.session_state.auth_expires < time.time():
            self.logout_user()
            return False
        
        return True
    
    def login_user(self, method: str, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
        """Login user with specified method"""
        self.initialize_auth_state()
        
        try:
            if method == 'email':
                return self._login_email(credentials)
            elif method == 'google':
                return self._login_oauth('google', credentials)
            elif method == 'facebook':
                return self._login_oauth('facebook', credentials)
            else:
                return False, f"Unsupported login method: {method}"
        
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False, f"Login failed: {str(e)}"
    
    def _login_email(self, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
        """Login with email and password"""
        try:
            # Demo mode fallback - always works for testing
            if credentials['email'] and credentials['password']:
                demo_user = {
                    'id': 'demo_user',
                    'email': credentials['email'],
                    'name': credentials['email'].split('@')[0],
                    'verified': True
                }
                self._set_auth_session({'user': demo_user, 'token': 'demo_token'})
                return True, demo_user
            return False, "Please enter both email and password"
        
        except Exception as e:
            logger.error(f"Email login failed: {e}")
            return False, "Login failed. Please try again."
    
    def _login_oauth(self, provider: str, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
        """Login with OAuth provider"""
        try:
            # Demo OAuth login
            demo_user = {
                'id': f'oauth_{provider}_demo',
                'email': f'demo@{provider}.com',
                'name': f'{provider.title()} User',
                'provider': provider,
                'verified': True
            }
            
            self._set_auth_session({'user': demo_user, 'token': f'oauth_{provider}_token'})
            return True, demo_user
        
        except Exception as e:
            logger.error(f"OAuth login failed: {e}")
            return False, f"OAuth login failed: {str(e)}"
    
    def register_user(self, method: str, user_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Register new user"""
        try:
            # Demo registration - always works for testing
            demo_user = {
                'id': f'user_{int(time.time())}',
                'email': user_data['email'],
                'name': user_data.get('full_name', user_data.get('org_name', 'User')),
                'account_type': user_data.get('account_type', 'individual'),
                'verified': False
            }
            self._set_auth_session({'user': demo_user, 'token': 'demo_token'})
            return True, demo_user
        
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False, f"Registration failed: {str(e)}"
    
    def _set_auth_session(self, auth_data: Dict[str, Any]):
        """Set authentication session data"""
        st.session_state.authenticated = True
        st.session_state.user_data = auth_data['user']
        st.session_state.auth_token = auth_data.get('token')
        st.session_state.auth_expires = time.time() + self.session_timeout
        st.session_state.login_attempts = 0
    
    def logout_user(self):
        """Logout current user"""
        st.session_state.authenticated = False
        st.session_state.user_data = {}
        st.session_state.auth_token = None
        st.session_state.auth_expires = 0
        st.session_state.current_page = 'login'

# Global authentication manager instance
auth_manager = AuthenticationManager()

# ============================================================================
# PAGE FUNCTIONS
# ============================================================================

def show_login():
    """Show login page with the design from the image"""
    # Main content area (right side)
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <div style="display: inline-block; margin-bottom: 1rem;">
            🏠
        </div>
        <h1 style="color: #4CAF50; margin: 0.5rem 0;">Welcome to HAVEN</h1>
        <h2 style="color: #4CAF50; font-weight: normal; margin: 0.5rem 0;">Your Trusted Crowdfunding Platform</h2>
        <p style="color: #4CAF50; margin: 1rem 0;">Empowering communities to support causes that matter</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language selector
    st.markdown("🌐 **Language**")
    language = st.selectbox(
        "Select Language",
        ["🇺🇸 English", "🇮🇳 हिंदी", "🇮🇳 தமிழ்", "🇮🇳 తెలుగు"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Get Started section
    st.markdown("🔒 **Get Started**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔑</div>
            <h3 style="color: #4CAF50; margin: 0.5rem 0;">Existing User</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Sign In", use_container_width=True, key="existing_user"):
            st.session_state.show_login_form = True
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">👤</div>
            <h3 style="color: #4CAF50; margin: 0.5rem 0;">New User</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Create Account", use_container_width=True, key="new_user"):
            st.session_state.current_page = 'register'
            st.rerun()
    
    # Show login form if "Existing User" was clicked
    if st.session_state.get('show_login_form', False):
        st.markdown("---")
        st.markdown("### 🔑 Sign In to HAVEN")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Continue", use_container_width=True):
                    if email and password:
                        success, result = auth_manager.login_user('email', {'email': email, 'password': password})
                        
                        if success:
                            st.success(f"Welcome back, {result.get('name', 'User')}!")
                            time.sleep(1)
                            st.session_state.current_page = 'home'
                            st.session_state.show_login_form = False
                            st.rerun()
                        else:
                            st.error(f"Login failed: {result}")
                    else:
                        st.error("Please enter both email and password")
            
            with col2:
                if st.form_submit_button("Sign Up", use_container_width=True):
                    st.session_state.current_page = 'register'
                    st.session_state.show_login_form = False
                    st.rerun()
        
        st.markdown("### Or continue with:")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔴 Google", use_container_width=True, key="google_login"):
                success, result = auth_manager.login_user('google', {})
                if success:
                    st.success(f"Welcome, {result.get('name', 'User')}!")
                    time.sleep(1)
                    st.session_state.current_page = 'home'
                    st.session_state.show_login_form = False
                    st.rerun()
        
        with col2:
            if st.button("🔵 Facebook", use_container_width=True, key="facebook_login"):
                success, result = auth_manager.login_user('facebook', {})
                if success:
                    st.success(f"Welcome, {result.get('name', 'User')}!")
                    time.sleep(1)
                    st.session_state.current_page = 'home'
                    st.session_state.show_login_form = False
                    st.rerun()
        
        if st.button("⬅️ Back to Get Started"):
            st.session_state.show_login_form = False
            st.rerun()

def show_register():
    """Show registration page with HAVEN logo and account types"""
    # HAVEN Header with Logo
    st.markdown(f"""
    <div class="header-container" style="text-align: center; padding: 2rem; 
                background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                border-radius: 15px; margin-bottom: 2rem;">
        <div class="header-logo" style="margin-bottom: 1rem;">
            {HAVEN_LOGO_SVG}
        </div>
        <div class="header-subtitle" style="color: #2e7d32; font-size: 1.5rem; font-weight: 600;">
            Help not just some people, but Help Humanity
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    st.markdown("## Register for HAVEN")
    
    # Account type selection
    account_type = st.selectbox("Account Type", ["Individual", "Organization"])
    
    if account_type == "Individual":
        # Individual Registration Form
        with st.form("individual_register"):
            st.markdown("#### 👤 Individual Account Registration")
            
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name *", placeholder="Enter your full name")
                email = st.text_input("Email *", placeholder="your.email@example.com")
                password = st.text_input("Password *", type="password", placeholder="Create a strong password")
            
            with col2:
                phone = st.text_input("Phone Number *", placeholder="+91 9876543210")
                confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password")
            
            address = st.text_area("Address", placeholder="Your complete address")
            
            # Terms and conditions
            terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
            newsletter = st.checkbox("Subscribe to newsletter for updates")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("👤 Register as Individual", use_container_width=True):
                    if not all([full_name, email, phone, password, confirm_password]):
                        st.error("Please fill in all required fields marked with *")
                    elif password != confirm_password:
                        st.error("Passwords do not match!")
                    elif not terms_accepted:
                        st.error("Please accept the Terms of Service")
                    else:
                        user_data = {
                            'full_name': full_name,
                            'email': email,
                            'phone': phone,
                            'password': password,
                            'address': address,
                            'account_type': 'individual',
                            'newsletter': newsletter
                        }
                        
                        success, result = auth_manager.register_user('email', user_data)
                        
                        if success:
                            st.success("Registration successful!")
                            time.sleep(1)
                            st.session_state.current_page = 'home'
                            st.rerun()
                        else:
                            st.error(f"Registration failed: {result}")
            
            with col2:
                if st.form_submit_button("🔑 Sign In Instead", use_container_width=True):
                    st.session_state.current_page = 'login'
                    st.rerun()
    
    else:  # Organization
        # Organization Registration Form
        with st.form("organization_register"):
            st.markdown("#### 🏢 Organization Account Registration")
            
            col1, col2 = st.columns(2)
            
            with col1:
                org_name = st.text_input("Organization Name *", placeholder="Enter organization name")
                email = st.text_input("Email *", placeholder="organization@example.com")
                org_type = st.selectbox("Organization Type *", ["", "NGO", "Startup", "Charity", "Foundation", "Trust"])
                password = st.text_input("Password *", type="password", placeholder="Create a strong password")
            
            with col2:
                phone = st.text_input("Phone Number *", placeholder="+91 9876543210")
                registration_number = st.text_input("Registration Number", placeholder="Official registration number")
                confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password")
            
            description = st.text_area("Organization Description *", placeholder="Describe your organization's mission and activities")
            address = st.text_area("Address *", placeholder="Organization's complete address")
            
            # Additional organization fields
            col1, col2 = st.columns(2)
            
            with col1:
                website = st.text_input("Website", placeholder="https://yourorganization.com")
                established_year = st.number_input("Established Year", min_value=1900, max_value=2024, value=2020)
            
            with col2:
                contact_person = st.text_input("Contact Person", placeholder="Primary contact person name")
                employee_count = st.selectbox("Employee Count", ["", "1-10", "11-50", "51-200", "200+"])
            
            # Terms and conditions
            terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
            verification_consent = st.checkbox("I consent to organization verification process *")
            newsletter = st.checkbox("Subscribe to newsletter for updates")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("🏢 Register as Organization", use_container_width=True):
                    if not all([org_name, email, phone, password, confirm_password, org_type, description, address]):
                        st.error("Please fill in all required fields marked with *")
                    elif password != confirm_password:
                        st.error("Passwords do not match!")
                    elif not terms_accepted or not verification_consent:
                        st.error("Please accept the Terms of Service and verification consent")
                    else:
                        user_data = {
                            'org_name': org_name,
                            'email': email,
                            'phone': phone,
                            'password': password,
                            'org_type': org_type,
                            'description': description,
                            'address': address,
                            'registration_number': registration_number,
                            'website': website,
                            'established_year': established_year,
                            'contact_person': contact_person,
                            'employee_count': employee_count,
                            'account_type': 'organization',
                            'newsletter': newsletter
                        }
                        
                        success, result = auth_manager.register_user('email', user_data)
                        
                        if success:
                            st.success("Registration successful! Your organization will be verified within 24-48 hours.")
                            time.sleep(1)
                            st.session_state.current_page = 'home'
                            st.rerun()
                        else:
                            st.error(f"Registration failed: {result}")
            
            with col2:
                if st.form_submit_button("🔑 Sign In Instead", use_container_width=True):
                    st.session_state.current_page = 'login'
                    st.rerun()
    
    # Social registration options
    st.markdown("### Or register with:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔴 Register with Google", use_container_width=True, key="google_register"):
            success, result = auth_manager.register_user('google', {'account_type': account_type.lower()})
            
            if success:
                st.success(f"Welcome to HAVEN, {result.get('name', 'User')}!")
                time.sleep(1)
                st.session_state.current_page = 'home'
                st.rerun()
            else:
                st.error(f"Google registration failed: {result}")
    
    with col2:
        if st.button("🔵 Register with Facebook", use_container_width=True, key="facebook_register"):
            success, result = auth_manager.register_user('facebook', {'account_type': account_type.lower()})
            
            if success:
                st.success(f"Welcome to HAVEN, {result.get('name', 'User')}!")
                time.sleep(1)
                st.session_state.current_page = 'home'
                st.rerun()
            else:
                st.error(f"Facebook registration failed: {result}")
    
    # Back to login button
    if st.button("⬅️ Back to Login", use_container_width=True):
        st.session_state.current_page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_home():
    """Show authenticated user dashboard"""
    user_data = st.session_state.user_data
    
    # Header with user info
    st.markdown(f"### 🏠 Welcome back, {user_data.get('name', 'User')}!")
    
    if user_data.get('account_type') == 'organization':
        st.markdown(f"**Organization Type:** {user_data.get('org_type', 'N/A')}")
    
    # Logout button
    if st.button("🚪 Logout"):
        auth_manager.logout_user()
        st.rerun()
    
    # Dashboard content
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <h3 style="color: #2e7d32;">🎯 Create Campaign</h3>
            <p style="color: #666;">Launch your crowdfunding campaign</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Campaign", use_container_width=True, key="create_campaign_btn"):
            st.session_state.current_page = 'campaign'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <h3 style="color: #2e7d32;">🔍 Browse Projects</h3>
            <p style="color: #666;">Discover amazing causes to support</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 Browse Now", use_container_width=True, key="browse_campaigns_btn"):
            st.session_state.current_page = 'explore'
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <h3 style="color: #2e7d32;">💝 Support Causes</h3>
            <p style="color: #666;">Make a difference today</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💝 Donate Now", use_container_width=True, key="support_causes_btn"):
            st.session_state.current_page = 'explore'
            st.rerun()
    
    # User stats (placeholder)
    st.markdown("### 📊 Your Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Campaigns Created", "0", "0")
    
    with col2:
        st.metric("Total Raised", "₹0", "₹0")
    
    with col3:
        st.metric("Donations Made", "0", "0")
    
    with col4:
        st.metric("Lives Impacted", "0", "0")

def show_campaign():
    """Show campaign creation page"""
    st.markdown("### 🎯 Create Your Campaign")
    st.info("Campaign creation feature coming soon!")
    
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.current_page = 'home'
        st.rerun()

def show_explore():
    """Show campaign browsing page"""
    st.markdown("### 🔍 Explore Campaigns")
    st.info("Campaign browsing feature coming soon!")
    
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.current_page = 'home'
        st.rerun()

def show_search():
    """Show search page"""
    st.markdown("### 🔍 Search Campaigns")
    st.info("Search feature coming soon!")
    
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.current_page = 'home'
        st.rerun()

def show_profile():
    """Show profile page"""
    st.markdown("### 👤 User Profile")
    st.info("Profile management feature coming soon!")
    
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.current_page = 'home'
        st.rerun()

def show_footer():
    """Show footer"""
    st.markdown("---")
    st.markdown("© 2025 HAVEN - Crowdfunding Platform | Built with ❤️ using Streamlit")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    # Configure Streamlit page
    st.set_page_config(
        page_title="HAVEN - Crowdfunding Platform",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for light green theme
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e8 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .auth-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'  # Start with login page
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    if 'show_login_form' not in st.session_state:
        st.session_state.show_login_form = False
    
    # Initialize auth manager
    auth_manager.initialize_auth_state()
    
    # Sidebar navigation (only show if authenticated)
    if st.session_state.authenticated:
        with st.sidebar:
            st.markdown("### 🧭 Navigation")
            
            # Navigation buttons
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.current_page = 'home'
                st.rerun()
            
            if st.button("🎯 Campaign", use_container_width=True):
                st.session_state.current_page = 'campaign'
                st.rerun()
            
            if st.button("🔍 Explore", use_container_width=True):
                st.session_state.current_page = 'explore'
                st.rerun()
            
            if st.button("🔍 Search", use_container_width=True):
                st.session_state.current_page = 'search'
                st.rerun()
            
            if st.button("👤 Profile", use_container_width=True):
                st.session_state.current_page = 'profile'
                st.rerun()
            
            st.markdown("---")
            
            # Debug mode toggle
            debug_mode = st.checkbox("Debug Mode")
            if debug_mode:
                st.write("**Session State:**")
                st.json(dict(st.session_state))
    
    # Main content area
    if not st.session_state.authenticated:
        # Show login or register page
        if st.session_state.current_page == 'register':
            show_register()
        else:
            show_login()
    else:
        # Show authenticated pages
        if st.session_state.current_page == 'home':
            show_home()
        elif st.session_state.current_page == 'campaign':
            show_campaign()
        elif st.session_state.current_page == 'explore':
            show_explore()
        elif st.session_state.current_page == 'search':
            show_search()
        elif st.session_state.current_page == 'profile':
            show_profile()
        else:
            show_home()  # Default to home
    
    # Footer
    show_footer()

if __name__ == "__main__":
    main()

