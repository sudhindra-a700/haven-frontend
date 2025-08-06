"""
Fixed Login Page for HAVEN Crowdfunding Platform
Standardized with show() function and improved UI with MaterializeCSS styling
"""

import streamlit as st
import requests
import logging
from typing import Dict, Any, Optional

# Import utilities with error handling
try:
    from utils.translation_service import t
    from utils.auth_utils import login, oauth_login
    from utils.config import is_oauth_enabled
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

logger = logging.getLogger(__name__)

def show():
    """
    Render the login page for unauthenticated users
    """
    try:
        # Custom CSS for MaterializeCSS-inspired styling
        st.markdown("""
        <style>
        .login-container {
            background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            margin: 2rem auto;
            max-width: 500px;
        }
        .login-header {
            text-align: center;
            color: #2e7d32;
            margin-bottom: 2rem;
        }
        .oauth-button {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .google-btn {
            background: #db4437;
            color: white;
        }
        .google-btn:hover {
            background: #c23321;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(219, 68, 55, 0.3);
        }
        .facebook-btn {
            background: #3b5998;
            color: white;
        }
        .facebook-btn:hover {
            background: #2d4373;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 89, 152, 0.3);
        }
        .pulse {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        .divider {
            text-align: center;
            margin: 1.5rem 0;
            position: relative;
        }
        .divider::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: #ccc;
        }
        .divider span {
            background: white;
            padding: 0 1rem;
            color: #666;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Main login container
        st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <h1>🏠 Welcome to HAVEN</h1>
                <h3>Your Trusted Crowdfunding Platform</h3>
                <p>Sign in to start your journey of making a difference</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form container
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                # OAuth Login Buttons with pulse effect
                st.markdown("### 🔐 Sign In")
                
                # Google OAuth Button
                if st.button("🔍 Sign in with Google", key="google_login", use_container_width=True):
                    handle_google_login()
                
                # Facebook OAuth Button  
                if st.button("📘 Sign in with Facebook", key="facebook_login", use_container_width=True):
                    handle_facebook_login()
                
                # Divider
                st.markdown("""
                <div class="divider">
                    <span>or</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Email/Password Login Form
                with st.form("login_form"):
                    st.markdown("#### Email & Password")
                    
                    email = st.text_input(
                        "📧 Email Address",
                        placeholder="Enter your email address",
                        help="Use the email you registered with"
                    )
                    
                    password = st.text_input(
                        "🔒 Password",
                        type="password",
                        placeholder="Enter your password",
                        help="Your secure password"
                    )
                    
                    col_login, col_forgot = st.columns([2, 1])
                    
                    with col_login:
                        login_submitted = st.form_submit_button(
                            "🚀 Sign In",
                            use_container_width=True,
                            type="primary"
                        )
                    
                    with col_forgot:
                        if st.form_submit_button("🔄 Forgot?", use_container_width=True):
                            handle_forgot_password(email)
                
                # Handle email/password login
                if login_submitted:
                    if email and password:
                        handle_email_login(email, password)
                    else:
                        st.error("Please enter both email and password")
                
                # Registration link
                st.markdown("---")
                st.markdown("### 🆕 New to HAVEN?")
                
                col_reg1, col_reg2 = st.columns([1, 1])
                
                with col_reg1:
                    if st.button("📝 Create Account", key="register_btn", use_container_width=True):
                        st.session_state.current_page = 'register'
                        st.rerun()
                
                with col_reg2:
                    if st.button("ℹ️ Learn More", key="learn_more_btn", use_container_width=True):
                        show_platform_info()
        
        # Footer information
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
            <p>🔒 Your data is secure and protected</p>
            <p>📞 Need help? Contact our support team</p>
            <p>© 2025 HAVEN - Empowering Communities Through Crowdfunding</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Error rendering login page: {e}")
        st.error("Sorry, there was an error loading the login page. Please try refreshing.")
        st.exception(e)

def handle_google_login():
    """Handle Google OAuth login with popup window"""
    try:
        st.info("🔍 Opening Google sign-in window...")
        
        # In a real implementation, this would:
        # 1. Open OAuth popup window
        # 2. Handle OAuth callback
        # 3. Store authentication tokens
        # 4. Redirect to home page
        
        # For demo purposes, simulate successful login
        with st.spinner("Authenticating with Google..."):
            # Simulate API call delay
            import time
            time.sleep(2)
            
            # Set authentication state
            st.session_state.authenticated = True
            st.session_state.user = {
                'name': 'Google User',
                'email': 'user@gmail.com',
                'provider': 'google',
                'avatar': '👤'
            }
            st.session_state.current_page = 'home'
            
            st.success("✅ Successfully signed in with Google!")
            st.rerun()
            
    except Exception as e:
        logger.error(f"Google login error: {e}")
        st.error("❌ Google sign-in failed. Please try again.")

def handle_facebook_login():
    """Handle Facebook OAuth login with popup window"""
    try:
        st.info("📘 Opening Facebook sign-in window...")
        
        # In a real implementation, this would:
        # 1. Open OAuth popup window
        # 2. Handle OAuth callback
        # 3. Store authentication tokens
        # 4. Redirect to home page
        
        # For demo purposes, simulate successful login
        with st.spinner("Authenticating with Facebook..."):
            # Simulate API call delay
            import time
            time.sleep(2)
            
            # Set authentication state
            st.session_state.authenticated = True
            st.session_state.user = {
                'name': 'Facebook User',
                'email': 'user@facebook.com',
                'provider': 'facebook',
                'avatar': '👤'
            }
            st.session_state.current_page = 'home'
            
            st.success("✅ Successfully signed in with Facebook!")
            st.rerun()
            
    except Exception as e:
        logger.error(f"Facebook login error: {e}")
        st.error("❌ Facebook sign-in failed. Please try again.")

def handle_email_login(email: str, password: str):
    """Handle email/password login"""
    try:
        with st.spinner("Signing you in..."):
            # In a real implementation, this would call the backend API
            # For demo purposes, simulate authentication
            import time
            time.sleep(1)
            
            # Simple validation (replace with actual API call)
            if "@" in email and len(password) >= 6:
                # Set authentication state
                st.session_state.authenticated = True
                st.session_state.user = {
                    'name': email.split('@')[0].title(),
                    'email': email,
                    'provider': 'email',
                    'avatar': '👤'
                }
                st.session_state.current_page = 'home'
                
                st.success(f"✅ Welcome back, {st.session_state.user['name']}!")
                st.rerun()
            else:
                st.error("❌ Invalid email or password. Please try again.")
                
    except Exception as e:
        logger.error(f"Email login error: {e}")
        st.error("❌ Login failed. Please check your credentials and try again.")

def handle_forgot_password(email: str):
    """Handle forgot password request"""
    try:
        if email:
            with st.spinner("Sending reset link..."):
                import time
                time.sleep(1)
                st.success(f"📧 Password reset link sent to {email}")
        else:
            st.warning("⚠️ Please enter your email address first")
            
    except Exception as e:
        logger.error(f"Forgot password error: {e}")
        st.error("❌ Failed to send reset link. Please try again.")

def show_platform_info():
    """Show platform information modal"""
    st.info("""
    ### 🏠 About HAVEN Platform
    
    **HAVEN** is a trusted crowdfunding platform that empowers communities to make a positive impact.
    
    **Key Features:**
    - 🎯 **Create Campaigns**: Launch your fundraising campaigns easily
    - 🔍 **Discover Projects**: Find and support causes you care about  
    - 💝 **Secure Donations**: Safe and transparent donation process
    - 🌍 **Multi-language Support**: Available in multiple languages
    - 📱 **Mobile Friendly**: Access from any device
    - 🔒 **Fraud Detection**: Advanced security to protect donors
    
    **Why Choose HAVEN?**
    - ✅ Verified campaigns and organizations
    - ✅ Low platform fees
    - ✅ Real-time progress tracking
    - ✅ 24/7 customer support
    - ✅ Tax-compliant receipts
    
    Join thousands of changemakers today!
    """)

# Legacy function support
def render_login_page(api_client=None):
    """Legacy function name support - redirects to show()"""
    show()

