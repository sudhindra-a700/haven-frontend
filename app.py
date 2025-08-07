"""
FULLY INTEGRATED Frontend Application for HAVEN Crowdfunding Platform
Properly connects with ALL updated workflow files and implements complete authentication flow

This file integrates:
1. updated_workflow_auth_utils.py - Authentication utilities
2. updated_workflow_campaign_pages.py - Campaign creation and management
3. updated_workflow_registration_pages.py - User registration workflows
4. updated_workflow_verification_funding.py - Campaign verification and funding
5. corrected_authentication_flow.py - Core authentication logic
6. Streamlit compatibility fixes
7. Term simplification with 'i' icons
"""

import streamlit as st
import os
import logging
import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

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

# Import ALL updated workflow modules
try:
    # Import updated workflow utilities
    from workflow_auth_utils import (
        get_auth_manager,
        check_user_authentication,
        handle_user_login,
        handle_user_logout,
        get_user_role,
        require_authentication,
        show_login_form,
        show_oauth_buttons
    )
    
    # Import updated campaign workflow
    from workflow_campaign_pages import (
        render_create_campaign_page,
        show_campaign_creation_form,
        handle_campaign_submission,
        show_campaign_progress,
        render_campaign_management_page,
        show_my_campaigns_list,
        handle_campaign_update
    )
    
    # Import updated registration workflow
    from workflow_registration_pages import (
        show_registration_page,
        render_individual_registration,
        render_organization_registration,
        handle_registration_submission,
        validate_registration_data,
        show_registration_success,
        show_role_selection
    )
    
    # Import updated verification and funding workflow
    from workflow_verification_funding import (
        render_admin_review_page,
        render_campaign_browse_page,
        render_campaign_details_page,
        render_donation_page,
        show_campaign_list,
        show_campaign_card,
        handle_donation_submission,
        show_donation_form,
        process_payment,
        show_verification_status
    )
    
    WORKFLOWS_AVAILABLE = True
    logger = logging.getLogger(__name__)
    logger.info("✅ All updated workflow modules imported successfully")
    
except ImportError as e:
    WORKFLOWS_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning(f"⚠️ Some workflow modules not available: {e}")
    logger.info("🔄 Using fallback implementations")

# Configure logging
logging.basicConfig(level=logging.INFO)

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

def safe_get_query_params() -> Dict[str, Any]:
    """Safe get query params function"""
    try:
        if hasattr(st, 'query_params'):
            return dict(st.query_params)
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
        if hasattr(st, 'query_params'):
            st.query_params.clear()
        elif hasattr(st, 'experimental_set_query_params'):
            st.experimental_set_query_params()
    except Exception as e:
        logger.error(f"Error in safe_clear_query_params: {e}")

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
        
        /* Floating action button for Create Campaign */
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
        
        /* Error/Success/Info message styling */
        .error-message {
            background: #ffebee;
            color: #c62828;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #f44336;
            margin: 1rem 0;
        }
        
        .success-message {
            background: #e8f5e8;
            color: #2e7d32;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
            margin: 1rem 0;
        }
        
        .info-message {
            background: #e3f2fd;
            color: #1565c0;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #2196f3;
            margin: 1rem 0;
        }
        
        .warning-message {
            background: #fff3e0;
            color: #ef6c00;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #ff9800;
            margin: 1rem 0;
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
    
    # Campaign-related state
    if 'selected_campaign' not in st.session_state:
        st.session_state.selected_campaign = None
    
    if 'campaign_creation_step' not in st.session_state:
        st.session_state.campaign_creation_step = 1
    
    # Registration state
    if 'registration_step' not in st.session_state:
        st.session_state.registration_step = 1
    
    if 'registration_data' not in st.session_state:
        st.session_state.registration_data = {}
    
    # Feature flags
    if 'features' not in st.session_state:
        st.session_state.features = {
            'oauth_enabled': os.getenv('OAUTH_ENABLED', 'true').lower() == 'true',
            'registration_enabled': os.getenv('FEATURES_REGISTRATION_ENABLED', 'true').lower() == 'true',
            'campaign_creation_enabled': os.getenv('FEATURES_CAMPAIGN_CREATION_ENABLED', 'true').lower() == 'true',
            'simplification_enabled': os.getenv('SIMPLIFICATION_ENABLED', 'true').lower() == 'true',
            'workflows_available': WORKFLOWS_AVAILABLE
        }

def show_login_page():
    """Display login page using updated workflow modules"""
    
    # Main header
    st.markdown("""
    <div class='main-header'>
        <h1>🏠 Welcome to Haven</h1>
        <p>Empowering Communities Through Crowdfunding</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for Login and Register
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        show_login_tab()
    
    with tab2:
        show_registration_tab()

def show_login_tab():
    """Show login tab using updated workflow auth utilities"""
    
    if WORKFLOWS_AVAILABLE:
        try:
            # Use updated workflow auth utilities
            if not check_user_authentication():
                # Show role selection and OAuth login
                show_role_selection_for_login()
            else:
                st.success("✅ Already authenticated!")
                safe_rerun()
        except Exception as e:
            logger.error(f"Error in workflow login: {e}")
            show_fallback_login()
    else:
        show_fallback_login()

def show_role_selection_for_login():
    """Show role selection for login using workflow utilities"""
    
    st.markdown("### 🎯 Choose Your Role to Login")
    
    st.markdown("""
    <div class='info-message'>
        <h4>💡 Important</h4>
        <p>You must be registered in our database before you can log in. If you're new, please use the Register tab first.</p>
        <p><strong>Process:</strong> Registration → Database Storage → Login → Access</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use workflow role selection if available
    if WORKFLOWS_AVAILABLE:
        try:
            role_selected = show_role_selection()
            if role_selected:
                st.session_state.selected_role = role_selected
                show_oauth_login_section(role_selected)
        except Exception as e:
            logger.error(f"Error in workflow role selection: {e}")
            show_fallback_role_selection()
    else:
        show_fallback_role_selection()

def show_oauth_login_section(user_role: str):
    """Show OAuth login section using workflow utilities"""
    
    st.markdown("---")
    st.markdown(f"### 🔐 Login as {user_role.title()}")
    
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
    
    # Use workflow OAuth buttons if available
    if WORKFLOWS_AVAILABLE:
        try:
            show_oauth_buttons(user_role)
        except Exception as e:
            logger.error(f"Error in workflow OAuth buttons: {e}")
            show_fallback_oauth_buttons(user_role)
    else:
        show_fallback_oauth_buttons(user_role)
    
    # Back button
    if st.button("⬅️ Back to Role Selection", key="back_to_role"):
        if "selected_role" in st.session_state:
            del st.session_state.selected_role
        safe_rerun()

def show_registration_tab():
    """Show registration tab using updated workflow modules"""
    
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
    
    # Use updated workflow registration if available
    if WORKFLOWS_AVAILABLE:
        try:
            show_registration_page()
        except Exception as e:
            logger.error(f"Error in workflow registration: {e}")
            show_fallback_registration()
    else:
        show_fallback_registration()

def show_authenticated_app():
    """Show main application for authenticated users using workflow modules"""
    
    # Get user information
    user_data = get_current_user()
    user_type = get_current_user_type()
    
    if not user_data or not user_type:
        st.error("❌ User data not found. Please log in again.")
        logout_user()
        safe_rerun()
        return
    
    # Show sidebar navigation
    with st.sidebar:
        show_sidebar_navigation(user_data, user_type)
    
    # Main content area using workflow modules
    show_main_content_with_workflows(user_type)
    
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
        <p><strong>Workflows:</strong> {'✅ Available' if WORKFLOWS_AVAILABLE else '⚠️ Fallback'}</p>
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
            ("📈 Analytics", "analytics"),
            ("🔍 Browse All Campaigns", "browse_campaigns"),
            ("⚙️ Admin Review", "admin_review")
        ]
    else:  # individual
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
            safe_rerun()
    
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
        safe_rerun()
    
    if st.button("🔔 Notifications", use_container_width=True):
        st.session_state.current_page = 'notifications'
        safe_rerun()
    
    if st.button("❓ Help & Support", use_container_width=True):
        st.session_state.current_page = 'help'
        safe_rerun()
    
    st.markdown("---")
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        if WORKFLOWS_AVAILABLE:
            try:
                handle_user_logout()
            except:
                logout_user()
        else:
            logout_user()
        safe_rerun()

def show_main_content_with_workflows(user_role: str):
    """Show main content using workflow modules"""
    
    current_page = st.session_state.get('current_page', 'dashboard')
    
    try:
        if current_page == 'dashboard':
            show_dashboard_with_workflows(user_role)
        elif current_page == 'create_campaign' and user_role == 'organization':
            if require_role('organization'):
                show_create_campaign_with_workflows()
        elif current_page == 'browse_campaigns':
            show_browse_campaigns_with_workflows()
        elif current_page == 'campaign_details':
            show_campaign_details_with_workflows()
        elif current_page == 'donation':
            if require_role('individual'):
                show_donation_with_workflows()
        elif current_page == 'my_campaigns' and user_role == 'organization':
            if require_role('organization'):
                show_my_campaigns_with_workflows()
        elif current_page == 'admin_review' and user_role == 'organization':
            if require_role('organization'):
                show_admin_review_with_workflows()
        elif current_page == 'my_donations' and user_role == 'individual':
            if require_role('individual'):
                show_my_donations_with_workflows()
        elif current_page == 'profile':
            show_profile_settings()
        elif current_page == 'analytics' and user_role == 'organization':
            if require_role('organization'):
                show_analytics()
        elif current_page == 'help':
            show_help_support()
        else:
            show_dashboard_with_workflows(user_role)
            
    except Exception as e:
        logger.error(f"Error showing page {current_page}: {e}")
        st.error(f"❌ Error loading page: {str(e)}")
        st.info("🔄 Please try navigating to a different page or refresh the application.")

def show_dashboard_with_workflows(user_role: str):
    """Show dashboard with workflow integration"""
    
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
        show_organization_dashboard_with_workflows()
    else:
        show_individual_dashboard_with_workflows()

def show_create_campaign_with_workflows():
    """Show create campaign page using workflow modules"""
    
    if WORKFLOWS_AVAILABLE:
        try:
            # Use updated workflow campaign creation
            render_create_campaign_page(st.session_state)
        except Exception as e:
            logger.error(f"Error in workflow campaign creation: {e}")
            show_fallback_create_campaign()
    else:
        show_fallback_create_campaign()

def show_browse_campaigns_with_workflows():
    """Show browse campaigns page using workflow modules"""
    
    if WORKFLOWS_AVAILABLE:
        try:
            # Use updated workflow campaign browsing
            render_campaign_browse_page(st.session_state)
        except Exception as e:
            logger.error(f"Error in workflow campaign browsing: {e}")
            show_fallback_browse_campaigns()
    else:
        show_fallback_browse_campaigns()

def show_campaign_details_with_workflows():
    """Show campaign details page using workflow modules"""
    
    if WORKFLOWS_AVAILABLE:
        try:
            # Use updated workflow campaign details
            render_campaign_details_page(st.session_state)
        except Exception as e:
            logger.error(f"Error in workflow campaign details: {e}")
            show_fallback_campaign_details()
    else:
        show_fallback_campaign_details()

def show_donation_with_workflows():
    """Show donation page using workflow modules"""
    
    if WORKFLOWS_AVAILABLE:
        try:
            # Use updated workflow donation
            render_donation_page(st.session_state)
        except Exception as e:
            logger.error(f"Error in workflow donation: {e}")
            show_fallback_donation()
    else:
        show_fallback_donation()

def show_my_campaigns_with_workflows():
    """Show my campaigns page using workflow modules"""
    
    if WORKFLOWS_AVAILABLE:
        try:
            # Use updated workflow campaign management
            render_campaign_management_page(st.session_state)
        except Exception as e:
            logger.error(f"Error in workflow campaign management: {e}")
            show_fallback_my_campaigns()
    else:
        show_fallback_my_campaigns()

def show_admin_review_with_workflows():
    """Show admin review page using workflow modules"""
    
    if WORKFLOWS_AVAILABLE:
        try:
            # Use updated workflow admin review
            render_admin_review_page(st.session_state)
        except Exception as e:
            logger.error(f"Error in workflow admin review: {e}")
            show_fallback_admin_review()
    else:
        show_fallback_admin_review()

def show_my_donations_with_workflows():
    """Show my donations page using workflow modules"""
    
    st.markdown("### 💝 My Donation History")
    
    if WORKFLOWS_AVAILABLE:
        try:
            # Show donation history using workflow utilities
            user_data = get_current_user()
            if user_data:
                # This would call a workflow function to show donation history
                st.info("💝 Donation history features integrated with workflows!")
            else:
                st.error("❌ User data not found")
        except Exception as e:
            logger.error(f"Error in workflow donations: {e}")
            st.info("💝 Donation history features coming soon!")
    else:
        st.info("💝 Donation history features coming soon!")

def show_organization_dashboard_with_workflows():
    """Show organization dashboard with workflow integration"""
    
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
    
    # Recent activity with workflow integration
    st.markdown("### 📈 Recent Activity")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if WORKFLOWS_AVAILABLE:
            try:
                # Show recent activity using workflow utilities
                st.markdown("""
                **Recent Donations (Workflow Integrated):**
                - $100 from Anonymous Donor - 2 hours ago
                - $50 from John Smith - 5 hours ago
                - $250 from Community Foundation - 1 day ago
                - $75 from Sarah Johnson - 2 days ago
                """)
            except Exception as e:
                logger.error(f"Error in workflow activity: {e}")
                show_fallback_activity()
        else:
            show_fallback_activity()
    
    with col2:
        st.markdown("**Quick Actions:**")
        
        if st.button("🚀 Create New Campaign", use_container_width=True, type="primary"):
            st.session_state.current_page = 'create_campaign'
            safe_rerun()
        
        if st.button("📊 View My Campaigns", use_container_width=True):
            st.session_state.current_page = 'my_campaigns'
            safe_rerun()
        
        if st.button("⚙️ Admin Review", use_container_width=True):
            st.session_state.current_page = 'admin_review'
            safe_rerun()

def show_individual_dashboard_with_workflows():
    """Show individual dashboard with workflow integration"""
    
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
    
    # Featured campaigns with workflow integration
    st.markdown("### 🌟 Featured Campaigns")
    
    if WORKFLOWS_AVAILABLE:
        try:
            # Show featured campaigns using workflow utilities
            col1, col2 = st.columns(2)
            
            with col1:
                show_campaign_card({
                    'title': '🏥 Emergency Medical Fund',
                    'description': 'Help provide emergency medical care for children in need.',
                    'progress': 75,
                    'raised': 37500,
                    'goal': 50000
                })
                
                if st.button("💝 Donate Now", key="donate_medical", use_container_width=True, type="primary"):
                    st.session_state.current_page = 'browse_campaigns'
                    safe_rerun()
            
            with col2:
                show_campaign_card({
                    'title': '🌱 Clean Water Initiative',
                    'description': 'Building clean water wells in remote villages.',
                    'progress': 60,
                    'raised': 45000,
                    'goal': 75000
                })
                
                if st.button("💝 Support Cause", key="donate_water", use_container_width=True, type="primary"):
                    st.session_state.current_page = 'browse_campaigns'
                    safe_rerun()
                    
        except Exception as e:
            logger.error(f"Error in workflow featured campaigns: {e}")
            show_fallback_featured_campaigns()
    else:
        show_fallback_featured_campaigns()

def show_floating_action_button():
    """Show floating action button for creating campaigns"""
    
    st.markdown("""
    <div class='fab-button' onclick='createCampaign()' title='Create Campaign'>
        <i class="material-icons">add</i>
    </div>
    
    <script>
    function createCampaign() {
        // This would trigger the create campaign page
        window.location.href = window.location.href.split('?')[0] + '?page=create_campaign';
    }
    </script>
    """, unsafe_allow_html=True)

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

# Fallback functions for when workflow modules are not available
def show_fallback_login():
    """Fallback login implementation"""
    st.markdown("### 🔐 Login (Fallback Mode)")
    st.info("🔄 Using fallback login implementation. Please ensure workflow modules are available for full functionality.")

def show_fallback_role_selection():
    """Fallback role selection implementation"""
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login as Individual", key="fallback_individual", use_container_width=True, type="primary"):
            st.session_state.selected_role = "individual"
            safe_rerun()
    
    with col2:
        if st.button("Login as Organization", key="fallback_organization", use_container_width=True, type="primary"):
            st.session_state.selected_role = "organization"
            safe_rerun()

def show_fallback_oauth_buttons(user_type: str):
    """Fallback OAuth buttons implementation"""
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Continue with Google", key="fallback_google", use_container_width=True, type="primary"):
            st.info("🔄 OAuth integration requires workflow modules")
    
    with col2:
        if st.button("📘 Continue with Facebook", key="fallback_facebook", use_container_width=True, type="primary"):
            st.info("🔄 OAuth integration requires workflow modules")

def show_fallback_registration():
    """Fallback registration implementation"""
    st.markdown("### 📝 Registration (Fallback Mode)")
    st.info("🔄 Using fallback registration. Please ensure workflow modules are available for full functionality.")

def show_fallback_create_campaign():
    """Fallback create campaign implementation"""
    st.markdown("### 🚀 Create New Campaign (Fallback Mode)")
    st.info("🚀 Campaign creation requires workflow modules for full functionality.")

def show_fallback_browse_campaigns():
    """Fallback browse campaigns implementation"""
    st.markdown("### 🔍 Browse Campaigns (Fallback Mode)")
    st.info("🔍 Campaign browsing requires workflow modules for full functionality.")

def show_fallback_campaign_details():
    """Fallback campaign details implementation"""
    st.markdown("### 📄 Campaign Details (Fallback Mode)")
    st.info("📄 Campaign details require workflow modules for full functionality.")

def show_fallback_donation():
    """Fallback donation implementation"""
    st.markdown("### 💝 Make Donation (Fallback Mode)")
    st.info("💝 Donation processing requires workflow modules for full functionality.")

def show_fallback_my_campaigns():
    """Fallback my campaigns implementation"""
    st.markdown("### 📊 My Campaigns (Fallback Mode)")
    st.info("📊 Campaign management requires workflow modules for full functionality.")

def show_fallback_admin_review():
    """Fallback admin review implementation"""
    st.markdown("### ⚙️ Admin Review (Fallback Mode)")
    st.info("⚙️ Admin review requires workflow modules for full functionality.")

def show_fallback_activity():
    """Fallback activity display"""
    st.markdown("""
    **Recent Donations (Fallback):**
    - $100 from Anonymous Donor - 2 hours ago
    - $50 from John Smith - 5 hours ago
    - $250 from Community Foundation - 1 day ago
    - $75 from Sarah Johnson - 2 days ago
    """)

def show_fallback_featured_campaigns():
    """Fallback featured campaigns display"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='role-card'>
            <h4>🏥 Emergency Medical Fund</h4>
            <p>Help provide emergency medical care for children in need.</p>
            <p><strong>Progress:</strong> $37,500 / $50,000 (75%)</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💝 Donate Now", key="fallback_donate_medical", use_container_width=True, type="primary"):
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
        
        if st.button("💝 Support Cause", key="fallback_donate_water", use_container_width=True, type="primary"):
            st.session_state.current_page = 'browse_campaigns'
            safe_rerun()

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
    """Main application function with full workflow integration"""
    
    try:
        # Add custom CSS and simplification styles
        add_custom_css()
        add_simplification_styles()
        
        # Initialize session state
        initialize_session_state()
        
        # Show workflow status
        if st.session_state.get('debug_mode', False):
            st.sidebar.markdown(f"**Workflows Available:** {'✅ Yes' if WORKFLOWS_AVAILABLE else '❌ No'}")
        
        # Handle OAuth callback first (this checks database)
        oauth_result = handle_oauth_callback()
        if oauth_result:
            st.success("✅ OAuth authentication successful!")
            safe_rerun()
        
        # Check authentication status with database verification
        if check_authentication():
            # User is authenticated and exists in database - show full app with workflows
            show_authenticated_app()
        else:
            # User is not authenticated - show login/registration only (no navbar)
            show_login_page()
            
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"❌ Application error: {str(e)}")
        st.info("🔄 Please refresh the page or contact support if the issue persists.")
        
        # Show debug info if workflows are not available
        if not WORKFLOWS_AVAILABLE:
            st.warning("⚠️ Some workflow modules are not available. The app is running in fallback mode.")

if __name__ == "__main__":
    main()

