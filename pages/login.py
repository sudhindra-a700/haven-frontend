"""
Login Page for HAVEN Crowdfunding Platform
"""

import streamlit as st
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def render_login_page(api_client, auth_utils):
    """Render the login page"""
    try:
        # Check if user is already authenticated
        if st.session_state.get('authenticated'):
            st.success("You are already logged in!")
            if st.button("Go to Dashboard"):
                st.session_state.current_page = 'dashboard'
                st.experimental_rerun()
            return
        
        # Page header
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="color: #667eea;">🔐 Login to HAVEN</h1>
            <p style="color: #666; font-size: 1.1rem;">
                Welcome back! Sign in to continue your crowdfunding journey.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for different login methods
        tab1, tab2 = st.tabs(["📧 Email Login", "🔗 Social Login"])
        
        with tab1:
            render_email_login(api_client, auth_utils)
        
        with tab2:
            render_social_login(auth_utils)
        
        # Additional options
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 Don't have an account? Register", use_container_width=True):
                st.session_state.current_page = 'register'
                st.experimental_rerun()
        
        with col2:
            if st.button("🔑 Forgot Password?", use_container_width=True):
                st.session_state.current_page = 'forgot_password'
                st.experimental_rerun()
    
    except Exception as e:
        logger.error(f"Error rendering login page: {e}")
        st.error("Unable to load login page. Please refresh and try again.")

def render_email_login(api_client, auth_utils):
    """Render email/password login form"""
    with st.form("login_form", clear_on_submit=False):
        st.markdown("### Sign in with Email")
        
        email = st.text_input(
            "Email Address",
            placeholder="Enter your email address",
            help="The email address you used to register"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            help="Your account password"
        )
        
        remember_me = st.checkbox("Remember me", value=True)
        
        submitted = st.form_submit_button("🔐 Sign In", use_container_width=True)
        
        if submitted:
            if not email or not password:
                st.error("Please enter both email and password.")
                return
            
            # Validate email format
            is_valid_email, email_message = auth_utils.validate_email(email)
            if not is_valid_email:
                st.error(email_message)
                return
            
            try:
                with st.spinner("Signing you in..."):
                    success = auth_utils.login_with_credentials(email, password)
                
                if success:
                    st.success("Login successful! Redirecting...")
                    
                    # Store remember me preference
                    if remember_me:
                        st.session_state.remember_login = True
                    
                    # Redirect to dashboard or intended page
                    intended_page = st.session_state.get('intended_page', 'dashboard')
                    st.session_state.current_page = intended_page
                    
                    # Clear intended page
                    if 'intended_page' in st.session_state:
                        del st.session_state.intended_page
                    
                    st.experimental_rerun()
                else:
                    st.error("Login failed. Please check your credentials and try again.")
            
            except Exception as e:
                error_message = str(e)
                if "401" in error_message or "unauthorized" in error_message.lower():
                    st.error("Invalid email or password. Please try again.")
                elif "403" in error_message or "forbidden" in error_message.lower():
                    st.error("Your account has been suspended. Please contact support.")
                elif "429" in error_message or "rate limit" in error_message.lower():
                    st.error("Too many login attempts. Please wait a few minutes and try again.")
                else:
                    st.error(f"Login failed: {error_message}")
                
                logger.error(f"Login error for {email}: {e}")

def render_social_login(auth_utils):
    """Render social login options"""
    st.markdown("### Sign in with Social Media")
    
    # Check if OAuth is enabled
    from utils.config import config_manager
    
    if not config_manager.is_oauth_enabled():
        st.info("Social login is currently disabled. Please use email login.")
        return
    
    oauth_config = config_manager.get_oauth_config()
    
    # Google OAuth
    if oauth_config.get('google_client_id'):
        if st.button("🔍 Continue with Google", key="google_login", use_container_width=True):
            try:
                with st.spinner("Redirecting to Google..."):
                    auth_url = auth_utils.handle_oauth_login('google')
                
                # Create popup window for OAuth
                st.markdown(f"""
                <script>
                window.open('{auth_url}', 'google_oauth', 'width=500,height=600,scrollbars=yes,resizable=yes');
                </script>
                """, unsafe_allow_html=True)
                
                st.info("A popup window has opened for Google login. Please complete the authentication there.")
                
            except Exception as e:
                st.error(f"Google login failed: {e}")
                logger.error(f"Google OAuth error: {e}")
    
    # Facebook OAuth
    if oauth_config.get('facebook_app_id'):
        if st.button("📘 Continue with Facebook", key="facebook_login", use_container_width=True):
            try:
                with st.spinner("Redirecting to Facebook..."):
                    auth_url = auth_utils.handle_oauth_login('facebook')
                
                # Create popup window for OAuth
                st.markdown(f"""
                <script>
                window.open('{auth_url}', 'facebook_oauth', 'width=500,height=600,scrollbars=yes,resizable=yes');
                </script>
                """, unsafe_allow_html=True)
                
                st.info("A popup window has opened for Facebook login. Please complete the authentication there.")
                
            except Exception as e:
                st.error(f"Facebook login failed: {e}")
                logger.error(f"Facebook OAuth error: {e}")
    
    if not oauth_config.get('google_client_id') and not oauth_config.get('facebook_app_id'):
        st.info("Social login options are not configured. Please use email login.")

def render_forgot_password_page(api_client):
    """Render forgot password page"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #667eea;">🔑 Reset Password</h1>
        <p style="color: #666; font-size: 1.1rem;">
            Enter your email address and we'll send you a reset link.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("forgot_password_form"):
        email = st.text_input(
            "Email Address",
            placeholder="Enter your registered email address"
        )
        
        submitted = st.form_submit_button("📧 Send Reset Link", use_container_width=True)
        
        if submitted:
            if not email:
                st.error("Please enter your email address.")
                return
            
            try:
                # TODO: Implement forgot password API call
                st.success(f"If an account with email {email} exists, you will receive a password reset link shortly.")
                
            except Exception as e:
                st.error(f"Failed to send reset link: {e}")
    
    if st.button("← Back to Login"):
        st.session_state.current_page = 'login'
        st.experimental_rerun()

def render_login_status():
    """Render login status component"""
    if st.session_state.get('authenticated'):
        user = st.session_state.get('user', {})
        
        with st.expander("👤 Account Info", expanded=False):
            st.write(f"**Name:** {user.get('full_name', 'N/A')}")
            st.write(f"**Email:** {user.get('email', 'N/A')}")
            st.write(f"**Role:** {user.get('role', 'user').title()}")
            st.write(f"**Verified:** {'✅' if user.get('is_verified') else '❌'}")
            
            if st.button("🚪 Logout"):
                from utils.auth_utils import AuthUtils
                auth_utils = AuthUtils(None)  # API client not needed for logout
                auth_utils.logout_user()
                st.experimental_rerun()

def handle_oauth_callback():
    """Handle OAuth callback from URL parameters"""
    query_params = st.experimental_get_query_params()
    
    if 'code' in query_params and 'state' in query_params:
        try:
            # Extract OAuth parameters
            code = query_params['code'][0]
            state = query_params['state'][0]
            
            # TODO: Exchange code for tokens via backend API
            st.success("OAuth login successful!")
            
            # Clear URL parameters
            st.experimental_set_query_params()
            
            # Redirect to dashboard
            st.session_state.current_page = 'dashboard'
            st.experimental_rerun()
            
        except Exception as e:
            st.error(f"OAuth login failed: {e}")
            logger.error(f"OAuth callback error: {e}")
    
    elif 'error' in query_params:
        error = query_params['error'][0]
        error_description = query_params.get('error_description', ['Unknown error'])[0]
        
        st.error(f"OAuth login failed: {error_description}")
        
        # Clear URL parameters
        st.experimental_set_query_params()

def check_session_expiry():
    """Check if user session has expired"""
    if st.session_state.get('authenticated'):
        from utils.auth_utils import AuthUtils
        from utils.api_client import APIClient
        from utils.config import config_manager
        
        api_client = APIClient(config_manager.get_backend_url())
        auth_utils = AuthUtils(api_client)
        
        if not auth_utils.check_authentication():
            st.warning("Your session has expired. Please login again.")
            st.session_state.current_page = 'login'
            st.experimental_rerun()

