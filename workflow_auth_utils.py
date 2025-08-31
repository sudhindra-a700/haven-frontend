# Modified workflow_auth_utils.py - Authentication Workflow with Bootstrap Icons
# This file replaces your existing workflow_auth_utils.py

import streamlit as st
from utils.icon_utils import display_icon, get_icon_html
from config.icon_mapping import get_icon, ICON_COLORS, ICON_SIZES

def render_login_page():
    """Render login page with Bootstrap icons."""
    # Page header with icon
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        {get_icon_html('shield-lock-fill', 48, ICON_COLORS['primary'])}
        <h1 style="color: {ICON_COLORS['primary']}; margin-top: 15px;">
            Welcome to Haven
        </h1>
        <p style="color: {ICON_COLORS['muted']};">Sign in to your account</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form with icons
    with st.form("login_form"):
        # Email field with icon
        col1, col2 = st.columns([1, 10])
        with col1:
            st.markdown(f"""
            <div style="padding-top: 8px;">
                {get_icon_html('envelope-fill', ICON_SIZES['md'], ICON_COLORS['muted'])}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            email = st.text_input("Email Address", placeholder="Enter your email")
        
        # Password field with icon
        col1, col2 = st.columns([1, 10])
        with col1:
            st.markdown(f"""
            <div style="padding-top: 8px;">
                {get_icon_html('key-fill', ICON_SIZES['md'], ICON_COLORS['muted'])}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        # Remember me checkbox with icon
        col1, col2 = st.columns([1, 10])
        with col1:
            st.markdown(f"""
            <div style="padding-top: 8px;">
                {get_icon_html('check-square', ICON_SIZES['sm'], ICON_COLORS['muted'])}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            remember_me = st.checkbox("Remember me")
        
        # Login button with icon
        if st.form_submit_button(f"{get_icon_html('box-arrow-in-right', ICON_SIZES['sm'])} Sign In"):
            if authenticate_user(email, password):
                st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} Login successful!")
                return True
            else:
                st.error(f"{get_icon_html('x-circle-fill', ICON_SIZES['sm'], ICON_COLORS['danger'])} Invalid credentials")
                return False
    
    # Social login options
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center;">
        <p style="color: {ICON_COLORS['muted']};">Or sign in with</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button(f"{get_icon_html('google', ICON_SIZES['sm'])} Google", key="google_login"):
            st.info("Google OAuth integration")
    with col2:
        if st.button(f"{get_icon_html('facebook', ICON_SIZES['sm'])} Facebook", key="facebook_login"):
            st.info("Facebook OAuth integration")
    with col3:
        if st.button(f"{get_icon_html('github', ICON_SIZES['sm'])} GitHub", key="github_login"):
            st.info("GitHub OAuth integration")
    
    # Registration link
    st.markdown(f"""
    <div style="text-align: center; margin-top: 30px;">
        <p>Don't have an account? 
        <a href="#" style="color: {ICON_COLORS['primary']};">
            {get_icon_html('person-plus', ICON_SIZES['sm'])} Create one here
        </a></p>
    </div>
    """, unsafe_allow_html=True)
    
    return False

def render_registration_page():
    """Render registration page with Bootstrap icons."""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        {get_icon_html('person-plus-fill', 48, ICON_COLORS['primary'])}
        <h1 style="color: {ICON_COLORS['primary']}; margin-top: 15px;">
            Join Haven
        </h1>
        <p style="color: {ICON_COLORS['muted']};">Create your crowdfunding account</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("registration_form"):
        # Personal information section
        st.markdown(f"""
        <h3>{get_icon_html('person-vcard', ICON_SIZES['lg'])} Personal Information</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input(f"{get_icon_html('person', ICON_SIZES['sm'])} First Name")
        with col2:
            last_name = st.text_input(f"{get_icon_html('person', ICON_SIZES['sm'])} Last Name")
        
        email = st.text_input(f"{get_icon_html('envelope', ICON_SIZES['sm'])} Email Address")
        phone = st.text_input(f"{get_icon_html('telephone', ICON_SIZES['sm'])} Phone Number")
        
        # Account security section
        st.markdown(f"""
        <h3>{get_icon_html('shield-check', ICON_SIZES['lg'])} Account Security</h3>
        """, unsafe_allow_html=True)
        
        password = st.text_input(f"{get_icon_html('key', ICON_SIZES['sm'])} Password", type="password")
        confirm_password = st.text_input(f"{get_icon_html('key-fill', ICON_SIZES['sm'])} Confirm Password", type="password")
        
        # Terms and conditions
        terms_accepted = st.checkbox(f"{get_icon_html('file-text', ICON_SIZES['sm'])} I agree to the Terms and Conditions")
        newsletter = st.checkbox(f"{get_icon_html('envelope-heart', ICON_SIZES['sm'])} Subscribe to newsletter")
        
        if st.form_submit_button(f"{get_icon_html('person-plus', ICON_SIZES['sm'])} Create Account"):
            if validate_registration_data(first_name, last_name, email, password, confirm_password, terms_accepted):
                st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} Account created successfully!")
                return True
            else:
                st.error(f"{get_icon_html('exclamation-triangle', ICON_SIZES['sm'], ICON_COLORS['warning'])} Please check your information")
                return False
    
    return False

def render_forgot_password_page():
    """Render forgot password page with Bootstrap icons."""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        {get_icon_html('key-fill', 48, ICON_COLORS['warning'])}
        <h1 style="color: {ICON_COLORS['warning']}; margin-top: 15px;">
            Reset Password
        </h1>
        <p style="color: {ICON_COLORS['muted']};">Enter your email to receive reset instructions</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("forgot_password_form"):
        col1, col2 = st.columns([1, 10])
        with col1:
            st.markdown(f"""
            <div style="padding-top: 8px;">
                {get_icon_html('envelope', ICON_SIZES['md'], ICON_COLORS['muted'])}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            email = st.text_input("Email Address", placeholder="Enter your registered email")
        
        if st.form_submit_button(f"{get_icon_html('send', ICON_SIZES['sm'])} Send Reset Link"):
            if email:
                st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} Reset link sent to {email}")
                return True
            else:
                st.error(f"{get_icon_html('exclamation-triangle', ICON_SIZES['sm'], ICON_COLORS['warning'])} Please enter your email address")
    
    return False

def render_user_profile_settings():
    """Render user profile settings with Bootstrap icons."""
    st.markdown(f"""
    <h1>{get_icon_html('person-gear', 32, ICON_COLORS['primary'])} Profile Settings</h1>
    """, unsafe_allow_html=True)
    
    # Profile tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        f"{get_icon_html('person', ICON_SIZES['sm'])} Personal Info",
        f"{get_icon_html('shield-check', ICON_SIZES['sm'])} Security", 
        f"{get_icon_html('bell', ICON_SIZES['sm'])} Notifications",
        f"{get_icon_html('credit-card', ICON_SIZES['sm'])} Payment"
    ])
    
    with tab1:
        render_personal_info_tab()
    
    with tab2:
        render_security_tab()
    
    with tab3:
        render_notifications_tab()
    
    with tab4:
        render_payment_tab()

def render_personal_info_tab():
    """Render personal information tab."""
    st.markdown(f"""
    <h3>{get_icon_html('person-vcard-fill', ICON_SIZES['lg'])} Personal Information</h3>
    """, unsafe_allow_html=True)
    
    with st.form("personal_info_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", value="John")
            email = st.text_input("Email", value="john@example.com")
        with col2:
            last_name = st.text_input("Last Name", value="Doe")
            phone = st.text_input("Phone", value="+1234567890")
        
        bio = st.text_area("Bio", value="Passionate about innovative projects...")
        location = st.text_input(f"{get_icon_html('geo-alt', ICON_SIZES['sm'])} Location", value="San Francisco, CA")
        
        if st.form_submit_button(f"{get_icon_html('floppy', ICON_SIZES['sm'])} Save Changes"):
            st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} Profile updated successfully!")

def render_security_tab():
    """Render security settings tab."""
    st.markdown(f"""
    <h3>{get_icon_html('shield-lock-fill', ICON_SIZES['lg'])} Security Settings</h3>
    """, unsafe_allow_html=True)
    
    # Change password section
    st.markdown(f"""
    <h4>{get_icon_html('key', ICON_SIZES['md'])} Change Password</h4>
    """, unsafe_allow_html=True)
    
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_new_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button(f"{get_icon_html('shield-check', ICON_SIZES['sm'])} Update Password"):
            st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} Password updated successfully!")
    
    # Two-factor authentication
    st.markdown(f"""
    <h4>{get_icon_html('phone', ICON_SIZES['md'])} Two-Factor Authentication</h4>
    """, unsafe_allow_html=True)
    
    two_fa_enabled = st.checkbox(f"{get_icon_html('shield-fill-check', ICON_SIZES['sm'])} Enable 2FA", value=False)
    
    if two_fa_enabled:
        st.info(f"{get_icon_html('info-circle', ICON_SIZES['sm'])} 2FA setup instructions will be sent to your phone")

def render_notifications_tab():
    """Render notifications settings tab."""
    st.markdown(f"""
    <h3>{get_icon_html('bell-fill', ICON_SIZES['lg'])} Notification Preferences</h3>
    """, unsafe_allow_html=True)
    
    # Email notifications
    st.markdown(f"""
    <h4>{get_icon_html('envelope', ICON_SIZES['md'])} Email Notifications</h4>
    """, unsafe_allow_html=True)
    
    email_campaign_updates = st.checkbox(f"{get_icon_html('megaphone', ICON_SIZES['sm'])} Campaign updates", value=True)
    email_new_campaigns = st.checkbox(f"{get_icon_html('plus-circle', ICON_SIZES['sm'])} New campaigns in your interests", value=True)
    email_funding_milestones = st.checkbox(f"{get_icon_html('trophy', ICON_SIZES['sm'])} Funding milestones", value=True)
    email_newsletter = st.checkbox(f"{get_icon_html('newspaper', ICON_SIZES['sm'])} Weekly newsletter", value=False)
    
    # Push notifications
    st.markdown(f"""
    <h4>{get_icon_html('phone', ICON_SIZES['md'])} Push Notifications</h4>
    """, unsafe_allow_html=True)
    
    push_messages = st.checkbox(f"{get_icon_html('chat-dots', ICON_SIZES['sm'])} Direct messages", value=True)
    push_campaign_alerts = st.checkbox(f"{get_icon_html('exclamation-triangle', ICON_SIZES['sm'])} Campaign alerts", value=True)
    
    if st.button(f"{get_icon_html('floppy', ICON_SIZES['sm'])} Save Notification Settings"):
        st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} Notification preferences saved!")

def render_payment_tab():
    """Render payment settings tab."""
    st.markdown(f"""
    <h3>{get_icon_html('credit-card-fill', ICON_SIZES['lg'])} Payment Methods</h3>
    """, unsafe_allow_html=True)
    
    # Existing payment methods
    payment_methods = [
        {"type": "credit_card", "name": "Visa ending in 4242", "icon": "credit-card", "primary": True},
        {"type": "bank", "name": "Chase Bank Account", "icon": "bank", "primary": False},
        {"type": "paypal", "name": "PayPal Account", "icon": "paypal", "primary": False}
    ]
    
    for method in payment_methods:
        primary_badge = f"""
        <span style="background: {ICON_COLORS['success']}; color: white; padding: 2px 8px; 
                     border-radius: 12px; font-size: 12px; margin-left: 10px;">
            {get_icon_html('star-fill', 12)} Primary
        </span>
        """ if method['primary'] else ""
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; 
                    padding: 15px; margin: 10px 0; background: white; border-radius: 10px; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center;">
                {get_icon_html(method['icon'], 24, ICON_COLORS['primary'])}
                <span style="margin-left: 15px; font-weight: 500;">{method['name']}</span>
                {primary_badge}
            </div>
            <div>
                <button style="background: none; border: 1px solid {ICON_COLORS['muted']}; 
                               color: {ICON_COLORS['muted']}; padding: 5px 10px; border-radius: 5px; 
                               margin-right: 5px; cursor: pointer;">
                    {get_icon_html('pencil', 14)} Edit
                </button>
                <button style="background: none; border: 1px solid {ICON_COLORS['danger']}; 
                               color: {ICON_COLORS['danger']}; padding: 5px 10px; border-radius: 5px; 
                               cursor: pointer;">
                    {get_icon_html('trash', 14)} Remove
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add new payment method
    if st.button(f"{get_icon_html('plus-circle', ICON_SIZES['sm'])} Add Payment Method", key="add_payment"):
        st.info("Opening payment method setup...")

# Helper functions (add your existing authentication logic here)
def authenticate_user(email: str, password: str) -> bool:
    """Authenticate user credentials."""
    # Add your existing authentication logic here
    # This is a placeholder
    return email and password and len(password) >= 6

def validate_registration_data(first_name: str, last_name: str, email: str, 
                             password: str, confirm_password: str, terms_accepted: bool) -> bool:
    """Validate registration form data."""
    # Add your existing validation logic here
    # This is a placeholder
    return (first_name and last_name and email and password and 
            password == confirm_password and terms_accepted and len(password) >= 6)

# Main authentication workflow function
def run_authentication_workflow():
    """Main function to run authentication workflow."""
    if 'auth_page' not in st.session_state:
        st.session_state.auth_page = 'login'
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(f"{get_icon_html('box-arrow-in-right', ICON_SIZES['sm'])} Login"):
            st.session_state.auth_page = 'login'
    with col2:
        if st.button(f"{get_icon_html('person-plus', ICON_SIZES['sm'])} Register"):
            st.session_state.auth_page = 'register'
    with col3:
        if st.button(f"{get_icon_html('key', ICON_SIZES['sm'])} Forgot Password"):
            st.session_state.auth_page = 'forgot'
    
    # Render appropriate page
    if st.session_state.auth_page == 'login':
        return render_login_page()
    elif st.session_state.auth_page == 'register':
        return render_registration_page()
    elif st.session_state.auth_page == 'forgot':
        return render_forgot_password_page()
    
    return False

