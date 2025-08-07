"""
WORKING Haven Crowdfunding Platform - Main Application
This version properly imports the existing workflow files from your repository
"""

import streamlit as st
import logging
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Haven - Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for MaterializeCSS-inspired styling
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        background: linear-gradient(135deg, #4CAF50, #66BB6A);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #E8F5E8;
        border-radius: 10px 10px 0 0;
        color: #2E7D32;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    
    /* Card styling */
    .info-card {
        background: #E8F5E8;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: #FFF3E0;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #FF9800;
        margin: 1rem 0;
    }
    
    .error-card {
        background: #FFEBEE;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #F44336;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50, #66BB6A);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #388E3C, #4CAF50);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Navbar styling */
    .navbar {
        background: #4CAF50;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .navbar a {
        color: white;
        text-decoration: none;
        margin: 0 1rem;
        font-weight: bold;
    }
    
    /* Role selection cards */
    .role-card {
        background: #F1F8E9;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #C8E6C9;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .role-card:hover {
        border-color: #4CAF50;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    
    /* OAuth buttons */
    .oauth-button {
        background: white;
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .oauth-button:hover {
        border-color: #4CAF50;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
    }
    
    /* Simplified term styling */
    .simplified-term {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #4CAF50;
        cursor: help;
    }
    
    .info-icon {
        font-size: 14px;
        color: #4CAF50;
        margin-left: 4px;
        cursor: help;
    }
    
    .term-explanation {
        display: none;
        position: absolute;
        background: #4CAF50;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        white-space: nowrap;
        z-index: 1000;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        margin-bottom: 5px;
    }
    
    .simplified-term:hover .term-explanation {
        display: block;
    }
    
    /* Progress indicators */
    .progress-container {
        background: #E8F5E8;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Status badges */
    .status-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .status-active {
        background: #C8E6C9;
        color: #2E7D32;
    }
    
    .status-pending {
        background: #FFF9C4;
        color: #F57F17;
    }
    
    .status-completed {
        background: #C8E6C9;
        color: #2E7D32;
    }
</style>
""", unsafe_allow_html=True)

# Safe rerun function for Streamlit compatibility
def safe_rerun():
    """Safe rerun function that works with both old and new Streamlit versions"""
    try:
        if hasattr(st, 'rerun'):
            st.rerun()
        elif hasattr(st, 'experimental_rerun'):
            st.experimental_rerun()
        else:
            st.markdown('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in safe_rerun: {e}")

# Import workflow modules with error handling
def import_workflow_modules():
    """Import workflow modules with proper error handling"""
    modules = {}
    
    try:
        import workflow_auth_utils
        modules['auth_utils'] = workflow_auth_utils
        logger.info("✅ Successfully imported workflow_auth_utils")
    except ImportError as e:
        logger.warning(f"❌ Failed to import workflow_auth_utils: {e}")
        modules['auth_utils'] = None
    
    try:
        import workflow_campaign_pages
        modules['campaign_pages'] = workflow_campaign_pages
        logger.info("✅ Successfully imported workflow_campaign_pages")
    except ImportError as e:
        logger.warning(f"❌ Failed to import workflow_campaign_pages: {e}")
        modules['campaign_pages'] = None
    
    try:
        import workflow_registration_pages
        modules['registration_pages'] = workflow_registration_pages
        logger.info("✅ Successfully imported workflow_registration_pages")
    except ImportError as e:
        logger.warning(f"❌ Failed to import workflow_registration_pages: {e}")
        modules['registration_pages'] = None
    
    try:
        import workflow_verification_funding
        modules['verification_funding'] = workflow_verification_funding
        logger.info("✅ Successfully imported workflow_verification_funding")
    except ImportError as e:
        logger.warning(f"❌ Failed to import workflow_verification_funding: {e}")
        modules['verification_funding'] = None
    
    try:
        import oauth_integration
        modules['oauth_integration'] = oauth_integration
        logger.info("✅ Successfully imported oauth_integration")
    except ImportError as e:
        logger.warning(f"❌ Failed to import oauth_integration: {e}")
        modules['oauth_integration'] = None
    
    try:
        import corrected_authentication_flow
        modules['auth_flow'] = corrected_authentication_flow
        logger.info("✅ Successfully imported corrected_authentication_flow")
    except ImportError as e:
        logger.warning(f"❌ Failed to import corrected_authentication_flow: {e}")
        modules['auth_flow'] = None
    
    return modules

# Initialize workflow modules
WORKFLOW_MODULES = import_workflow_modules()

# Initialize session state
def initialize_session_state():
    """Initialize session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.session_state.user_type = None
        st.session_state.current_page = 'home'
        st.session_state.simplification_active = False
        logger.info("Session state initialized")

# Authentication functions
def check_user_authentication() -> bool:
    """Check if user is authenticated"""
    if WORKFLOW_MODULES['auth_utils']:
        try:
            return WORKFLOW_MODULES['auth_utils'].check_user_authentication()
        except Exception as e:
            logger.error(f"Error checking authentication: {e}")
    
    # Fallback authentication check
    return st.session_state.get('authenticated', False)

def get_user_role() -> Optional[str]:
    """Get current user role"""
    if WORKFLOW_MODULES['auth_utils']:
        try:
            return WORKFLOW_MODULES['auth_utils'].get_user_role()
        except Exception as e:
            logger.error(f"Error getting user role: {e}")
    
    # Fallback role check
    return st.session_state.get('user_type')

def handle_user_logout():
    """Handle user logout"""
    if WORKFLOW_MODULES['auth_utils']:
        try:
            WORKFLOW_MODULES['auth_utils'].handle_user_logout()
            return
        except Exception as e:
            logger.error(f"Error in logout: {e}")
    
    # Fallback logout
    st.session_state.authenticated = False
    st.session_state.user_data = None
    st.session_state.user_type = None
    st.session_state.current_page = 'home'
    st.success("✅ Logged out successfully!")
    safe_rerun()

# Navigation functions
def show_navbar():
    """Show navigation bar for authenticated users"""
    if not check_user_authentication():
        return
    
    user_role = get_user_role()
    user_data = st.session_state.get('user_data', {})
    
    with st.container():
        st.markdown("""
        <div class='navbar'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <span style='font-size: 1.2rem; font-weight: bold;'>🏠 Haven Platform</span>
                </div>
                <div>
                    <span style='margin-right: 1rem;'>👤 {role} | {email}</span>
                </div>
            </div>
        </div>
        """.format(
            role=user_role.title() if user_role else "User",
            email=user_data.get('email', 'Unknown')
        ), unsafe_allow_html=True)
    
    # Navigation menu
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            safe_rerun()
    
    with col2:
        if st.button("🔍 Browse Campaigns", use_container_width=True):
            st.session_state.current_page = 'browse_campaigns'
            safe_rerun()
    
    with col3:
        if user_role == 'organization':
            if st.button("🚀 Create Campaign", use_container_width=True):
                st.session_state.current_page = 'create_campaign'
                safe_rerun()
        else:
            if st.button("❤️ My Donations", use_container_width=True):
                st.session_state.current_page = 'my_donations'
                safe_rerun()
    
    with col4:
        if user_role == 'organization':
            if st.button("📊 My Campaigns", use_container_width=True):
                st.session_state.current_page = 'my_campaigns'
                safe_rerun()
        else:
            if st.button("📈 Impact Tracker", use_container_width=True):
                st.session_state.current_page = 'impact_tracker'
                safe_rerun()
    
    with col5:
        if st.button("👤 Profile", use_container_width=True):
            st.session_state.current_page = 'profile'
            safe_rerun()
    
    with col6:
        if st.button("🚪 Logout", use_container_width=True):
            handle_user_logout()

# Page rendering functions
def show_home_page():
    """Show home page"""
    st.markdown("""
    <div class='main-header'>
        <h1>🏠 Welcome to Haven</h1>
        <p>Empowering Communities Through Crowdfunding</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not check_user_authentication():
        # Show login/register tabs for unauthenticated users
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            show_login_tab()
        
        with tab2:
            show_register_tab()
    else:
        # Show dashboard for authenticated users
        show_dashboard_page()

def show_login_tab():
    """Show login tab content"""
    if WORKFLOW_MODULES['auth_utils']:
        try:
            WORKFLOW_MODULES['auth_utils'].show_login_form()
            return
        except Exception as e:
            logger.error(f"Error showing login form: {e}")
    
    # Fallback login form
    st.markdown("### 🔐 Login (Fallback Mode)")
    st.markdown("""
    <div class='warning-card'>
        <h4>⚠️ Using fallback login implementation</h4>
        <p>Please ensure workflow modules are available for full functionality.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Choose Your Role")
    
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
        
        if st.button("Login as Individual", key="fallback_login_individual", use_container_width=True, type="primary"):
            # Simulate login for demo
            st.session_state.authenticated = True
            st.session_state.user_type = 'individual'
            st.session_state.user_data = {'email': 'demo@individual.com', 'name': 'Demo Individual'}
            st.success("✅ Demo login successful!")
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
        
        if st.button("Login as Organization", key="fallback_login_organization", use_container_width=True, type="primary"):
            # Simulate login for demo
            st.session_state.authenticated = True
            st.session_state.user_type = 'organization'
            st.session_state.user_data = {'email': 'demo@organization.com', 'name': 'Demo Organization'}
            st.success("✅ Demo login successful!")
            safe_rerun()

def show_register_tab():
    """Show register tab content"""
    if WORKFLOW_MODULES['registration_pages']:
        try:
            WORKFLOW_MODULES['registration_pages'].show_registration_page()
            return
        except Exception as e:
            logger.error(f"Error showing registration page: {e}")
    
    # Fallback registration form
    st.markdown("### 📝 New to Haven? Register Now!")
    
    st.markdown("""
    <div class='info-card'>
        <h4>💡 Registration Process</h4>
        <p>Your details will be stored in our database first, then you can log in using OAuth.</p>
        <p><strong>Steps:</strong> Fill Form → Database Storage → OAuth Login → Access</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📝 Registration (Fallback Mode)")
    st.markdown("""
    <div class='warning-card'>
        <h4>⚠️ Using fallback registration implementation</h4>
        <p>Please ensure workflow modules are available for full functionality.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple registration form
    with st.form("fallback_registration"):
        col1, col2 = st.columns(2)
        
        with col1:
            user_type = st.selectbox("User Type", ["individual", "organization"])
            name = st.text_input("Full Name/Organization Name")
            email = st.text_input("Email Address")
        
        with col2:
            phone = st.text_input("Phone Number")
            location = st.text_input("Location")
            
            if user_type == "organization":
                org_type = st.selectbox("Organization Type", ["NGO", "Charity", "Social Enterprise", "Other"])
        
        terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        if st.form_submit_button("Register", use_container_width=True, type="primary"):
            if not all([name, email, phone, location]) or not terms_accepted:
                st.error("❌ Please fill in all required fields and accept the terms")
            else:
                st.success("✅ Registration successful! You can now log in.")
                st.info("💡 In the full version, your data would be stored in the database.")

def show_dashboard_page():
    """Show user dashboard"""
    user_role = get_user_role()
    user_data = st.session_state.get('user_data', {})
    
    st.markdown(f"### 📊 {user_role.title()} Dashboard")
    
    # Welcome message
    st.markdown(f"""
    <div class='info-card'>
        <h4>👋 Welcome back, {user_data.get('name', 'User')}!</h4>
        <p>Here's your activity overview and quick actions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard content based on role
    if user_role == 'individual':
        show_individual_dashboard()
    elif user_role == 'organization':
        show_organization_dashboard()

def show_individual_dashboard():
    """Show individual user dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Donations", "$1,250", "+$150")
    
    with col2:
        st.metric("Campaigns Supported", "8", "+2")
    
    with col3:
        st.metric("Impact Score", "95%", "+5%")
    
    with col4:
        st.metric("Tax Savings", "$375", "+$45")
    
    st.markdown("#### 🎯 Recent Activity")
    st.info("📊 Your recent donations and campaign interactions would appear here.")
    
    st.markdown("#### ❤️ Recommended Campaigns")
    st.info("🔍 Personalized campaign recommendations would appear here.")

def show_organization_dashboard():
    """Show organization dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Campaigns", "3", "+1")
    
    with col2:
        st.metric("Total Raised", "$45,230", "+$2,150")
    
    with col3:
        st.metric("Total Donors", "156", "+12")
    
    with col4:
        st.metric("Success Rate", "87%", "+3%")
    
    st.markdown("#### 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🆕 Create New Campaign", use_container_width=True, type="primary"):
            st.session_state.current_page = 'create_campaign'
            safe_rerun()
    
    with col2:
        if st.button("📊 View Campaign Analytics", use_container_width=True):
            st.session_state.current_page = 'campaign_analytics'
            safe_rerun()
    
    with col3:
        if st.button("💬 Donor Communications", use_container_width=True):
            st.session_state.current_page = 'donor_communications'
            safe_rerun()
    
    st.markdown("#### 📈 Campaign Performance")
    st.info("📊 Your campaign performance metrics would appear here.")

def show_create_campaign_page():
    """Show create campaign page"""
    if WORKFLOW_MODULES['campaign_pages']:
        try:
            WORKFLOW_MODULES['campaign_pages'].render_create_campaign_page(st.session_state)
            return
        except Exception as e:
            logger.error(f"Error showing create campaign page: {e}")
    
    # Fallback create campaign page
    st.markdown("### 🚀 Create New Campaign (Fallback Mode)")
    st.markdown("""
    <div class='warning-card'>
        <h4>⚠️ Using fallback campaign creation</h4>
        <p>Please ensure workflow modules are available for full functionality.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🔧 Campaign creation functionality would be available here with the full workflow modules.")

def show_browse_campaigns_page():
    """Show browse campaigns page"""
    if WORKFLOW_MODULES['verification_funding']:
        try:
            WORKFLOW_MODULES['verification_funding'].render_campaign_browse_page(st.session_state)
            return
        except Exception as e:
            logger.error(f"Error showing browse campaigns page: {e}")
    
    # Fallback browse campaigns page
    st.markdown("### 🔍 Browse Campaigns (Fallback Mode)")
    st.markdown("""
    <div class='warning-card'>
        <h4>⚠️ Using fallback campaign browsing</h4>
        <p>Please ensure workflow modules are available for full functionality.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🔧 Campaign browsing functionality would be available here with the full workflow modules.")

def show_my_campaigns_page():
    """Show my campaigns page"""
    if WORKFLOW_MODULES['campaign_pages']:
        try:
            WORKFLOW_MODULES['campaign_pages'].render_campaign_management_page(st.session_state)
            return
        except Exception as e:
            logger.error(f"Error showing my campaigns page: {e}")
    
    # Fallback my campaigns page
    st.markdown("### 📊 My Campaigns (Fallback Mode)")
    st.markdown("""
    <div class='warning-card'>
        <h4>⚠️ Using fallback campaign management</h4>
        <p>Please ensure workflow modules are available for full functionality.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🔧 Campaign management functionality would be available here with the full workflow modules.")

def show_profile_page():
    """Show user profile page"""
    st.markdown("### 👤 User Profile")
    
    user_data = st.session_state.get('user_data', {})
    user_role = get_user_role()
    
    st.markdown(f"""
    <div class='info-card'>
        <h4>📋 Profile Information</h4>
        <p><strong>Role:</strong> {user_role.title() if user_role else 'Unknown'}</p>
        <p><strong>Email:</strong> {user_data.get('email', 'Unknown')}</p>
        <p><strong>Name:</strong> {user_data.get('name', 'Unknown')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🔧 Full profile management functionality would be available here.")

# Sidebar functions
def show_sidebar():
    """Show sidebar with settings and debug info"""
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Term simplification toggle
        simplification_active = st.checkbox(
            "Enable Term Simplification",
            value=st.session_state.get('simplification_active', False),
            help="Show simplified terms with explanations"
        )
        st.session_state.simplification_active = simplification_active
        
        # Debug information
        if st.checkbox("Show Debug Info"):
            st.markdown("### 🔍 Debug Information")
            
            st.markdown("**Workflow Modules Status:**")
            for module_name, module in WORKFLOW_MODULES.items():
                status = "✅ Available" if module else "❌ Missing"
                st.write(f"- {module_name}: {status}")
            
            st.markdown("**Session State:**")
            st.write(f"- Authenticated: {st.session_state.get('authenticated', False)}")
            st.write(f"- User Type: {st.session_state.get('user_type', 'None')}")
            st.write(f"- Current Page: {st.session_state.get('current_page', 'None')}")
            
            if st.button("Clear Session State"):
                for key in list(st.session_state.keys()):
                    if key != 'initialized':
                        del st.session_state[key]
                safe_rerun()

# Main application
def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Show sidebar
    show_sidebar()
    
    # Show navbar if authenticated
    if check_user_authentication():
        show_navbar()
    
    # Route to appropriate page
    current_page = st.session_state.get('current_page', 'home')
    
    if current_page == 'home' or not check_user_authentication():
        show_home_page()
    elif current_page == 'dashboard':
        show_dashboard_page()
    elif current_page == 'create_campaign':
        show_create_campaign_page()
    elif current_page == 'browse_campaigns':
        show_browse_campaigns_page()
    elif current_page == 'my_campaigns':
        show_my_campaigns_page()
    elif current_page == 'profile':
        show_profile_page()
    else:
        st.error(f"❌ Unknown page: {current_page}")
        st.session_state.current_page = 'home'
        safe_rerun()

if __name__ == "__main__":
    main()

