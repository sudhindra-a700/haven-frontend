"""
HAVEN Crowdfunding Platform - Enhanced Registration with Document Verification
Added PAN/Aadhaar for individuals and legitimacy certificates for organizations
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

# HAVEN Logo SVG - Minimalist Design
HAVEN_LOGO_SVG = """
<svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="60" height="60" rx="12" fill="#4CAF50"/>
    <path d="M15 20h30v5H15z" fill="white"/>
    <path d="M20 25h20v15H20z" fill="white" opacity="0.8"/>
    <path d="M25 30h10v5H25z" fill="white"/>
    <circle cx="30" cy="45" r="3" fill="white"/>
</svg>
"""

# Minimalist SVG Icons
MINIMALIST_ICONS = {
    'home': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
        <polyline points="9,22 9,12 15,12 15,22"/>
    </svg>
    """,
    'campaign': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <polygon points="10,8 16,12 10,16 10,8"/>
    </svg>
    """,
    'explore': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8"/>
        <path d="m21 21-4.35-4.35"/>
    </svg>
    """,
    'search': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8"/>
        <path d="m21 21-4.35-4.35"/>
    </svg>
    """,
    'profile': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
        <circle cx="12" cy="7" r="4"/>
    </svg>
    """,
    'logout': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
        <polyline points="16,17 21,12 16,7"/>
        <line x1="21" y1="12" x2="9" y2="12"/>
    </svg>
    """,
    'user': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
        <circle cx="12" cy="7" r="4"/>
    </svg>
    """,
    'key': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="7" cy="7" r="3"/>
        <path d="m10 10 11 11"/>
        <path d="m15 15 6 6"/>
        <path d="m20 15-1.5-1.5"/>
        <path d="m4 4 3 3"/>
    </svg>
    """,
    'lock': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
        <circle cx="12" cy="7" r="4"/>
    </svg>
    """,
    'target': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <circle cx="12" cy="12" r="6"/>
        <circle cx="12" cy="12" r="2"/>
    </svg>
    """,
    'heart': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 1.51 4.04 3 5.5l7 7Z"/>
    </svg>
    """,
    'globe': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <line x1="2" y1="12" x2="22" y2="12"/>
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
    </svg>
    """,
    'navigation': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="3,11 22,2 13,21 11,13 3,11"/>
    </svg>
    """,
    'lightning': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="13,2 3,14 12,14 11,22 21,10 12,10 13,2"/>
    </svg>
    """,
    'chart': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="20" x2="18" y2="10"/>
        <line x1="12" y1="20" x2="12" y2="4"/>
        <line x1="6" y1="20" x2="6" y2="14"/>
    </svg>
    """,
    'arrow-left': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="19" y1="12" x2="5" y2="12"/>
        <polyline points="12,19 5,12 12,5"/>
    </svg>
    """,
    'file': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
        <polyline points="14,2 14,8 20,8"/>
        <line x1="16" y1="13" x2="8" y2="13"/>
        <line x1="16" y1="17" x2="8" y2="17"/>
        <polyline points="10,9 9,9 8,9"/>
    </svg>
    """,
    'upload': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="7,10 12,5 17,10"/>
        <line x1="12" y1="5" x2="12" y2="15"/>
    </svg>
    """,
    'shield': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
    """,
    'check': """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20,6 9,17 4,12"/>
    </svg>
    """
}

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
        """Register new user with document verification"""
        try:
            # Validate required documents
            if user_data.get('account_type') == 'individual':
                if not user_data.get('pan_card') or not user_data.get('aadhaar_card'):
                    return False, "PAN and Aadhaar documents are required for individual accounts"
            
            elif user_data.get('account_type') == 'organization':
                if not user_data.get('registration_certificate'):
                    return False, "Registration certificate is required for organization accounts"
            
            # Demo registration - always works for testing
            demo_user = {
                'id': f'user_{int(time.time())}',
                'email': user_data['email'],
                'name': user_data.get('full_name', user_data.get('org_name', 'User')),
                'account_type': user_data.get('account_type', 'individual'),
                'verified': False,
                'documents_submitted': True,
                'verification_status': 'pending'
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
# DOCUMENT VERIFICATION UTILITIES
# ============================================================================

def validate_document_upload(uploaded_file, doc_type: str) -> Tuple[bool, str]:
    """Validate uploaded document"""
    if uploaded_file is None:
        return False, f"{doc_type} is required"
    
    # Check file size (max 5MB)
    if uploaded_file.size > 5 * 1024 * 1024:
        return False, f"{doc_type} file size must be less than 5MB"
    
    # Check file type
    allowed_types = ['pdf', 'jpg', 'jpeg', 'png']
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension not in allowed_types:
        return False, f"{doc_type} must be PDF, JPG, JPEG, or PNG format"
    
    return True, "Valid document"

def render_document_upload_section(doc_type: str, label: str, help_text: str, required: bool = True):
    """Render document upload section with validation"""
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #4CAF50;">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            {MINIMALIST_ICONS['file']}
            <span style="margin-left: 0.5rem; font-weight: 600; color: #2e7d32;">{label}</span>
            {'<span style="color: #d32f2f; margin-left: 0.25rem;">*</span>' if required else ''}
        </div>
        <p style="color: #666; margin: 0.5rem 0; font-size: 0.9rem;">{help_text}</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        f"Upload {label}",
        type=['pdf', 'jpg', 'jpeg', 'png'],
        key=f"upload_{doc_type}",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        is_valid, message = validate_document_upload(uploaded_file, label)
        
        if is_valid:
            st.success(f"✅ {label} uploaded successfully")
            
            # Show file details
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text(f"📄 {uploaded_file.name}")
            with col2:
                st.text(f"📊 {uploaded_file.size / 1024:.1f} KB")
            with col3:
                st.text(f"📁 {uploaded_file.type}")
        else:
            st.error(f"❌ {message}")
            uploaded_file = None
    
    return uploaded_file

# ============================================================================
# NAVIGATION UTILITIES
# ============================================================================

def render_sidebar_navigation():
    """Render sidebar navigation with minimalist icons"""
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
        {MINIMALIST_ICONS['navigation']}
        <span style="margin-left: 0.5rem; font-weight: 600; color: #2e7d32;">Navigation</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current page for highlighting
    current_page = st.session_state.get('current_page', 'home')
    
    # Navigation items with minimalist icons
    nav_items = [
        ('home', 'home', 'Home'),
        ('campaign', 'target', 'Campaign'),
        ('explore', 'explore', 'Explore'),
        ('search', 'search', 'Search'),
        ('profile', 'profile', 'Profile')
    ]
    
    # Create clickable navigation links
    for page_key, icon_key, label in nav_items:
        # Highlight current page
        if current_page == page_key:
            # Active page styling
            st.markdown(f"""
            <div style="background: #4CAF50; color: white; padding: 0.75rem 1rem; 
                        border-radius: 8px; margin: 0.25rem 0; cursor: pointer;
                        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
                        display: flex; align-items: center;">
                <span style="margin-right: 0.75rem;">{MINIMALIST_ICONS[icon_key]}</span>
                <span style="font-weight: 600;">{label}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Inactive page - clickable
            if st.button(f"{label}", key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()

# ============================================================================
# PAGE FUNCTIONS
# ============================================================================

def show_login():
    """Show login page with minimalist design"""
    # Main content area (right side)
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0;">
        <div style="display: inline-block; margin-bottom: 1rem;">
            {HAVEN_LOGO_SVG}
        </div>
        <h1 style="color: #4CAF50; margin: 0.5rem 0;">Welcome to HAVEN</h1>
        <h2 style="color: #4CAF50; font-weight: normal; margin: 0.5rem 0;">Your Trusted Crowdfunding Platform</h2>
        <p style="color: #4CAF50; margin: 1rem 0;">Empowering communities to support causes that matter</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language selector with minimalist globe icon
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin: 1rem 0;">
        {MINIMALIST_ICONS['globe']}
        <span style="margin-left: 0.5rem; font-weight: 600;">Language</span>
    </div>
    """, unsafe_allow_html=True)
    
    language = st.selectbox(
        "Select Language",
        ["English", "हिंदी", "தமிழ்", "తెలుగు"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Get Started section with minimalist lock icon
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin: 1rem 0;">
        {MINIMALIST_ICONS['lock']}
        <span style="margin-left: 0.5rem; font-weight: 600;">Get Started</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
            <div style="margin-bottom: 0.5rem; color: #666;">{MINIMALIST_ICONS['key']}</div>
            <h3 style="color: #4CAF50; margin: 0.5rem 0;">Existing User</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Sign In", use_container_width=True, key="existing_user"):
            st.session_state.show_login_form = True
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
            <div style="margin-bottom: 0.5rem; color: #666;">{MINIMALIST_ICONS['user']}</div>
            <h3 style="color: #4CAF50; margin: 0.5rem 0;">New User</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Create Account", use_container_width=True, key="new_user"):
            st.session_state.current_page = 'register'
            st.rerun()
    
    # Show login form if "Existing User" was clicked
    if st.session_state.get('show_login_form', False):
        st.markdown("---")
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 1rem 0;">
            {MINIMALIST_ICONS['key']}
            <span style="margin-left: 0.5rem; font-weight: 600; font-size: 1.2rem;">Sign In to HAVEN</span>
        </div>
        """, unsafe_allow_html=True)
        
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
            if st.button("Google", use_container_width=True, key="google_login"):
                success, result = auth_manager.login_user('google', {})
                if success:
                    st.success(f"Welcome, {result.get('name', 'User')}!")
                    time.sleep(1)
                    st.session_state.current_page = 'home'
                    st.session_state.show_login_form = False
                    st.rerun()
        
        with col2:
            if st.button("Facebook", use_container_width=True, key="facebook_login"):
                success, result = auth_manager.login_user('facebook', {})
                if success:
                    st.success(f"Welcome, {result.get('name', 'User')}!")
                    time.sleep(1)
                    st.session_state.current_page = 'home'
                    st.session_state.show_login_form = False
                    st.rerun()
        
        if st.button(f"Back to Get Started", key="back_to_start"):
            st.session_state.show_login_form = False
            st.rerun()

def show_register():
    """Show registration page with document verification"""
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
        # Individual Registration Form with Document Verification
        with st.form("individual_register"):
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin: 1rem 0;">
                {MINIMALIST_ICONS['user']}
                <span style="margin-left: 0.5rem; font-weight: 600; font-size: 1.1rem;">Individual Account Registration</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Basic Information
            st.markdown("#### 📝 Basic Information")
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name *", placeholder="Enter your full name")
                email = st.text_input("Email *", placeholder="your.email@example.com")
                password = st.text_input("Password *", type="password", placeholder="Create a strong password")
            
            with col2:
                phone = st.text_input("Phone Number *", placeholder="+91 9876543210")
                confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password")
                date_of_birth = st.date_input("Date of Birth *")
            
            address = st.text_area("Address *", placeholder="Your complete address")
            
            # Document Verification Section
            st.markdown("#### 📄 Document Verification")
            st.markdown(f"""
            <div style="background: #fff3cd; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #ffc107;">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    {MINIMALIST_ICONS['shield']}
                    <span style="margin-left: 0.5rem; font-weight: 600; color: #856404;">Identity Verification Required</span>
                </div>
                <p style="color: #856404; margin: 0; font-size: 0.9rem;">
                    To ensure platform security and prevent fraud, we require valid government-issued identity documents.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # PAN Card Upload
            pan_card = render_document_upload_section(
                "pan_card",
                "PAN Card",
                "Upload a clear image or PDF of your PAN card. Ensure all details are visible and readable.",
                required=True
            )
            
            # Aadhaar Card Upload
            aadhaar_card = render_document_upload_section(
                "aadhaar_card", 
                "Aadhaar Card",
                "Upload a clear image or PDF of your Aadhaar card. You may mask the Aadhaar number for privacy.",
                required=True
            )
            
            # Optional Documents
            st.markdown("#### 📋 Additional Documents (Optional)")
            
            # Bank Statement
            bank_statement = render_document_upload_section(
                "bank_statement",
                "Bank Statement",
                "Upload recent bank statement (last 3 months) for enhanced verification.",
                required=False
            )
            
            # Address Proof
            address_proof = render_document_upload_section(
                "address_proof",
                "Address Proof",
                "Upload utility bill, rental agreement, or other address proof document.",
                required=False
            )
            
            # Terms and conditions
            st.markdown("#### ✅ Terms & Conditions")
            terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
            kyc_consent = st.checkbox("I consent to KYC (Know Your Customer) verification process *")
            data_processing = st.checkbox("I consent to processing of my personal data for verification purposes *")
            newsletter = st.checkbox("Subscribe to newsletter for updates")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("Register as Individual", use_container_width=True):
                    # Validation
                    if not all([full_name, email, phone, password, confirm_password, address]):
                        st.error("Please fill in all required fields marked with *")
                    elif password != confirm_password:
                        st.error("Passwords do not match!")
                    elif not all([terms_accepted, kyc_consent, data_processing]):
                        st.error("Please accept all required terms and consents")
                    elif not pan_card or not aadhaar_card:
                        st.error("PAN Card and Aadhaar Card are required for registration")
                    else:
                        user_data = {
                            'full_name': full_name,
                            'email': email,
                            'phone': phone,
                            'password': password,
                            'address': address,
                            'date_of_birth': date_of_birth,
                            'account_type': 'individual',
                            'newsletter': newsletter,
                            'pan_card': pan_card,
                            'aadhaar_card': aadhaar_card,
                            'bank_statement': bank_statement,
                            'address_proof': address_proof
                        }
                        
                        success, result = auth_manager.register_user('email', user_data)
                        
                        if success:
                            st.success("Registration successful! Your documents will be verified within 24-48 hours.")
                            time.sleep(2)
                            st.session_state.current_page = 'home'
                            st.rerun()
                        else:
                            st.error(f"Registration failed: {result}")
            
            with col2:
                if st.form_submit_button("Sign In Instead", use_container_width=True):
                    st.session_state.current_page = 'login'
                    st.rerun()
    
    else:  # Organization
        # Organization Registration Form with Document Verification
        with st.form("organization_register"):
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin: 1rem 0;">
                {MINIMALIST_ICONS['target']}
                <span style="margin-left: 0.5rem; font-weight: 600; font-size: 1.1rem;">Organization Account Registration</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Basic Information
            st.markdown("#### 🏢 Organization Information")
            col1, col2 = st.columns(2)
            
            with col1:
                org_name = st.text_input("Organization Name *", placeholder="Enter organization name")
                email = st.text_input("Email *", placeholder="organization@example.com")
                org_type = st.selectbox("Organization Type *", ["", "NGO", "Startup", "Charity", "Foundation", "Trust", "Social Enterprise"])
                password = st.text_input("Password *", type="password", placeholder="Create a strong password")
            
            with col2:
                phone = st.text_input("Phone Number *", placeholder="+91 9876543210")
                registration_number = st.text_input("Registration Number *", placeholder="Official registration number")
                confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password")
                established_year = st.number_input("Established Year *", min_value=1900, max_value=2024, value=2020)
            
            description = st.text_area("Organization Description *", placeholder="Describe your organization's mission and activities")
            address = st.text_area("Address *", placeholder="Organization's complete address")
            
            # Additional organization fields
            col1, col2 = st.columns(2)
            
            with col1:
                website = st.text_input("Website", placeholder="https://yourorganization.com")
                contact_person = st.text_input("Contact Person *", placeholder="Primary contact person name")
            
            with col2:
                employee_count = st.selectbox("Employee Count", ["", "1-10", "11-50", "51-200", "200+"])
                annual_turnover = st.selectbox("Annual Turnover", ["", "< ₹1 Lakh", "₹1-10 Lakhs", "₹10-50 Lakhs", "₹50 Lakhs - ₹1 Crore", "> ₹1 Crore"])
            
            # Document Verification Section
            st.markdown("#### 📄 Organization Document Verification")
            st.markdown(f"""
            <div style="background: #fff3cd; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #ffc107;">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    {MINIMALIST_ICONS['shield']}
                    <span style="margin-left: 0.5rem; font-weight: 600; color: #856404;">Organization Verification Required</span>
                </div>
                <p style="color: #856404; margin: 0; font-size: 0.9rem;">
                    To ensure legitimacy and prevent fraudulent organizations, we require official registration documents.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Registration Certificate
            registration_certificate = render_document_upload_section(
                "registration_certificate",
                "Registration Certificate",
                "Upload official registration certificate (Society Registration, Trust Deed, Company Incorporation, etc.)",
                required=True
            )
            
            # Tax Exemption Certificate
            tax_exemption = render_document_upload_section(
                "tax_exemption",
                "Tax Exemption Certificate",
                "Upload 12A/80G certificate for NGOs or relevant tax documents for other organization types.",
                required=True
            )
            
            # PAN Card of Organization
            org_pan_card = render_document_upload_section(
                "org_pan_card",
                "Organization PAN Card",
                "Upload PAN card issued in the name of the organization.",
                required=True
            )
            
            # Additional Documents
            st.markdown("#### 📋 Additional Documents")
            
            # Audited Financial Statements
            financial_statements = render_document_upload_section(
                "financial_statements",
                "Audited Financial Statements",
                "Upload last 2 years audited financial statements or balance sheets.",
                required=False
            )
            
            # Board Resolution
            board_resolution = render_document_upload_section(
                "board_resolution",
                "Board Resolution",
                "Upload board resolution authorizing the contact person to register on behalf of the organization.",
                required=False
            )
            
            # FCRA Certificate (for NGOs)
            if org_type == "NGO":
                fcra_certificate = render_document_upload_section(
                    "fcra_certificate",
                    "FCRA Certificate",
                    "Upload FCRA (Foreign Contribution Regulation Act) certificate if applicable.",
                    required=False
                )
            
            # Terms and conditions
            st.markdown("#### ✅ Terms & Conditions")
            terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
            verification_consent = st.checkbox("I consent to organization verification process *")
            data_processing = st.checkbox("I consent to processing of organization data for verification purposes *")
            authorized_signatory = st.checkbox("I confirm that I am an authorized signatory of this organization *")
            newsletter = st.checkbox("Subscribe to newsletter for updates")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("Register as Organization", use_container_width=True):
                    # Validation
                    required_fields = [org_name, email, phone, password, confirm_password, org_type, 
                                     description, address, registration_number, contact_person, established_year]
                    
                    if not all(required_fields):
                        st.error("Please fill in all required fields marked with *")
                    elif password != confirm_password:
                        st.error("Passwords do not match!")
                    elif not all([terms_accepted, verification_consent, data_processing, authorized_signatory]):
                        st.error("Please accept all required terms and consents")
                    elif not registration_certificate or not tax_exemption or not org_pan_card:
                        st.error("Registration Certificate, Tax Exemption Certificate, and Organization PAN Card are required")
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
                            'annual_turnover': annual_turnover,
                            'account_type': 'organization',
                            'newsletter': newsletter,
                            'registration_certificate': registration_certificate,
                            'tax_exemption': tax_exemption,
                            'org_pan_card': org_pan_card,
                            'financial_statements': financial_statements,
                            'board_resolution': board_resolution
                        }
                        
                        # Add FCRA certificate if NGO
                        if org_type == "NGO" and 'fcra_certificate' in locals():
                            user_data['fcra_certificate'] = fcra_certificate
                        
                        success, result = auth_manager.register_user('email', user_data)
                        
                        if success:
                            st.success("Registration successful! Your organization will be verified within 3-5 business days.")
                            st.info("You will receive email updates about the verification status.")
                            time.sleep(2)
                            st.session_state.current_page = 'home'
                            st.rerun()
                        else:
                            st.error(f"Registration failed: {result}")
            
            with col2:
                if st.form_submit_button("Sign In Instead", use_container_width=True):
                    st.session_state.current_page = 'login'
                    st.rerun()
    
    # Social registration options
    st.markdown("### Or register with:")
    st.info("Note: Social registration will still require document verification to be completed later.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Register with Google", use_container_width=True, key="google_register"):
            success, result = auth_manager.register_user('google', {'account_type': account_type.lower()})
            
            if success:
                st.success(f"Welcome to HAVEN, {result.get('name', 'User')}!")
                st.info("Please complete document verification from your profile to unlock all features.")
                time.sleep(2)
                st.session_state.current_page = 'home'
                st.rerun()
            else:
                st.error(f"Google registration failed: {result}")
    
    with col2:
        if st.button("Register with Facebook", use_container_width=True, key="facebook_register"):
            success, result = auth_manager.register_user('facebook', {'account_type': account_type.lower()})
            
            if success:
                st.success(f"Welcome to HAVEN, {result.get('name', 'User')}!")
                st.info("Please complete document verification from your profile to unlock all features.")
                time.sleep(2)
                st.session_state.current_page = 'home'
                st.rerun()
            else:
                st.error(f"Facebook registration failed: {result}")
    
    # Back to login button
    if st.button("Back to Login", use_container_width=True, key="back_to_login"):
        st.session_state.current_page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_home():
    """Show authenticated user dashboard with verification status"""
    user_data = st.session_state.user_data
    
    # Header with user info
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        {MINIMALIST_ICONS['home']}
        <span style="margin-left: 0.5rem; font-size: 1.5rem; font-weight: 600; color: #2e7d32;">
            Welcome back, {user_data.get('name', 'User')}!
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Verification Status
    verification_status = user_data.get('verification_status', 'pending')
    if verification_status == 'pending':
        st.warning("📋 Document verification is pending. Some features may be limited until verification is complete.")
    elif verification_status == 'verified':
        st.success("✅ Your account is fully verified!")
    elif verification_status == 'rejected':
        st.error("❌ Document verification was rejected. Please contact support or re-submit documents.")
    
    if user_data.get('account_type') == 'organization':
        st.markdown(f"**Organization Type:** {user_data.get('org_type', 'N/A')}")
    
    # Logout button with icon
    if st.button("Logout", key="logout_btn"):
        auth_manager.logout_user()
        st.rerun()
    
    # Dashboard content
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin: 2rem 0 1rem 0;">
        {MINIMALIST_ICONS['lightning']}
        <span style="margin-left: 0.5rem; font-size: 1.3rem; font-weight: 600; color: #2e7d32;">Quick Actions</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 2rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <div style="margin-bottom: 1rem; color: #2e7d32;">{MINIMALIST_ICONS['target']}</div>
            <h3 style="color: #2e7d32;">Create Campaign</h3>
            <p style="color: #666;">Launch your crowdfunding campaign</p>
        </div>
        """, unsafe_allow_html=True)
        
        if verification_status == 'verified':
            if st.button("Start Campaign", use_container_width=True, key="create_campaign_btn"):
                st.session_state.current_page = 'campaign'
                st.rerun()
        else:
            st.button("Start Campaign", use_container_width=True, disabled=True, key="create_campaign_btn_disabled")
            st.caption("⚠️ Requires verification")
    
    with col2:
        st.markdown(f"""
        <div style="background: white; padding: 2rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <div style="margin-bottom: 1rem; color: #2e7d32;">{MINIMALIST_ICONS['explore']}</div>
            <h3 style="color: #2e7d32;">Browse Projects</h3>
            <p style="color: #666;">Discover amazing causes to support</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Browse Now", use_container_width=True, key="browse_campaigns_btn"):
            st.session_state.current_page = 'explore'
            st.rerun()
    
    with col3:
        st.markdown(f"""
        <div style="background: white; padding: 2rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <div style="margin-bottom: 1rem; color: #2e7d32;">{MINIMALIST_ICONS['heart']}</div>
            <h3 style="color: #2e7d32;">Support Causes</h3>
            <p style="color: #666;">Make a difference today</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Donate Now", use_container_width=True, key="support_causes_btn"):
            st.session_state.current_page = 'explore'
            st.rerun()
    
    # User stats (placeholder)
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin: 2rem 0 1rem 0;">
        {MINIMALIST_ICONS['chart']}
        <span style="margin-left: 0.5rem; font-size: 1.3rem; font-weight: 600; color: #2e7d32;">Your Impact</span>
    </div>
    """, unsafe_allow_html=True)
    
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
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        {MINIMALIST_ICONS['target']}
        <span style="margin-left: 0.5rem; font-size: 1.5rem; font-weight: 600; color: #2e7d32;">Create Your Campaign</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Campaign creation feature coming soon!")
    
    if st.button("Back to Dashboard", key="back_to_dashboard_campaign"):
        st.session_state.current_page = 'home'
        st.rerun()

def show_explore():
    """Show campaign browsing page"""
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        {MINIMALIST_ICONS['explore']}
        <span style="margin-left: 0.5rem; font-size: 1.5rem; font-weight: 600; color: #2e7d32;">Explore Campaigns</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Campaign browsing feature coming soon!")
    
    if st.button("Back to Dashboard", key="back_to_dashboard_explore"):
        st.session_state.current_page = 'home'
        st.rerun()

def show_search():
    """Show search page"""
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        {MINIMALIST_ICONS['search']}
        <span style="margin-left: 0.5rem; font-size: 1.5rem; font-weight: 600; color: #2e7d32;">Search Campaigns</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Search feature coming soon!")
    
    if st.button("Back to Dashboard", key="back_to_dashboard_search"):
        st.session_state.current_page = 'home'
        st.rerun()

def show_profile():
    """Show profile page with document verification status"""
    user_data = st.session_state.user_data
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        {MINIMALIST_ICONS['profile']}
        <span style="margin-left: 0.5rem; font-size: 1.5rem; font-weight: 600; color: #2e7d32;">User Profile</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Verification Status Section
    st.markdown("### 📋 Verification Status")
    
    verification_status = user_data.get('verification_status', 'pending')
    
    if verification_status == 'pending':
        st.warning("⏳ Document verification is in progress. This typically takes 24-48 hours for individuals and 3-5 business days for organizations.")
    elif verification_status == 'verified':
        st.success("✅ Your account is fully verified! You can now access all platform features.")
    elif verification_status == 'rejected':
        st.error("❌ Document verification was rejected. Please contact support for details.")
        
        if st.button("Re-submit Documents"):
            st.session_state.current_page = 'register'
            st.rerun()
    
    # Documents Submitted
    if user_data.get('documents_submitted'):
        st.markdown("### 📄 Documents Submitted")
        
        if user_data.get('account_type') == 'individual':
            st.markdown("- ✅ PAN Card")
            st.markdown("- ✅ Aadhaar Card")
        else:
            st.markdown("- ✅ Registration Certificate")
            st.markdown("- ✅ Tax Exemption Certificate")
            st.markdown("- ✅ Organization PAN Card")
    
    st.info("Profile management feature coming soon!")
    
    if st.button("Back to Dashboard", key="back_to_dashboard_profile"):
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
    
    # Custom CSS for minimalist design and light green theme
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
    
    .stButton > button:disabled {
        background: #cccccc;
        color: #666666;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: #f8f9fa;
        border: 2px dashed #4caf50;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Success/Error message styling */
    .stAlert {
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Form styling */
    .stForm {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
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
            render_sidebar_navigation()
            
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

