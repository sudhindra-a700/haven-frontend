"""
CORRECTED Frontend Application for HAVEN Crowdfunding Platform
Implements proper authentication flow: Registration → Database Storage → Login → Navbar Access
Integrates term simplification features with 'i' icons and hover explanations

This file ensures:
1. No navbar visibility until user is properly authenticated
2. User data is stored in database before allowing access
3. Proper OAuth flow with database verification
4. Term simplification with 'i' icons and MaterializeCSS styling
5. Role-based access control
"""

import streamlit as st
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Import corrected authentication flow
from corrected_authentication_flow import (
    auth_manager,
    simplification_manager,
    check_authentication,
    require_auth,
    require_role,
    get_current_user,
    get_current_user_type,
    logout_user,
    handle_oauth_callback,
    simplify_text,
    add_simplification_styles,
    explain_term
)

# Import updated workflow utilities (these should be the corrected versions)
try:
    from workflow_auth_utils import get_auth_manager
    from workflow_campaign_pages import render_create_campaign_page
    from workflow_registration_pages import show_registration_page
    from workflow_verification_funding import (
        render_admin_review_page,
        render_campaign_browse_page,
        render_campaign_details_page,
        render_donation_page
    )
except ImportError:

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Haven - Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start collapsed until authenticated
)

def add_custom_css():
    """Add custom CSS with MaterializeCSS styling and term simplification support"""
    
    st.markdown("""
    <style>
        /* Import Material Icons */
        @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
        
        /* Main header styling */
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        /* Role card styling */
        .role-card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #4CAF50;
            margin: 1rem 0;
            transition: transform 0.2s ease;
        }
        
        .role-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
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
        
        /* Navigation styling - hidden by default */
        .nav-container {
            display: none;
        }
        
        .nav-container.authenticated {
            display: block;
        }
        
        .nav-item {
            padding: 0.5rem 1rem;
            margin: 0.2rem 0;
            border-radius: 5px;
            transition: background-color 0.2s ease;
        }
        
        .nav-item:hover {
            background-color: #e8f5e8;
        }
        
        /* Button styling with MaterializeCSS-like effects */
        .stButton > button {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            transition: all 0.2s ease;
            min-height: 44px; /* Touch-friendly */
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
        }
        
        /* Floating action button style for Create Campaign */
        .fab-button {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: #f44336;
            color: white;
            border: none;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.2s ease;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .fab-button:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
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
        
        /* Simplification toggle */
        .simplification-toggle {
            margin: 10px 0;
            padding: 10px 15px;
            background: #e8f5e8;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        /* Success/Error message styling */
        .success-message {
            background: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #28a745;
            margin: 1rem 0;
        }
        
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #dc3545;
            margin: 1rem 0;
        }
        
        /* Authentication required overlay */
        .auth-required-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.95);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
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
            
            .fab-button {
                width: 64px;
                height: 64px;
                font-size: 28px;
                bottom: 1rem;
                right: 1rem;
            }
            
            .term-explanation {
                max-width: 250px;
                font-size: 11px;
            }
        }
        
        /* Hide Streamlit elements until authenticated */
        .main .block-container {
            padding-top: 1rem;
        }
        
        /* Sidebar styling - only show when authenticated */
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
    
    # Selected campaign for viewing/donating
    if 'selected_campaign' not in st.session_state:
        st.session_state.selected_campaign = None
    
    # Registration step tracking
    if 'registration_step' not in st.session_state:
        st.session_state.registration_step = 1
    
    # Feature flags
    if 'features' not in st.session_state:
        st.session_state.features = {
            'oauth_enabled': os.getenv('OAUTH_ENABLED', 'true').lower() == 'true',
            'registration_enabled': os.getenv('FEATURES_REGISTRATION_ENABLED', 'true').lower() == 'true',
            'campaign_creation_enabled': os.getenv('FEATURES_CAMPAIGN_CREATION_ENABLED', 'true').lower() == 'true',
            'simplification_enabled': os.getenv('SIMPLIFICATION_ENABLED', 'true').lower() == 'true'
        }

def show_authentication_required():
    """Show authentication required message"""
    
    st.markdown("""
    <div class='main-header'>
        <h1>🏠 Welcome to Haven</h1>
        <p>Empowering Communities Through Crowdfunding</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='error-message'>
        <h3>🔒 Authentication Required</h3>
        <p>You must be registered and logged in to access the Haven platform.</p>
        <p><strong>Process:</strong> Registration → Database Storage → Login → Access</p>
    </div>
    """, unsafe_allow_html=True)

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
        st.warning("🔒 OAuth authentication is currently disabled. Please contact the administrator.")
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
    
    st.info("💡 **Important**: You must be registered in our database before you can log in. If you're new, please use the Register tab first.")
    
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
            st.experimental_rerun()
    
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
            st.experimental_rerun()
    
    # Show OAuth buttons if role is selected
    if st.session_state.get("selected_role"):
        st.markdown("---")
        st.markdown(f"### 🔐 Login as {st.session_state.selected_role.title()}")
        
        st.warning("⚠️ **Database Check**: We will verify that you exist in our database before allowing login.")
        
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
            st.experimental_rerun()

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
                st.info("🔄 OAuth window opened. Please complete authentication and return to this page.")
    
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
                st.info("🔄 OAuth window opened. Please complete authentication and return to this page.")

def generate_oauth_url(provider: str, user_type: str) -> Optional[str]:
    """Generate OAuth URL for the specified provider"""
    
    try:
        backend_url = os.getenv('BACKEND_URL', 'https://haven-backend-9lw3.onrender.com')
        frontend_url = os.getenv('FRONTEND_URL', 'https://haven-frontend-65jr.onrender.com')
        
        # Create state parameter with provider and user_type
        import json
        state = json.dumps({
            'provider': provider,
            'user_type': user_type,
            'timestamp': datetime.now().isoformat()
        })
        
        oauth_url = f"{backend_url}/api/v1/auth/{provider}/login"
        oauth_url += f"?user_type={user_type}&state={state}&redirect_uri={frontend_url}"
        
        return oauth_url
        
    except Exception as e:
        logger.error(f"Error generating OAuth URL: {e}")
        st.error(f"❌ Error generating OAuth URL: {str(e)}")
        return None

def show_registration_tab():
    """Show registration tab with proper database integration"""
    
    if not st.session_state.features.get('registration_enabled', True):
        st.warning("📝 Registration is currently disabled. Please contact the administrator.")
        return
    
    st.markdown("### 📝 New to Haven? Register Now!")
    
    st.info("💡 **Registration Process**: Your details will be stored in our database first, then you can log in using OAuth.")
    
    # Use updated registration workflow
    try:
        show_registration_page()
    except Exception as e:
        logger.error(f"Registration page error: {e}")
        st.error("❌ Registration system temporarily unavailable. Please try again later.")

def show_authenticated_app():
    """Show main application for authenticated users with navbar"""
    
    # Verify authentication with database
    if not check_authentication():
        st.error("❌ Authentication verification failed. Please log in again.")
        logout_user()
        st.experimental_rerun()
        return
    
    # Get user information
    user_data = get_current_user()
    user_type = get_current_user_type()
    
    if not user_data or not user_type:
        st.error("❌ User data not found. Please log in again.")
        logout_user()
        st.experimental_rerun()
        return
    
    # Show sidebar navigation (now visible after authentication)
    with st.sidebar:
        show_sidebar_navigation(user_data, user_type)
    
    # Main content area
    show_main_content(user_type)
    
    # Floating action button for organizations
    if user_type == 'organization' and st.session_state.features.get('campaign_creation_enabled', True):
        show_floating_action_button()

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
        show_organization_navigation()
    else:  # individual
        show_individual_navigation()
    
    st.markdown("---")
    
    # Simplification toggle
    if st.session_state.features.get('simplification_enabled', True):
        st.markdown("### 🔤 Text Simplification")
        
        simplify_enabled = st.checkbox(
            "Enable term simplification", 
            value=st.session_state.get('simplification_active', False),
            help="Show simplified terms with explanations"
        )
        st.session_state.simplification_active = simplify_enabled
        
        if simplify_enabled:
            st.info("💡 Look for 'i' icons next to simplified terms!")
    
    st.markdown("---")
    
    # Settings and logout
    st.markdown("### ⚙️ Settings")
    
    if st.button("👤 Profile Settings", use_container_width=True):
        st.session_state.current_page = 'profile'
        st.experimental_rerun()
    
    if st.button("🔔 Notifications", use_container_width=True):
        st.session_state.current_page = 'notifications'
        st.experimental_rerun()
    
    if st.button("❓ Help & Support", use_container_width=True):
        st.session_state.current_page = 'help'
        st.experimental_rerun()
    
    st.markdown("---")
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        logout_user()
        st.experimental_rerun()

def show_organization_navigation():
    """Show navigation menu for organizations"""
    
    nav_items = [
        ("🏠 Dashboard", "dashboard"),
        ("🚀 Create Campaign", "create_campaign"),
        ("📊 My Campaigns", "my_campaigns"),
        ("💰 Donations Received", "donations_received"),
        ("📈 Analytics", "analytics"),
        ("🔍 Browse All Campaigns", "browse_campaigns")
    ]
    
    for label, page_key in nav_items:
        if st.button(label, key=f"nav_{page_key}", use_container_width=True):
            st.session_state.current_page = page_key
            st.experimental_rerun()

def show_individual_navigation():
    """Show navigation menu for individuals"""
    
    nav_items = [
        ("🏠 Dashboard", "dashboard"),
        ("🔍 Browse Campaigns", "browse_campaigns"),
        ("💝 My Donations", "my_donations"),
        ("❤️ Favorite Campaigns", "favorites"),
        ("📊 Impact Report", "impact_report")
    ]
    
    for label, page_key in nav_items:
        if st.button(label, key=f"nav_{page_key}", use_container_width=True):
            st.session_state.current_page = page_key
            st.experimental_rerun()

def show_main_content(user_role: str):
    """Show main content based on current page and user role"""
    
    current_page = st.session_state.get('current_page', 'dashboard')
    
    try:
        if current_page == 'dashboard':
            show_dashboard(user_role)
        elif current_page == 'create_campaign' and user_role == 'organization':
            if require_role('organization'):
                render_create_campaign_page(None)
        elif current_page == 'browse_campaigns':
            render_campaign_browse_page(None)
        elif current_page == 'campaign_details':
            render_campaign_details_page(None)
        elif current_page == 'donation':
            if require_role('individual'):
                render_donation_page(None)
        elif current_page == 'my_campaigns' and user_role == 'organization':
            if require_role('organization'):
                show_my_campaigns()
        elif current_page == 'my_donations' and user_role == 'individual':
            if require_role('individual'):
                show_my_donations()
        elif current_page == 'profile':
            show_profile_settings()
        elif current_page == 'analytics' and user_role == 'organization':
            if require_role('organization'):
                show_analytics()
        elif current_page == 'help':
            show_help_support()
        else:
            show_dashboard(user_role)
            
    except Exception as e:
        logger.error(f"Error showing page {current_page}: {e}")
        st.error(f"❌ Error loading page: {str(e)}")
        st.info("🔄 Please try navigating to a different page or refresh the application.")

def show_dashboard(user_role: str):
    """Show role-specific dashboard with term simplification"""
    
    dashboard_title = f"🏠 {user_role.title()} Dashboard"
    dashboard_subtitle = "Welcome to your Haven dashboard"
    
    # Apply term simplification if enabled
    if st.session_state.get('simplification_active', False):
        dashboard_subtitle = apply_term_simplification(dashboard_subtitle)
    
    st.markdown(f"""
    <div class='main-header'>
        <h1>{dashboard_title}</h1>
        <p>{dashboard_subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if user_role == 'organization':
        show_organization_dashboard()
    else:
        show_individual_dashboard()

def apply_term_simplification(text: str) -> str:
    """Apply term simplification with 'i' icons"""
    
    if not st.session_state.get('simplification_active', False):
        return text
    
    # Example simplifications (in real app, this would call the backend API)
    simplifications = {
        'dashboard': {
            'simplified': 'control panel',
            'explanation': 'A control panel where you can see important information and manage your account'
        },
        'crowdfunding': {
            'simplified': 'group funding',
            'explanation': 'When many people give small amounts of money to support a project or cause'
        },
        'campaign': {
            'simplified': 'fundraising project',
            'explanation': 'A specific project or cause that is asking for money donations'
        }
    }
    
    result_text = text
    for original, data in simplifications.items():
        if original.lower() in text.lower():
            simplified = data['simplified']
            explanation = data['explanation']
            
            # Create HTML with 'i' icon and hover explanation
            replacement = f"""
            <span class="simplified-term">
                {simplified}
                <i class="material-icons info-icon">info</i>
                <div class="term-explanation">{explanation}</div>
            </span>
            """
            
            result_text = result_text.replace(original, replacement)
    
    return result_text

def show_organization_dashboard():
    """Show dashboard for organizations with term simplification"""
    
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
    
    # Recent activity with simplification
    activity_title = "📈 Recent Activity"
    if st.session_state.get('simplification_active', False):
        activity_title = apply_term_simplification(activity_title)
    
    st.markdown(f"### {activity_title}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        recent_donations_text = """
        **Recent Donations:**
        - $100 from Anonymous Donor - 2 hours ago
        - $50 from John Smith - 5 hours ago
        - $250 from Community Foundation - 1 day ago
        - $75 from Sarah Johnson - 2 days ago
        """
        
        if st.session_state.get('simplification_active', False):
            recent_donations_text = apply_term_simplification(recent_donations_text)
        
        st.markdown(recent_donations_text, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Quick Actions:**")
        
        if st.button("🚀 Create New Campaign", use_container_width=True, type="primary"):
            st.session_state.current_page = 'create_campaign'
            st.experimental_rerun()
        
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.current_page = 'analytics'
            st.experimental_rerun()
        
        if st.button("💌 Send Update", use_container_width=True):
            st.info("📧 Campaign update feature coming soon!")

def show_individual_dashboard():
    """Show dashboard for individuals with term simplification"""
    
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
    
    # Featured campaigns with simplification
    campaigns_title = "🌟 Featured Campaigns"
    if st.session_state.get('simplification_active', False):
        campaigns_title = apply_term_simplification(campaigns_title)
    
    st.markdown(f"### {campaigns_title}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        campaign1_text = """
        <div class='role-card'>
            <h4>🏥 Emergency Medical Fund</h4>
            <p>Help provide emergency medical care for children in need.</p>
            <p><strong>Progress:</strong> $37,500 / $50,000 (75%)</p>
        </div>
        """
        
        if st.session_state.get('simplification_active', False):
            campaign1_text = apply_term_simplification(campaign1_text)
        
        st.markdown(campaign1_text, unsafe_allow_html=True)
        
        if st.button("💝 Donate Now", key="donate_medical", use_container_width=True, type="primary"):
            st.session_state.current_page = 'browse_campaigns'
            st.experimental_rerun()
    
    with col2:
        campaign2_text = """
        <div class='role-card'>
            <h4>🌱 Clean Water Initiative</h4>
            <p>Building clean water wells in remote villages.</p>
            <p><strong>Progress:</strong> $45,000 / $75,000 (60%)</p>
        </div>
        """
        
        if st.session_state.get('simplification_active', False):
            campaign2_text = apply_term_simplification(campaign2_text)
        
        st.markdown(campaign2_text, unsafe_allow_html=True)
        
        if st.button("💝 Support Cause", key="donate_water", use_container_width=True, type="primary"):
            st.session_state.current_page = 'browse_campaigns'
            st.experimental_rerun()

def show_floating_action_button():
    """Show floating action button for creating campaigns"""
    
    st.markdown("""
    <div class='fab-button' onclick='createCampaign()' title='Create Campaign'>
        <i class="material-icons">add</i>
    </div>
    
    <script>
    function createCampaign() {
        // This would trigger the create campaign page
        window.location.href = window.location.href + '?page=create_campaign';
    }
    </script>
    """, unsafe_allow_html=True)

def show_my_campaigns():
    """Show organization's campaigns"""
    st.markdown("### 📊 My Campaigns")
    st.info("📊 Campaign management features coming soon!")

def show_my_donations():
    """Show individual's donation history"""
    st.markdown("### 💝 My Donation History")
    st.info("💝 Donation history features coming soon!")

def show_profile_settings():
    """Show profile settings page"""
    st.markdown("### 👤 Profile Settings")
    st.info("👤 Profile settings coming soon!")

def show_analytics():
    """Show analytics page for organizations"""
    st.markdown("### 📊 Campaign Analytics")
    st.info("📊 Analytics features coming soon!")

def show_help_support():
    """Show help and support page"""
    st.markdown("### ❓ Help & Support")
    st.info("❓ Help and support features coming soon!")

def main():
    """Main application function with corrected authentication flow"""
    
    try:
        # Add custom CSS and simplification styles
        add_custom_css()
        add_simplification_styles()
        
        # Initialize session state
        initialize_session_state()
        
        # Handle OAuth callback first (this checks database)
        oauth_result = handle_oauth_callback()
        if oauth_result:
            st.success("✅ OAuth authentication successful!")
            st.experimental_rerun()
        
        # Check authentication status with database verification
        if check_authentication():
            # User is authenticated and exists in database - show full app
            show_authenticated_app()
        else:
            # User is not authenticated - show login/registration only
            show_login_page()
            
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"❌ Application error: {str(e)}")
        st.info("🔄 Please refresh the page or contact support if the issue persists.")

if __name__ == "__main__":
    main()

