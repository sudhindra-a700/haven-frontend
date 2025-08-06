"""

# Import utilities with error handling
try:
    from utils.translation_service import t, format_currency
    from utils.auth_utils import get_current_user
    from utils.api_client import *
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

Registration Page for HAVEN Crowdfunding Platform
Standardized with show() function and improved UI with MaterializeCSS styling
"""

import streamlit as st
import requests
import logging
import re
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def show():
    """
    Render the registration page for new users
    """
    try:
        # Custom CSS for MaterializeCSS-inspired styling
        st.markdown("""
        <style>
        .register-container {
            background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            margin: 2rem auto;
            max-width: 600px;
        }
        .register-header {
            text-align: center;
            color: #2e7d32;
            margin-bottom: 2rem;
        }
        .form-section {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
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
        .strength-meter {
            height: 8px;
            border-radius: 4px;
            margin-top: 5px;
            transition: all 0.3s ease;
        }
        .strength-weak { background: #f44336; }
        .strength-medium { background: #ff9800; }
        .strength-strong { background: #4caf50; }
        </style>
        """, unsafe_allow_html=True)
        
        # Main registration container
        st.markdown("""
        <div class="register-container">
            <div class="register-header">
                <h1>🆕 Join HAVEN</h1>
                <h3>Create Your Account</h3>
                <p>Start your journey of making a positive impact in communities</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Registration form container
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                # Quick OAuth Registration
                st.markdown("### 🚀 Quick Registration")
                
                # Google OAuth Button
                if st.button("🔍 Sign up with Google", key="google_register", use_container_width=True):
                    handle_google_register()
                
                # Facebook OAuth Button  
                if st.button("📘 Sign up with Facebook", key="facebook_register", use_container_width=True):
                    handle_facebook_register()
                
                # Divider
                st.markdown("""
                <div class="divider">
                    <span>or create account manually</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Manual Registration Form
                with st.form("registration_form"):
                    st.markdown("#### 📝 Account Information")
                    
                    # Personal Information
                    col_name1, col_name2 = st.columns(2)
                    with col_name1:
                        first_name = st.text_input(
                            "👤 First Name",
                            placeholder="Enter your first name",
                            help="Your given name"
                        )
                    
                    with col_name2:
                        last_name = st.text_input(
                            "👤 Last Name", 
                            placeholder="Enter your last name",
                            help="Your family name"
                        )
                    
                    # Contact Information
                    email = st.text_input(
                        "📧 Email Address",
                        placeholder="Enter your email address",
                        help="We'll use this for login and important updates"
                    )
                    
                    phone = st.text_input(
                        "📱 Phone Number",
                        placeholder="+91 XXXXX XXXXX",
                        help="For account verification and security"
                    )
                    
                    # Password Section
                    st.markdown("#### 🔒 Security")
                    
                    password = st.text_input(
                        "🔐 Password",
                        type="password",
                        placeholder="Create a strong password",
                        help="Minimum 8 characters with letters, numbers, and symbols"
                    )
                    
                    # Password strength indicator
                    if password:
                        strength = check_password_strength(password)
                        display_password_strength(strength)
                    
                    confirm_password = st.text_input(
                        "🔐 Confirm Password",
                        type="password",
                        placeholder="Re-enter your password",
                        help="Must match the password above"
                    )
                    
                    # Account Type
                    st.markdown("#### 👥 Account Type")
                    account_type = st.selectbox(
                        "Select your account type",
                        ["Individual", "Organization", "NGO", "Government"],
                        help="Choose the type that best describes you"
                    )
                    
                    # Terms and Conditions
                    st.markdown("#### 📋 Terms & Privacy")
                    
                    terms_accepted = st.checkbox(
                        "I agree to the Terms of Service and Privacy Policy",
                        help="Required to create an account"
                    )
                    
                    newsletter_opt_in = st.checkbox(
                        "Send me updates about new campaigns and platform features",
                        value=True,
                        help="Optional - you can unsubscribe anytime"
                    )
                    
                    # Submit button
                    register_submitted = st.form_submit_button(
                        "🎉 Create My Account",
                        use_container_width=True,
                        type="primary"
                    )
                
                # Handle registration submission
                if register_submitted:
                    handle_registration_submission(
                        first_name, last_name, email, phone, password, 
                        confirm_password, account_type, terms_accepted, newsletter_opt_in
                    )
                
                # Login link
                st.markdown("---")
                st.markdown("### 🔐 Already have an account?")
                
                if st.button("🚀 Sign In", key="login_btn", use_container_width=True):
                    st.session_state.current_page = 'login'
                    st.rerun()
        
        # Footer information
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
            <p>🔒 Your information is secure and will never be shared</p>
            <p>📞 Questions? Contact our support team</p>
            <p>© 2025 HAVEN - Empowering Communities Through Crowdfunding</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Error rendering registration page: {e}")
        st.error("Sorry, there was an error loading the registration page. Please try refreshing.")
        st.exception(e)

def check_password_strength(password: str) -> Dict[str, Any]:
    """Check password strength and return score with feedback"""
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("At least 8 characters")
    
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Lowercase letters")
    
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Uppercase letters")
    
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Numbers")
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Special characters")
    
    if score <= 2:
        strength = "weak"
    elif score <= 3:
        strength = "medium"
    else:
        strength = "strong"
    
    return {
        "score": score,
        "strength": strength,
        "feedback": feedback
    }

def display_password_strength(strength_info: Dict[str, Any]):
    """Display password strength indicator"""
    strength = strength_info["strength"]
    score = strength_info["score"]
    feedback = strength_info["feedback"]
    
    # Strength meter
    if strength == "weak":
        st.markdown(f"""
        <div class="strength-meter strength-weak" style="width: {score*20}%"></div>
        <small style="color: #f44336;">Weak password</small>
        """, unsafe_allow_html=True)
    elif strength == "medium":
        st.markdown(f"""
        <div class="strength-meter strength-medium" style="width: {score*20}%"></div>
        <small style="color: #ff9800;">Medium strength</small>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="strength-meter strength-strong" style="width: {score*20}%"></div>
        <small style="color: #4caf50;">Strong password ✓</small>
        """, unsafe_allow_html=True)
    
    # Feedback
    if feedback:
        st.caption(f"Add: {', '.join(feedback)}")

def handle_google_register():
    """Handle Google OAuth registration"""
    try:
        st.info("🔍 Opening Google sign-up window...")
        
        with st.spinner("Creating account with Google..."):
            import time
            time.sleep(2)
            
            # Set authentication state
            st.session_state.authenticated = True
            st.session_state.user = {
                'name': 'Google User',
                'email': 'newuser@gmail.com',
                'provider': 'google',
                'avatar': '👤',
                'account_type': 'Individual'
            }
            st.session_state.current_page = 'home'
            
            st.success("✅ Account created successfully with Google!")
            st.balloons()
            st.rerun()
            
    except Exception as e:
        logger.error(f"Google registration error: {e}")
        st.error("❌ Google sign-up failed. Please try again.")

def handle_facebook_register():
    """Handle Facebook OAuth registration"""
    try:
        st.info("📘 Opening Facebook sign-up window...")
        
        with st.spinner("Creating account with Facebook..."):
            import time
            time.sleep(2)
            
            # Set authentication state
            st.session_state.authenticated = True
            st.session_state.user = {
                'name': 'Facebook User',
                'email': 'newuser@facebook.com',
                'provider': 'facebook',
                'avatar': '👤',
                'account_type': 'Individual'
            }
            st.session_state.current_page = 'home'
            
            st.success("✅ Account created successfully with Facebook!")
            st.balloons()
            st.rerun()
            
    except Exception as e:
        logger.error(f"Facebook registration error: {e}")
        st.error("❌ Facebook sign-up failed. Please try again.")

def handle_registration_submission(first_name, last_name, email, phone, password, 
                                 confirm_password, account_type, terms_accepted, newsletter_opt_in):
    """Handle manual registration form submission"""
    try:
        # Validation
        errors = []
        
        if not first_name or not last_name:
            errors.append("First name and last name are required")
        
        if not email or "@" not in email:
            errors.append("Valid email address is required")
        
        if not phone:
            errors.append("Phone number is required")
        
        if not password or len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if password != confirm_password:
            errors.append("Passwords do not match")
        
        if not terms_accepted:
            errors.append("You must accept the Terms of Service and Privacy Policy")
        
        # Display errors
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
            return
        
        # Process registration
        with st.spinner("Creating your account..."):
            import time
            time.sleep(2)
            
            # In a real implementation, this would call the backend API
            # For demo purposes, simulate successful registration
            
            # Set authentication state
            st.session_state.authenticated = True
            st.session_state.user = {
                'name': f"{first_name} {last_name}",
                'email': email,
                'phone': phone,
                'provider': 'email',
                'avatar': '👤',
                'account_type': account_type,
                'newsletter_opt_in': newsletter_opt_in
            }
            st.session_state.current_page = 'home'
            
            st.success(f"🎉 Welcome to HAVEN, {first_name}!")
            st.balloons()
            
            # Show welcome message
            st.info("""
            ### 🎊 Account Created Successfully!
            
            Your HAVEN account has been created. You can now:
            - 🎯 Create and manage crowdfunding campaigns
            - 🔍 Discover and support amazing causes
            - 💝 Make secure donations to projects you care about
            - 📊 Track your impact and contributions
            
            Welcome to the HAVEN community!
            """)
            
            time.sleep(3)
            st.rerun()
            
    except Exception as e:
        logger.error(f"Registration error: {e}")
        st.error("❌ Registration failed. Please try again.")

# Legacy function support
def render_register_page(api_client=None):
    """Legacy function name support - redirects to show()"""
    show()

