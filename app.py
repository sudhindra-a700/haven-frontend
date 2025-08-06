"""
Complete Workflow-Based HAVEN Frontend Application
Implements the exact workflow from the diagrams with proper state management
"""

import streamlit as st
import logging
from typing import Dict, Any, Optional
import time
from datetime import datetime

# Import workflow modules
from workflow_auth_utils import auth_manager, check_authentication, login_user, register_user, logout_user
from workflow_campaign_pages import (
    render_create_campaign_page, render_submit_campaign_page, 
    render_xai_processing_page
)
from workflow_verification_funding import (
    render_admin_review_page, render_funding_display_page, render_discard_project_page,
    render_browse_campaigns_page, render_view_campaign_page, render_verification_check_page,
    render_show_warning_page, render_make_contribution_page, render_payment_page,
    render_success_page
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowManager:
    """Manages the complete workflow state and navigation"""
    
    def __init__(self):
        self.workflow_states = {
            'start': 'start',
            'login': 'login',
            'register': 'register',
            'authenticated': 'authenticated',
            'create_campaign': 'create_campaign',
            'submit_campaign': 'submit_campaign',
            'xai_processing': 'xai_processing',
            'admin_review': 'admin_review',
            'funding_display': 'funding_display',
            'discard_project': 'discard_project',
            'browse_campaigns': 'browse_campaigns',
            'view_campaign': 'view_campaign',
            'verification_check': 'verification_check',
            'show_warning': 'show_warning',
            'make_contribution': 'make_contribution',
            'payment': 'payment',
            'success': 'success'
        }
        
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize all session state variables"""
        # Authentication state
        if 'user_authenticated' not in st.session_state:
            st.session_state.user_authenticated = False
        
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {}
        
        # Workflow state
        if 'current_workflow_state' not in st.session_state:
            st.session_state.current_workflow_state = 'start'
        
        if 'previous_workflow_state' not in st.session_state:
            st.session_state.previous_workflow_state = None
        
        # Language state
        if 'selected_language' not in st.session_state:
            st.session_state.selected_language = 'English'
        
        # Campaign state
        if 'current_campaign' not in st.session_state:
            st.session_state.current_campaign = {}
        
        if 'selected_campaign' not in st.session_state:
            st.session_state.selected_campaign = {}
        
        # Payment state
        if 'payment_data' not in st.session_state:
            st.session_state.payment_data = {}
        
        # Initialize auth manager
        auth_manager.initialize_auth_state()
    
    def navigate_to(self, current_state: str, action: str):
        """Navigate between workflow states based on current state and action"""
        st.session_state.previous_workflow_state = current_state
        
        # Navigation logic based on workflow diagram
        if current_state == 'start':
            if action == 'login_yes':
                st.session_state.current_workflow_state = 'login'
            elif action == 'login_no':
                st.session_state.current_workflow_state = 'register'
        
        elif current_state == 'login':
            if action == 'success':
                st.session_state.current_workflow_state = 'authenticated'
            elif action == 'register':
                st.session_state.current_workflow_state = 'register'
        
        elif current_state == 'register':
            if action == 'success':
                st.session_state.current_workflow_state = 'authenticated'
            elif action == 'login':
                st.session_state.current_workflow_state = 'login'
        
        elif current_state == 'authenticated':
            if action == 'create':
                st.session_state.current_workflow_state = 'create_campaign'
            elif action == 'browse':
                st.session_state.current_workflow_state = 'browse_campaigns'
            elif action == 'logout':
                logout_user()
                st.session_state.current_workflow_state = 'start'
        
        elif current_state == 'create_campaign':
            if action == 'submit':
                st.session_state.current_workflow_state = 'submit_campaign'
            elif action == 'back':
                st.session_state.current_workflow_state = 'authenticated'
        
        elif current_state == 'submit_campaign':
            if action == 'auto':
                st.session_state.current_workflow_state = 'xai_processing'
            elif action == 'back':
                st.session_state.current_workflow_state = 'authenticated'
        
        elif current_state == 'xai_processing':
            if action == 'auto':
                st.session_state.current_workflow_state = 'admin_review'
        
        elif current_state == 'admin_review':
            if action == 'approved':
                st.session_state.current_workflow_state = 'funding_display'
            elif action == 'rejected':
                st.session_state.current_workflow_state = 'discard_project'
            elif action == 'back':
                st.session_state.current_workflow_state = 'authenticated'
        
        elif current_state == 'funding_display':
            if action == 'view':
                st.session_state.current_workflow_state = 'view_campaign'
            elif action == 'back':
                st.session_state.current_workflow_state = 'authenticated'
        
        elif current_state == 'discard_project':
            if action == 'back':
                st.session_state.current_workflow_state = 'authenticated'
        
        elif current_state == 'browse_campaigns':
            if action == 'view':
                st.session_state.current_workflow_state = 'view_campaign'
            elif action == 'back':
                st.session_state.current_workflow_state = 'authenticated'
        
        elif current_state == 'view_campaign':
            if action == 'fund_yes':
                st.session_state.current_workflow_state = 'verification_check'
            elif action == 'fund_no':
                st.session_state.current_workflow_state = 'show_warning'
            elif action == 'back':
                st.session_state.current_workflow_state = 'browse_campaigns'
        
        elif current_state == 'verification_check':
            if action == 'verified':
                st.session_state.current_workflow_state = 'make_contribution'
            elif action == 'not_verified':
                st.session_state.current_workflow_state = 'show_warning'
            elif action == 'back':
                st.session_state.current_workflow_state = 'view_campaign'
        
        elif current_state == 'show_warning':
            if action == 'back':
                st.session_state.current_workflow_state = 'browse_campaigns'
        
        elif current_state == 'make_contribution':
            if action == 'proceed':
                st.session_state.current_workflow_state = 'payment'
            elif action == 'back':
                st.session_state.current_workflow_state = 'view_campaign'
        
        elif current_state == 'payment':
            if action == 'success':
                st.session_state.current_workflow_state = 'success'
            elif action == 'back':
                st.session_state.current_workflow_state = 'make_contribution'
        
        elif current_state == 'success':
            if action == 'continue':
                st.session_state.current_workflow_state = 'authenticated'
        
        # Rerun to update the display
        st.rerun()
    
    def get_current_state(self) -> str:
        """Get current workflow state"""
        return st.session_state.current_workflow_state
    
    def render_current_page(self):
        """Render the current page based on workflow state"""
        current_state = self.get_current_state()
        
        if current_state == 'start':
            self.render_start_page()
        elif current_state == 'login':
            self.render_login_page()
        elif current_state == 'register':
            self.render_register_page()
        elif current_state == 'authenticated':
            self.render_authenticated_dashboard()
        elif current_state == 'create_campaign':
            render_create_campaign_page(self)
        elif current_state == 'submit_campaign':
            render_submit_campaign_page(self)
        elif current_state == 'xai_processing':
            render_xai_processing_page(self)
        elif current_state == 'admin_review':
            render_admin_review_page(self)
        elif current_state == 'funding_display':
            render_funding_display_page(self)
        elif current_state == 'discard_project':
            render_discard_project_page(self)
        elif current_state == 'browse_campaigns':
            render_browse_campaigns_page(self)
        elif current_state == 'view_campaign':
            render_view_campaign_page(self)
        elif current_state == 'verification_check':
            render_verification_check_page(self)
        elif current_state == 'show_warning':
            render_show_warning_page(self)
        elif current_state == 'make_contribution':
            render_make_contribution_page(self)
        elif current_state == 'payment':
            render_payment_page(self)
        elif current_state == 'success':
            render_success_page(self)
        else:
            st.error(f"Unknown workflow state: {current_state}")
    
    def render_start_page(self):
        """Render the start page - login decision point"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                    padding: 3rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #2e7d32;">🏠 Welcome to HAVEN</h1>
            <h2 style="color: #388e3c;">Your Trusted Crowdfunding Platform</h2>
            <p style="color: #4caf50; font-size: 1.2rem;">
                Empowering communities to support causes that matter
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Language selection (always available)
        self.render_language_selector()
        
        # Login decision
        st.markdown("### 🔐 Get Started")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <h3 style="color: #2e7d32;">🔑 Existing User</h3>
                <p style="color: #666;">Already have an account? Sign in to continue</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔑 Sign In", use_container_width=True, key="signin_btn"):
                self.navigate_to('start', 'login_yes')
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <h3 style="color: #2e7d32;">👤 New User</h3>
                <p style="color: #666;">Join our community and start making a difference</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("👤 Create Account", use_container_width=True, key="signup_btn"):
                self.navigate_to('start', 'login_no')
        
        # Platform features
        st.markdown("---")
        st.markdown("### ✨ Why Choose HAVEN?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <h4 style="color: #2e7d32;">🔒 Secure & Verified</h4>
                <p style="color: #666;">AI-powered fraud detection and manual verification</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <h4 style="color: #2e7d32;">🌍 Multi-Language</h4>
                <p style="color: #666;">Support in English, Hindi, Tamil, and Telugu</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <h4 style="color: #2e7d32;">💝 Transparent</h4>
                <p style="color: #666;">Real-time updates and complete transparency</p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_language_selector(self):
        """Render language selector (always available)"""
        languages = {
            'English': '🇺🇸 English',
            'Hindi': '🇮🇳 हिंदी',
            'Tamil': '🇮🇳 தமிழ்',
            'Telugu': '🇮🇳 తెలుగు'
        }
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col2:
            selected_lang = st.selectbox(
                "🌐 Language",
                options=list(languages.keys()),
                format_func=lambda x: languages[x],
                index=list(languages.keys()).index(st.session_state.selected_language)
            )
            
            if selected_lang != st.session_state.selected_language:
                st.session_state.selected_language = selected_lang
                st.rerun()
    
    def render_login_page(self):
        """Render login page"""
        st.markdown("### 🔑 Sign In to HAVEN")
        
        # Language selector
        self.render_language_selector()
        
        # Login tabs
        tab1, tab2 = st.tabs(["📧 Email Login", "🔗 Social Login"])
        
        with tab1:
            with st.form("email_login_form"):
                st.markdown("#### 📧 Email & Password")
                
                email = st.text_input("Email Address", placeholder="your.email@example.com")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                remember_me = st.checkbox("Remember me")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.form_submit_button("🔑 Sign In", use_container_width=True):
                        if email and password:
                            success, result = login_user('email', {'email': email, 'password': password})
                            
                            if success:
                                st.success(f"Welcome back, {result.get('first_name', 'User')}!")
                                time.sleep(1)
                                self.navigate_to('login', 'success')
                            else:
                                st.error(f"Login failed: {result}")
                        else:
                            st.error("Please enter both email and password")
                
                with col2:
                    if st.form_submit_button("👤 Create Account", use_container_width=True):
                        self.navigate_to('login', 'register')
                
                st.markdown("[Forgot Password?](#)")
        
        with tab2:
            st.markdown("#### 🔗 Social Login")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔴 Google", use_container_width=True, key="google_login"):
                    success, result = login_user('google', {})
                    
                    if success:
                        st.success(f"Welcome, {result.get('first_name', 'User')}!")
                        time.sleep(1)
                        self.navigate_to('login', 'success')
                    else:
                        st.error(f"Google login failed: {result}")
            
            with col2:
                if st.button("🔵 Facebook", use_container_width=True, key="facebook_login"):
                    success, result = login_user('facebook', {})
                    
                    if success:
                        st.success(f"Welcome, {result.get('first_name', 'User')}!")
                        time.sleep(1)
                        self.navigate_to('login', 'success')
                    else:
                        st.error(f"Facebook login failed: {result}")
    
    def render_register_page(self):
        """Render registration page"""
        st.markdown("### 👤 Create Your HAVEN Account")
        
        # Language selector
        self.render_language_selector()
        
        # Registration tabs
        tab1, tab2 = st.tabs(["📧 Email Registration", "🔗 Social Registration"])
        
        with tab1:
            with st.form("email_register_form"):
                st.markdown("#### 📧 Create Account with Email")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    first_name = st.text_input("First Name *", placeholder="Your first name")
                    email = st.text_input("Email Address *", placeholder="your.email@example.com")
                    password = st.text_input("Password *", type="password", placeholder="Create a strong password")
                
                with col2:
                    last_name = st.text_input("Last Name *", placeholder="Your last name")
                    phone = st.text_input("Phone Number", placeholder="+91 9876543210")
                    confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password")
                
                terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
                newsletter = st.checkbox("Subscribe to newsletter for updates")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.form_submit_button("👤 Create Account", use_container_width=True):
                        required_fields = [first_name, last_name, email, password, confirm_password]
                        
                        if not all(required_fields):
                            st.error("Please fill in all required fields marked with *")
                        elif password != confirm_password:
                            st.error("Passwords do not match")
                        elif not terms_accepted:
                            st.error("Please accept the Terms of Service")
                        else:
                            user_data = {
                                'first_name': first_name,
                                'last_name': last_name,
                                'email': email,
                                'password': password,
                                'phone': phone,
                                'newsletter': newsletter
                            }
                            
                            success, result = register_user('email', user_data)
                            
                            if success:
                                st.success(f"Welcome to HAVEN, {result.get('first_name', 'User')}!")
                                time.sleep(1)
                                self.navigate_to('register', 'success')
                            else:
                                st.error(f"Registration failed: {result}")
                
                with col2:
                    if st.form_submit_button("🔑 Sign In Instead", use_container_width=True):
                        self.navigate_to('register', 'login')
        
        with tab2:
            st.markdown("#### 🔗 Quick Registration with Social Media")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔴 Register with Google", use_container_width=True, key="google_register"):
                    success, result = register_user('google', {})
                    
                    if success:
                        st.success(f"Welcome to HAVEN, {result.get('first_name', 'User')}!")
                        time.sleep(1)
                        self.navigate_to('register', 'success')
                    else:
                        st.error(f"Google registration failed: {result}")
            
            with col2:
                if st.button("🔵 Register with Facebook", use_container_width=True, key="facebook_register"):
                    success, result = register_user('facebook', {})
                    
                    if success:
                        st.success(f"Welcome to HAVEN, {result.get('first_name', 'User')}!")
                        time.sleep(1)
                        self.navigate_to('register', 'success')
                    else:
                        st.error(f"Facebook registration failed: {result}")
    
    def render_authenticated_dashboard(self):
        """Render authenticated user dashboard"""
        user_data = st.session_state.user_data
        
        # Header with user info and language selector
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"### 🏠 Welcome back, {user_data.get('first_name', 'User')}!")
        
        with col2:
            self.render_language_selector()
        
        with col3:
            if st.button("🚪 Logout", use_container_width=True):
                self.navigate_to('authenticated', 'logout')
        
        # Navigation menu (only visible after authentication)
        st.markdown("### 🧭 Navigation")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("🏠 Home", use_container_width=True):
                st.rerun()  # Stay on dashboard
        
        with col2:
            if st.button("🔍 Explore", use_container_width=True):
                self.navigate_to('authenticated', 'browse')
        
        with col3:
            if st.button("🔍 Search", use_container_width=True):
                self.navigate_to('authenticated', 'browse')
        
        with col4:
            if st.button("🎯 Campaign", use_container_width=True):
                self.navigate_to('authenticated', 'create')
        
        with col5:
            if st.button("👤 Profile", use_container_width=True):
                st.info("Profile management coming soon!")
        
        # Dashboard content
        st.markdown("---")
        
        # Quick actions
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
                self.navigate_to('authenticated', 'create')
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <h3 style="color: #2e7d32;">🔍 Browse Projects</h3>
                <p style="color: #666;">Discover amazing causes to support</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔍 Browse Now", use_container_width=True, key="browse_campaigns_btn"):
                self.navigate_to('authenticated', 'browse')
        
        with col3:
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <h3 style="color: #2e7d32;">💝 Support Causes</h3>
                <p style="color: #666;">Make a difference today</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("💝 Donate Now", use_container_width=True, key="support_causes_btn"):
                self.navigate_to('authenticated', 'browse')
        
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

def main():
    """Main application entry point"""
    # Configure Streamlit page
    st.set_page_config(
        page_title="HAVEN - Crowdfunding Platform",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for light green theme
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e8 100%);
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
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    
    .stSelectbox > div > div {
        background: white;
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input {
        background: white;
        border-radius: 8px;
    }
    
    .stTextArea > div > div > textarea {
        background: white;
        border-radius: 8px;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
    }
    
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize workflow manager
    workflow_manager = WorkflowManager()
    
    # Check authentication status
    if check_authentication():
        st.session_state.user_authenticated = True
        # If authenticated but on start/login/register page, redirect to dashboard
        if workflow_manager.get_current_state() in ['start', 'login', 'register']:
            workflow_manager.navigate_to(workflow_manager.get_current_state(), 'success')
    else:
        st.session_state.user_authenticated = False
        # If not authenticated but on protected page, redirect to start
        protected_states = ['authenticated', 'create_campaign', 'submit_campaign', 'xai_processing', 
                          'admin_review', 'funding_display', 'discard_project']
        if workflow_manager.get_current_state() in protected_states:
            st.session_state.current_workflow_state = 'start'
    
    # Render current page
    workflow_manager.render_current_page()
    
    # Debug info (remove in production)
    if st.sidebar.checkbox("Debug Mode"):
        st.sidebar.markdown("### Debug Info")
        st.sidebar.markdown(f"**Current State:** {workflow_manager.get_current_state()}")
        st.sidebar.markdown(f"**Authenticated:** {st.session_state.user_authenticated}")
        st.sidebar.markdown(f"**User:** {st.session_state.user_data.get('first_name', 'None')}")
        st.sidebar.markdown(f"**Language:** {st.session_state.selected_language}")

if __name__ == "__main__":
    main()

