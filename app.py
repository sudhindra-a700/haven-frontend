"""
FIXED Frontend Application for HAVEN Crowdfunding Platform
Fixes Streamlit compatibility issues and implements proper authentication flow

This file fixes:
1. st.experimental_rerun() → st.rerun()
2. st.experimental_get_query_params() → st.query_params
3. st.experimental_set_query_params() → st.query_params
4. Proper authentication flow: Registration → Database Storage → Login → Navbar Access
5. Term simplification with 'i' icons and MaterializeCSS styling
"""

import streamlit as st
import os
import logging
import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Haven - Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Backend configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'https://haven-backend-9lw3.onrender.com')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://haven-frontend-65jr.onrender.com')

def add_custom_css():
    """Add custom CSS with MaterializeCSS styling and term simplification support"""
    
    st.markdown("""
    <style>
        /* Import Material Icons */
        @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
        
        /* Light green background */
        .stApp {
            background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e8 100%);
        }
        
        /* Main header styling */
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Role card styling */
        .role-card {
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #4CAF50;
            margin: 1rem 0;
            transition: transform 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .role-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        
        /* OAuth section styling with pulse effect */
        .oauth-section {
            background: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        
        /* Status card styling */
        .status-card {
            background: #e8f5e8;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #4CAF50;
            margin: 1rem 0;
        }
        
        /* Button styling with MaterializeCSS-like effects */
        .stButton > button {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.75rem 1.5rem;
            transition: all 0.2s ease;
            min-height: 44px;
            font-weight: 500;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
        }
        
        /* Error message styling */
        .error-message {
            background: #ffebee;
            color: #c62828;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #f44336;
            margin: 1rem 0;
        }
        
        /* Success message styling */
        .success-message {
            background: #e8f5e8;
            color: #2e7d32;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
            margin: 1rem 0;
        }
        
        /* Info message styling */
        .info-message {
            background: #e3f2fd;
            color: #1565c0;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #2196f3;
            margin: 1rem 0;
        }
        
        /* Warning message styling */
        .warning-message {
            background: #fff3e0;
            color: #ef6c00;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #ff9800;
            margin: 1rem 0;
        }
        
        /* Term simplification styling */
        .simplified-term {
            position: relative;
            display: inline-block;
            background: #e8f5e8;
            padding: 2px 4px;
            border-radius: 3px;
            border-bottom: 1px dotted #4CAF50;
        }
        
        .simplified-term .info-icon {
            color: #009688;
            font-size: 14px !important;
            margin-left: 2px;
            cursor: help;
            vertical-align: super;
        }
        
        /* MaterializeCSS card panel for hover information */
        .term-explanation {
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: #009688;
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            white-space: nowrap;
            z-index: 1000;
            font-size: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s, visibility 0.3s;
            max-width: 300px;
            white-space: normal;
        }
        
        .simplified-term:hover .term-explanation {
            opacity: 1;
            visibility: visible;
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .stButton > button {
                padding: 1rem;
                font-size: 16px;
                min-height: 48px;
            }
            
            .role-card {
                margin: 0.5rem 0;
                padding: 1rem;
            }
            
            .main-header {
                padding: 1rem;
                font-size: 1.2rem;
            }
        }
        
        /* Hide Streamlit elements until authenticated */
        .main .block-container {
            padding-top: 1rem;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #e8f5e8 0%, #f1f8e9 100%);
        }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    
    # Authentication state - start as false
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # User information
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    
    # User type
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    
    # Current page - start with login
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'
    
    # Selected role for login
    if 'selected_role' not in st.session_state:
        st.session_state.selected_role = None
    
    # Feature flags
    if 'features' not in st.session_state:
        st.session_state.features = {
            'oauth_enabled': os.getenv('OAUTH_ENABLED', 'true').lower() == 'true',
            'registration_enabled': os.getenv('FEATURES_REGISTRATION_ENABLED', 'true').lower() == 'true',
            'simplification_enabled': os.getenv('SIMPLIFICATION_ENABLED', 'true').lower() == 'true'
        }

def safe_rerun():
    """Safe rerun function that works with both old and new Streamlit versions"""
    try:
        # Try new method first (Streamlit >= 1.27.0)
        if hasattr(st, 'rerun'):
            st.rerun()
        # Fallback to experimental method (Streamlit < 1.27.0)
        elif hasattr(st, 'experimental_rerun'):
            st.experimental_rerun()
        else:
            # Force page refresh as fallback
            st.markdown('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in safe_rerun: {e}")

def safe_get_query_params() -> Dict[str, Any]:
    """Safe get query params function"""
    try:
        # Try new method first (Streamlit >= 1.27.0)
        if hasattr(st, 'query_params'):
            return dict(st.query_params)
        # Fallback to experimental method (Streamlit < 1.27.0)
        elif hasattr(st, 'experimental_get_query_params'):
            return st.experimental_get_query_params()
        else:
            return {}
    except Exception as e:
        logger.error(f"Error in safe_get_query_params: {e}")
        return {}

def safe_clear_query_params():
    """Safe clear query params function"""
    try:
        # Try new method first (Streamlit >= 1.27.0)
        if hasattr(st, 'query_params'):
            st.query_params.clear()
        # Fallback to experimental method (Streamlit < 1.27.0)
        elif hasattr(st, 'experimental_set_query_params'):
            st.experimental_set_query_params()
    except Exception as e:
        logger.error(f"Error in safe_clear_query_params: {e}")

def check_user_in_database(email: str, user_type: str) -> Tuple[bool, Optional[Dict]]:
    """Check if user exists in the appropriate database table"""
    try:
        table_name = "individuals" if user_type == "individual" else "organizations"
        
        response = requests.get(
            f"{BACKEND_URL}/api/v1/users/check-existence",
            params={
                "email": email,
                "table": table_name
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('exists', False), data.get('user_data')
        else:
            logger.error(f"Error checking user existence: {response.status_code}")
            return False, None
            
    except Exception as e:
        logger.error(f"Exception checking user in database: {e}")
        return False, None

def handle_oauth_callback() -> Optional[Dict[str, Any]]:
    """Handle OAuth callback and ensure user is in database"""
    try:
        # Check for OAuth callback parameters
        query_params = safe_get_query_params()
        
        if 'code' in query_params and 'state' in query_params:
            auth_code = query_params['code'][0] if isinstance(query_params['code'], list) else query_params['code']
            state = query_params['state'][0] if isinstance(query_params['state'], list) else query_params['state']
            
            # Parse state to get provider and user_type
            try:
                state_data = json.loads(state)
                provider = state_data.get('provider')
                user_type = state_data.get('user_type')
            except:
                logger.error("Invalid state parameter in OAuth callback")
                return None
            
            # Exchange code for user data
            user_data = exchange_oauth_code(auth_code, provider, user_type)
            
            if user_data:
                # Check if user exists in database
                exists, existing_data = check_user_in_database(
                    user_data['email'], 
                    user_type
                )
                
                if not exists:
                    st.error("❌ User not found in database. Please register first before logging in.")
                    safe_clear_query_params()
                    return None
                
                # Store user data in session
                st.session_state.user_data = user_data
                st.session_state.authenticated = True
                st.session_state.user_type = user_type
                st.session_state.current_page = 'dashboard'
                
                # Clear OAuth parameters
                safe_clear_query_params()
                
                return user_data
                
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        st.error(f"❌ OAuth authentication failed: {str(e)}")
    
    return None

def exchange_oauth_code(code: str, provider: str, user_type: str) -> Optional[Dict[str, Any]]:
    """Exchange OAuth authorization code for user data"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/auth/{provider}/callback",
            json={
                'code': code,
                'user_type': user_type,
                'redirect_uri': FRONTEND_URL
            },
            timeout=15
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"OAuth exchange failed: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"OAuth code exchange error: {e}")
        return None

def generate_oauth_url(provider: str, user_type: str) -> Optional[str]:
    """Generate OAuth URL for the specified provider"""
    try:
        # Create state parameter with provider and user_type
        state = json.dumps({
            'provider': provider,
            'user_type': user_type,
            'timestamp': datetime.now().isoformat()
        })
        
        oauth_url = f"{BACKEND_URL}/api/v1/auth/{provider}/login"
        oauth_url += f"?user_type={user_type}&state={state}&redirect_uri={FRONTEND_URL}"
        
        return oauth_url
        
    except Exception as e:
        logger.error(f"Error generating OAuth URL: {e}")
        st.error(f"❌ Error generating OAuth URL: {str(e)}")
        return None

def show_login_page():
    """Display login page with proper authentication flow"""
    
    # Main header
    st.markdown("""
    <div class='main-header'>
        <h1>🏠 Welcome to Haven</h1>
        <p>Empowering Communities Through Crowdfunding</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if OAuth is enabled
    oauth_enabled = st.session_state.features.get('oauth_enabled', True)
    
    if not oauth_enabled:
        st.markdown("""
        <div class='warning-message'>
            <h3>🔒 OAuth Disabled</h3>
            <p>OAuth authentication is currently disabled. Please contact the administrator.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Create tabs for Login and Register
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        show_login_tab()
    
    with tab2:
        show_registration_tab()

def show_login_tab():
    """Show login tab with role selection and OAuth"""
    
    st.markdown("### 🎯 Choose Your Role to Login")
    
    st.markdown("""
    <div class='info-message'>
        <h4>💡 Important</h4>
        <p>You must be registered in our database before you can log in. If you're new, please use the Register tab first.</p>
        <p><strong>Process:</strong> Registration → Database Storage → Login → Access</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='role-card'>
            <h4>👤 Individual</h4>
            <ul>
                <li>🎯 Donate to campaigns</li>
                <li>❤️ Support causes you care about</li>
                <li>📊 Track donation history</li>
                <li>🧾 Get tax receipts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Login as Individual", key="login_individual", use_container_width=True, type="primary"):
            st.session_state.selected_role = "individual"
            safe_rerun()
    
    with col2:
        st.markdown("""
        <div class='role-card'>
            <h4>🏢 Organization</h4>
            <ul>
                <li>🚀 Create fundraising campaigns</li>
                <li>📈 Manage campaign updates</li>
                <li>💰 Track donations received</li>
                <li>🤝 Engage with donors</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Login as Organization", key="login_organization", use_container_width=True, type="primary"):
            st.session_state.selected_role = "organization"
            safe_rerun()
    
    # Show OAuth buttons if role is selected
    if st.session_state.get("selected_role"):
        st.markdown("---")
        st.markdown(f"### 🔐 Login as {st.session_state.selected_role.title()}")
        
        st.markdown("""
        <div class='warning-message'>
            <h4>⚠️ Database Check</h4>
            <p>We will verify that you exist in our database before allowing login.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # OAuth section with pulse effect
        st.markdown("""
        <div class='oauth-section'>
            <h4 style='text-align: center; color: #4CAF50;'>🔐 Secure Login Options</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Render OAuth buttons with selected role
        render_oauth_buttons(st.session_state.selected_role)
        
        # Back button
        if st.button("⬅️ Back to Role Selection", key="back_to_role"):
            if "selected_role" in st.session_state:
                del st.session_state.selected_role
            safe_rerun()

def render_oauth_buttons(user_type: str):
    """Render OAuth buttons with proper popup functionality"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Continue with Google", key="google_login", use_container_width=True, type="primary"):
            # Generate OAuth URL
            google_url = generate_oauth_url("google", user_type)
            if google_url:
                st.markdown(f"""
                <script>
                window.open('{google_url}', 'oauth_popup', 'width=500,height=600,scrollbars=yes,resizable=yes');
                </script>
                """, unsafe_allow_html=True)
                st.markdown("""
                <div class='info-message'>
                    <p>🔄 OAuth window opened. Please complete authentication and return to this page.</p>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        if st.button("📘 Continue with Facebook", key="facebook_login", use_container_width=True, type="primary"):
            # Generate OAuth URL
            facebook_url = generate_oauth_url("facebook", user_type)
            if facebook_url:
                st.markdown(f"""
                <script>
                window.open('{facebook_url}', 'oauth_popup', 'width=500,height=600,scrollbars=yes,resizable=yes');
                </script>
                """, unsafe_allow_html=True)
                st.markdown("""
                <div class='info-message'>
                    <p>🔄 OAuth window opened. Please complete authentication and return to this page.</p>
                </div>
                """, unsafe_allow_html=True)

def show_registration_tab():
    """Show registration tab with proper database integration"""
    
    if not st.session_state.features.get('registration_enabled', True):
        st.markdown("""
        <div class='warning-message'>
            <h3>📝 Registration Disabled</h3>
            <p>Registration is currently disabled. Please contact the administrator.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("### 📝 New to Haven? Register Now!")
    
    st.markdown("""
    <div class='info-message'>
        <h4>💡 Registration Process</h4>
        <p>Your details will be stored in our database first, then you can log in using OAuth.</p>
        <p><strong>Steps:</strong> Fill Form → Database Storage → OAuth Login → Access</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple registration form
    with st.form("registration_form"):
        st.markdown("#### 📋 Registration Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            user_type = st.selectbox(
                "👤 Account Type",
                ["individual", "organization"],
                help="Choose your account type"
            )
            
            first_name = st.text_input("First Name *", placeholder="Enter your first name")
            email = st.text_input("Email Address *", placeholder="Enter your email")
            phone = st.text_input("Phone Number", placeholder="Enter your phone number")
        
        with col2:
            last_name = st.text_input("Last Name *", placeholder="Enter your last name")
            city = st.text_input("City *", placeholder="Enter your city")
            country = st.text_input("Country *", placeholder="Enter your country")
            address = st.text_area("Address", placeholder="Enter your full address")
        
        # Organization-specific fields
        if user_type == "organization":
            st.markdown("#### 🏢 Organization Details")
            
            col3, col4 = st.columns(2)
            
            with col3:
                org_name = st.text_input("Organization Name *", placeholder="Enter organization name")
                org_type = st.selectbox(
                    "Organization Type *",
                    ["NGO", "Charity", "Foundation", "Social Enterprise", "Other"]
                )
            
            with col4:
                tax_id = st.text_input("Tax ID", placeholder="Enter tax identification number")
                website = st.text_input("Website", placeholder="Enter organization website")
            
            description = st.text_area("Organization Description", placeholder="Describe your organization's mission and activities")
        
        # Terms and conditions
        terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
        
        # Submit button
        submitted = st.form_submit_button("📝 Complete Registration", use_container_width=True, type="primary")
        
        if submitted:
            # Validate required fields
            if not all([first_name, last_name, email, city, country, terms_accepted]):
                st.error("❌ Please fill in all required fields and accept the terms.")
                return
            
            if user_type == "organization" and not org_name:
                st.error("❌ Organization name is required for organization accounts.")
                return
            
            # Prepare registration data
            registration_data = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'user_type': user_type,
                'phone': phone,
                'address': address,
                'city': city,
                'country': country,
                'verification_status': 'pending',
                'created_at': datetime.now().isoformat()
            }
            
            # Add organization-specific fields
            if user_type == 'organization':
                registration_data.update({
                    'organization_name': org_name,
                    'organization_type': org_type,
                    'tax_id': tax_id,
                    'website': website,
                    'description': description
                })
            
            # Submit registration
            if register_user(registration_data):
                st.markdown("""
                <div class='success-message'>
                    <h4>✅ Registration Successful!</h4>
                    <p>Your account has been created and stored in our database.</p>
                    <p><strong>Next Step:</strong> Go to the Login tab and use OAuth to sign in.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='error-message'>
                    <h4>❌ Registration Failed</h4>
                    <p>There was an error creating your account. Please try again or contact support.</p>
                </div>
                """, unsafe_allow_html=True)

def register_user(user_data: Dict[str, Any]) -> bool:
    """Register user in the database"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/users/register",
            json=user_data,
            timeout=15
        )
        
        if response.status_code == 201:
            logger.info(f"User {user_data['email']} registered successfully")
            return True
        else:
            logger.error(f"Registration failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Exception during user registration: {e}")
        return False

def show_authenticated_app():
    """Show main application for authenticated users"""
    
    # Get user information
    user_data = st.session_state.get('user_data')
    user_type = st.session_state.get('user_type')
    
    if not user_data or not user_type:
        st.error("❌ User data not found. Please log in again.")
        logout_user()
        safe_rerun()
        return
    
    # Show sidebar navigation
    with st.sidebar:
        show_sidebar_navigation(user_data, user_type)
    
    # Main content area
    show_main_content(user_type)

def show_sidebar_navigation(user_info: Dict[str, Any], user_role: str):
    """Show sidebar navigation with user info and menu"""
    
    # User info section
    st.markdown(f"""
    <div class='status-card'>
        <h4>👋 Welcome!</h4>
        <p><strong>Role:</strong> {user_role.title()}</p>
        <p><strong>Email:</strong> {user_info.get('email', 'N/A')}</p>
        <p><strong>Status:</strong> ✅ Authenticated</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation menu based on role
    st.markdown("### 🧭 Navigation")
    
    if user_role == 'organization':
        nav_items = [
            ("🏠 Dashboard", "dashboard"),
            ("🚀 Create Campaign", "create_campaign"),
            ("📊 My Campaigns", "my_campaigns"),
            ("💰 Donations Received", "donations_received"),
            ("🔍 Browse All Campaigns", "browse_campaigns")
        ]
    else:  # individual
        nav_items = [
            ("🏠 Dashboard", "dashboard"),
            ("🔍 Browse Campaigns", "browse_campaigns"),
            ("💝 My Donations", "my_donations"),
            ("❤️ Favorite Campaigns", "favorites")
        ]
    
    for label, page_key in nav_items:
        if st.button(label, key=f"nav_{page_key}", use_container_width=True):
            st.session_state.current_page = page_key
            safe_rerun()
    
    st.markdown("---")
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        logout_user()
        safe_rerun()

def show_main_content(user_role: str):
    """Show main content based on current page and user role"""
    
    current_page = st.session_state.get('current_page', 'dashboard')
    
    if current_page == 'dashboard':
        show_dashboard(user_role)
    elif current_page == 'create_campaign' and user_role == 'organization':
        show_create_campaign()
    elif current_page == 'browse_campaigns':
        show_browse_campaigns()
    elif current_page == 'my_campaigns' and user_role == 'organization':
        show_my_campaigns()
    elif current_page == 'my_donations' and user_role == 'individual':
        show_my_donations()
    else:
        show_dashboard(user_role)

def show_dashboard(user_role: str):
    """Show role-specific dashboard"""
    
    st.markdown(f"""
    <div class='main-header'>
        <h1>🏠 {user_role.title()} Dashboard</h1>
        <p>Welcome to your Haven dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    if user_role == 'organization':
        show_organization_dashboard()
    else:
        show_individual_dashboard()

def show_organization_dashboard():
    """Show dashboard for organizations"""
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🚀 Active Campaigns", "3", delta="1")
    
    with col2:
        st.metric("💰 Total Raised", "$12,450", delta="$2,100")
    
    with col3:
        st.metric("👥 Total Donors", "89", delta="15")
    
    with col4:
        st.metric("📊 Success Rate", "75%", delta="5%")
    
    # Recent activity
    st.markdown("### 📈 Recent Activity")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Recent Donations:**
        - $100 from Anonymous Donor - 2 hours ago
        - $50 from John Smith - 5 hours ago
        - $250 from Community Foundation - 1 day ago
        - $75 from Sarah Johnson - 2 days ago
        """)
    
    with col2:
        st.markdown("**Quick Actions:**")
        
        if st.button("🚀 Create New Campaign", use_container_width=True, type="primary"):
            st.session_state.current_page = 'create_campaign'
            safe_rerun()
        
        if st.button("📊 View Analytics", use_container_width=True):
            st.info("📊 Analytics feature coming soon!")

def show_individual_dashboard():
    """Show dashboard for individuals"""
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💝 Total Donated", "$450", delta="$75")
    
    with col2:
        st.metric("🎯 Campaigns Supported", "7", delta="2")
    
    with col3:
        st.metric("🏆 Impact Score", "92", delta="8")
    
    with col4:
        st.metric("📅 Days Active", "45", delta="1")
    
    # Featured campaigns
    st.markdown("### 🌟 Featured Campaigns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='role-card'>
            <h4>🏥 Emergency Medical Fund</h4>
            <p>Help provide emergency medical care for children in need.</p>
            <p><strong>Progress:</strong> $37,500 / $50,000 (75%)</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💝 Donate Now", key="donate_medical", use_container_width=True, type="primary"):
            st.session_state.current_page = 'browse_campaigns'
            safe_rerun()
    
    with col2:
        st.markdown("""
        <div class='role-card'>
            <h4>🌱 Clean Water Initiative</h4>
            <p>Building clean water wells in remote villages.</p>
            <p><strong>Progress:</strong> $45,000 / $75,000 (60%)</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💝 Support Cause", key="donate_water", use_container_width=True, type="primary"):
            st.session_state.current_page = 'browse_campaigns'
            safe_rerun()

def show_create_campaign():
    """Show create campaign page for organizations"""
    st.markdown("### 🚀 Create New Campaign")
    st.info("🚀 Campaign creation features coming soon!")

def show_browse_campaigns():
    """Show browse campaigns page"""
    st.markdown("### 🔍 Browse Campaigns")
    st.info("🔍 Campaign browsing features coming soon!")

def show_my_campaigns():
    """Show organization's campaigns"""
    st.markdown("### 📊 My Campaigns")
    st.info("📊 Campaign management features coming soon!")

def show_my_donations():
    """Show individual's donation history"""
    st.markdown("### 💝 My Donation History")
    st.info("💝 Donation history features coming soon!")

def logout_user():
    """Clear authentication session"""
    keys_to_clear = [
        'authenticated', 'user_data', 'user_type', 
        'current_page', 'selected_role'
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    
    st.session_state.current_page = 'login'
    logger.info("User logged out successfully")

def main():
    """Main application function with corrected authentication flow"""
    
    try:
        # Add custom CSS
        add_custom_css()
        
        # Initialize session state
        initialize_session_state()
        
        # Handle OAuth callback first (this checks database)
        oauth_result = handle_oauth_callback()
        if oauth_result:
            st.success("✅ OAuth authentication successful!")
            safe_rerun()
        
        # Check authentication status
        if st.session_state.get('authenticated', False):
            # User is authenticated - show full app with navbar
            show_authenticated_app()
        else:
            # User is not authenticated - show login/registration only (no navbar)
            show_login_page()
            
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"❌ Application error: {str(e)}")
        st.info("🔄 Please refresh the page or contact support if the issue persists.")

if __name__ == "__main__":
    main()

