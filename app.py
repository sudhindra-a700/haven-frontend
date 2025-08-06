"""
HAVEN Crowdfunding Platform - Completely Clean Version
No HTML markup - Pure Streamlit components only
"""

import streamlit as st
import requests
import time
import uuid
from datetime import datetime, timedelta

# ============================================================================
# AUTHENTICATION UTILITIES
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    if 'show_login_form' not in st.session_state:
        st.session_state.show_login_form = False

def login_user(email, password):
    """Simple login function"""
    if email and password:
        # Demo login - always works for testing
        user_data = {
            'id': 'demo_user',
            'email': email,
            'name': email.split('@')[0],
            'verified': True,
            'account_type': 'individual'
        }
        
        st.session_state.authenticated = True
        st.session_state.user_data = user_data
        return True, user_data
    
    return False, "Please enter both email and password"

def register_user(user_data):
    """Simple registration function"""
    # Demo registration - always works for testing
    demo_user = {
        'id': f'user_{int(time.time())}',
        'email': user_data['email'],
        'name': user_data.get('full_name', user_data.get('org_name', 'User')),
        'account_type': user_data.get('account_type', 'individual'),
        'verified': False,
        'verification_status': 'pending'
    }
    
    st.session_state.authenticated = True
    st.session_state.user_data = demo_user
    return True, demo_user

def logout_user():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.user_data = {}
    st.session_state.current_page = 'login'

# ============================================================================
# NAVIGATION UTILITIES
# ============================================================================

def render_sidebar_navigation():
    """Render sidebar navigation"""
    st.sidebar.title("🧭 Navigation")
    
    current_page = st.session_state.get('current_page', 'home')
    
    # Navigation buttons
    if current_page == 'home':
        st.sidebar.success("🏠 Home (Current)")
    else:
        if st.sidebar.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()
    
    if current_page == 'campaign':
        st.sidebar.success("🎯 Campaign (Current)")
    else:
        if st.sidebar.button("🎯 Campaign", use_container_width=True):
            st.session_state.current_page = 'campaign'
            st.rerun()
    
    if current_page == 'explore':
        st.sidebar.success("🔍 Explore (Current)")
    else:
        if st.sidebar.button("🔍 Explore", use_container_width=True):
            st.session_state.current_page = 'explore'
            st.rerun()
    
    if current_page == 'search':
        st.sidebar.success("🔎 Search (Current)")
    else:
        if st.sidebar.button("🔎 Search", use_container_width=True):
            st.session_state.current_page = 'search'
            st.rerun()
    
    if current_page == 'profile':
        st.sidebar.success("👤 Profile (Current)")
    else:
        if st.sidebar.button("👤 Profile", use_container_width=True):
            st.session_state.current_page = 'profile'
            st.rerun()

# ============================================================================
# PAGE FUNCTIONS
# ============================================================================

def show_login():
    """Show login page - completely clean version"""
    # Simple header
    st.title("🏠 Welcome to HAVEN")
    st.subheader("Your Trusted Crowdfunding Platform")
    st.write("*Empowering communities to support causes that matter*")
    
    st.divider()
    
    # Language selector
    st.subheader("🌐 Language")
    language = st.selectbox(
        "Select Language",
        ["English", "हिंदी", "தமிழ்", "తెలుగు"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Get Started section
    st.subheader("🔐 Get Started")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### 🔑 Existing User")
        st.write("*Already have an account?*")
        
        if st.button("Sign In", use_container_width=True, key="existing_user"):
            st.session_state.show_login_form = True
            st.rerun()
    
    with col2:
        st.write("#### 👤 New User")
        st.write("*Create your account*")
        
        if st.button("Create Account", use_container_width=True, key="new_user"):
            st.session_state.current_page = 'register'
            st.rerun()
    
    # Show login form if "Existing User" was clicked
    if st.session_state.get('show_login_form', False):
        st.divider()
        st.subheader("🔑 Sign In to HAVEN")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Continue", use_container_width=True):
                    if email and password:
                        success, result = login_user(email, password)
                        
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
        
        st.write("#### Or continue with:")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔵 Google", use_container_width=True, key="google_login"):
                demo_user = {
                    'id': 'google_demo',
                    'email': 'demo@google.com',
                    'name': 'Google User',
                    'verified': True
                }
                st.session_state.authenticated = True
                st.session_state.user_data = demo_user
                st.success("Welcome, Google User!")
                time.sleep(1)
                st.session_state.current_page = 'home'
                st.session_state.show_login_form = False
                st.rerun()
        
        with col2:
            if st.button("🔵 Facebook", use_container_width=True, key="facebook_login"):
                demo_user = {
                    'id': 'facebook_demo',
                    'email': 'demo@facebook.com',
                    'name': 'Facebook User',
                    'verified': True
                }
                st.session_state.authenticated = True
                st.session_state.user_data = demo_user
                st.success("Welcome, Facebook User!")
                time.sleep(1)
                st.session_state.current_page = 'home'
                st.session_state.show_login_form = False
                st.rerun()
        
        if st.button("⬅️ Back to Get Started", key="back_to_start"):
            st.session_state.show_login_form = False
            st.rerun()

def show_register():
    """Show registration page - completely clean version"""
    st.title("🏠 HAVEN Registration")
    st.subheader("Help not just some people, but Help Humanity")
    
    st.divider()
    
    st.subheader("Register for HAVEN")
    
    # Account type selection
    account_type = st.selectbox("Account Type", ["Individual", "Organization"])
    
    if account_type == "Individual":
        # Individual Registration Form
        with st.form("individual_register"):
            st.write("### 👤 Individual Account Registration")
            
            # Basic Information
            st.write("#### 📝 Basic Information")
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
            st.write("#### 📄 Document Verification")
            st.warning("🛡️ Identity Verification Required - To ensure platform security and prevent fraud, we require valid government-issued identity documents.")
            
            # PAN Card Upload
            st.write("**📄 PAN Card** *")
            st.caption("Upload a clear image or PDF of your PAN card. Ensure all details are visible and readable.")
            pan_card = st.file_uploader(
                "Upload PAN Card",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                key="pan_card_upload"
            )
            
            # Aadhaar Card Upload
            st.write("**📄 Aadhaar Card** *")
            st.caption("Upload a clear image or PDF of your Aadhaar card. You may mask the Aadhaar number for privacy.")
            aadhaar_card = st.file_uploader(
                "Upload Aadhaar Card",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                key="aadhaar_card_upload"
            )
            
            # Optional Documents
            st.write("#### 📋 Additional Documents (Optional)")
            
            # Bank Statement
            st.write("**📄 Bank Statement**")
            st.caption("Upload recent bank statement (last 3 months) for enhanced verification.")
            bank_statement = st.file_uploader(
                "Upload Bank Statement",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                key="bank_statement_upload"
            )
            
            # Address Proof
            st.write("**📄 Address Proof**")
            st.caption("Upload utility bill, rental agreement, or other address proof document.")
            address_proof = st.file_uploader(
                "Upload Address Proof",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                key="address_proof_upload"
            )
            
            # Terms and conditions
            st.write("#### ✅ Terms & Conditions")
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
                            'newsletter': newsletter
                        }
                        
                        success, result = register_user(user_data)
                        
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
        # Organization Registration Form
        with st.form("organization_register"):
            st.write("### 🏢 Organization Account Registration")
            
            # Basic Information
            st.write("#### 🏢 Organization Information")
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
            st.write("#### 📄 Organization Document Verification")
            st.warning("🛡️ Organization Verification Required - To ensure legitimacy and prevent fraudulent organizations, we require official registration documents.")
            
            # Registration Certificate
            st.write("**📄 Registration Certificate** *")
            st.caption("Upload official registration certificate (Society Registration, Trust Deed, Company Incorporation, etc.)")
            registration_certificate = st.file_uploader(
                "Upload Registration Certificate",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                key="registration_certificate_upload"
            )
            
            # Tax Exemption Certificate
            st.write("**📄 Tax Exemption Certificate** *")
            st.caption("Upload 12A/80G certificate for NGOs or relevant tax documents for other organization types.")
            tax_exemption = st.file_uploader(
                "Upload Tax Exemption Certificate",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                key="tax_exemption_upload"
            )
            
            # PAN Card of Organization
            st.write("**📄 Organization PAN Card** *")
            st.caption("Upload PAN card issued in the name of the organization.")
            org_pan_card = st.file_uploader(
                "Upload Organization PAN Card",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                key="org_pan_card_upload"
            )
            
            # Additional Documents
            st.write("#### 📋 Additional Documents")
            
            # Audited Financial Statements
            st.write("**📄 Audited Financial Statements**")
            st.caption("Upload last 2 years audited financial statements or balance sheets.")
            financial_statements = st.file_uploader(
                "Upload Financial Statements",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                key="financial_statements_upload"
            )
            
            # Board Resolution
            st.write("**📄 Board Resolution**")
            st.caption("Upload board resolution authorizing the contact person to register on behalf of the organization.")
            board_resolution = st.file_uploader(
                "Upload Board Resolution",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                key="board_resolution_upload"
            )
            
            # FCRA Certificate (for NGOs)
            if org_type == "NGO":
                st.write("**📄 FCRA Certificate**")
                st.caption("Upload FCRA (Foreign Contribution Regulation Act) certificate if applicable.")
                fcra_certificate = st.file_uploader(
                    "Upload FCRA Certificate",
                    type=['pdf', 'jpg', 'jpeg', 'png'],
                    key="fcra_certificate_upload"
                )
            
            # Terms and conditions
            st.write("#### ✅ Terms & Conditions")
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
                            'newsletter': newsletter
                        }
                        
                        success, result = register_user(user_data)
                        
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
    st.write("### Or register with:")
    st.info("Note: Social registration will still require document verification to be completed later.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔵 Register with Google", use_container_width=True, key="google_register"):
            demo_user = {
                'id': 'google_demo',
                'email': 'demo@google.com',
                'name': 'Google User',
                'account_type': account_type.lower(),
                'verified': False,
                'verification_status': 'pending'
            }
            st.session_state.authenticated = True
            st.session_state.user_data = demo_user
            st.success("Welcome to HAVEN!")
            st.info("Please complete document verification from your profile to unlock all features.")
            time.sleep(2)
            st.session_state.current_page = 'home'
            st.rerun()
    
    with col2:
        if st.button("🔵 Register with Facebook", use_container_width=True, key="facebook_register"):
            demo_user = {
                'id': 'facebook_demo',
                'email': 'demo@facebook.com',
                'name': 'Facebook User',
                'account_type': account_type.lower(),
                'verified': False,
                'verification_status': 'pending'
            }
            st.session_state.authenticated = True
            st.session_state.user_data = demo_user
            st.success("Welcome to HAVEN!")
            st.info("Please complete document verification from your profile to unlock all features.")
            time.sleep(2)
            st.session_state.current_page = 'home'
            st.rerun()
    
    # Back to login button
    if st.button("⬅️ Back to Login", use_container_width=True, key="back_to_login"):
        st.session_state.current_page = 'login'
        st.rerun()

def show_home():
    """Show authenticated user dashboard"""
    user_data = st.session_state.user_data
    
    # Header with user info
    st.title(f"🏠 Welcome back, {user_data.get('name', 'User')}!")
    
    # Verification Status
    verification_status = user_data.get('verification_status', 'verified')
    if verification_status == 'pending':
        st.warning("📋 Document verification is pending. Some features may be limited until verification is complete.")
    elif verification_status == 'verified':
        st.success("✅ Your account is fully verified!")
    elif verification_status == 'rejected':
        st.error("❌ Document verification was rejected. Please contact support or re-submit documents.")
    
    if user_data.get('account_type') == 'organization':
        st.write(f"**Organization Type:** {user_data.get('org_type', 'N/A')}")
    
    # Logout button
    if st.button("🚪 Logout", key="logout_btn"):
        logout_user()
        st.rerun()
    
    # Dashboard content
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("### 🎯 Create Campaign")
        st.write("Launch your crowdfunding campaign")
        
        if verification_status == 'verified':
            if st.button("Start Campaign", use_container_width=True, key="create_campaign_btn"):
                st.session_state.current_page = 'campaign'
                st.rerun()
        else:
            st.button("Start Campaign", use_container_width=True, disabled=True, key="create_campaign_btn_disabled")
            st.caption("⚠️ Requires verification")
    
    with col2:
        st.write("### 🔍 Browse Projects")
        st.write("Discover amazing causes to support")
        
        if st.button("Browse Now", use_container_width=True, key="browse_campaigns_btn"):
            st.session_state.current_page = 'explore'
            st.rerun()
    
    with col3:
        st.write("### ❤️ Support Causes")
        st.write("Make a difference today")
        
        if st.button("Donate Now", use_container_width=True, key="support_causes_btn"):
            st.session_state.current_page = 'explore'
            st.rerun()
    
    # User stats
    st.subheader("📊 Your Impact")
    
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
    st.title("🎯 Create Your Campaign")
    
    st.info("Campaign creation feature coming soon!")
    
    if st.button("⬅️ Back to Dashboard", key="back_to_dashboard_campaign"):
        st.session_state.current_page = 'home'
        st.rerun()

def show_explore():
    """Show campaign browsing page"""
    st.title("🔍 Explore Campaigns")
    
    st.info("Campaign browsing feature coming soon!")
    
    if st.button("⬅️ Back to Dashboard", key="back_to_dashboard_explore"):
        st.session_state.current_page = 'home'
        st.rerun()

def show_search():
    """Show search page"""
    st.title("🔎 Search Campaigns")
    
    st.info("Search feature coming soon!")
    
    if st.button("⬅️ Back to Dashboard", key="back_to_dashboard_search"):
        st.session_state.current_page = 'home'
        st.rerun()

def show_profile():
    """Show profile page"""
    user_data = st.session_state.user_data
    
    st.title("👤 User Profile")
    
    # Verification Status Section
    st.subheader("📋 Verification Status")
    
    verification_status = user_data.get('verification_status', 'verified')
    
    if verification_status == 'pending':
        st.warning("⏳ Document verification is in progress. This typically takes 24-48 hours for individuals and 3-5 business days for organizations.")
    elif verification_status == 'verified':
        st.success("✅ Your account is fully verified! You can now access all platform features.")
    elif verification_status == 'rejected':
        st.error("❌ Document verification was rejected. Please contact support for details.")
        
        if st.button("Re-submit Documents"):
            st.session_state.current_page = 'register'
            st.rerun()
    
    st.info("Profile management feature coming soon!")
    
    if st.button("⬅️ Back to Dashboard", key="back_to_dashboard_profile"):
        st.session_state.current_page = 'home'
        st.rerun()

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
    
    # Simple CSS for light green theme - NO HTML MARKUP
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
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
    }
    
    .stButton > button:disabled {
        background: #cccccc;
        color: #666666;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar navigation (only show if authenticated)
    if st.session_state.authenticated:
        render_sidebar_navigation()
    
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
    st.divider()
    st.write("© 2025 HAVEN - Crowdfunding Platform | Built with ❤️ using Streamlit")

if __name__ == "__main__":
    main()

