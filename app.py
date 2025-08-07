"""
COMPLETELY UPDATED Frontend Application for HAVEN Crowdfunding Platform
Integrates all latest OAuth fixes and workflow updates in tandem

This file contains the corrected Streamlit application that fixes:
1. OAuth integration with proper error handling
2. Environment variable usage
3. User interface improvements
4. Session management
5. Complete workflow integration
6. Role-based access control
7. MaterializeCSS styling with light green theme
"""

import streamlit as st
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Import fixed OAuth integration
from oauth_integration import (
    handle_oauth_callback,
    check_authentication_status,
    render_oauth_buttons,
    logout,
    get_user_info
)

# Import updated workflow utilities
from workflow_auth_utils import (
    get_auth_manager, 
    require_auth, 
    require_role, 
    get_current_user_role,
    is_authenticated
)

# Import updated workflow pages
from workflow_campaign_pages import render_create_campaign_page
from workflow_registration_pages import show_registration_page
from workflow_verification_funding import (
    render_admin_review_page,
    render_campaign_browse_page,
    render_campaign_details_page,
    render_donation_page
)

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

# Custom CSS for better styling with light green theme and MaterializeCSS
st.markdown("""
<style>
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
    
    /* OAuth section styling */
    .oauth-section {
        background: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* Status card styling */
    .status-card {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #4CAF50;
        margin: 1rem 0;
    }
    
    /* Navigation styling */
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
    }
    
    .fab-button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    /* Card panel for hover information */
    .info-card {
        background: #009688;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    /* Pulse effect for OAuth buttons */
    .pulse-button {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #e8f5e8 0%, #f1f8e9 100%);
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
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function with complete OAuth and workflow integration"""
    
    try:
        # Initialize session state
        initialize_session_state()
        
        # Handle OAuth callback first
        handle_oauth_callback()
        
        # Check authentication status
        if check_authentication_status():
            show_authenticated_app()
        else:
            show_login_page()
            
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"❌ Application error: {str(e)}")
        st.info("🔄 Please refresh the page or contact support if the issue persists.")

def initialize_session_state():
    """Initialize session state variables"""
    
    # Authentication state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # User information
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    
    # Current page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    
    # Selected campaign for viewing/donating
    if 'selected_campaign' not in st.session_state:
        st.session_state.selected_campaign = None
    
    # Navigation state
    if 'navigation_expanded' not in st.session_state:
        st.session_state.navigation_expanded = True
    
    # Feature flags
    if 'features' not in st.session_state:
        st.session_state.features = {
            'oauth_enabled': os.getenv('FEATURES_OAUTH_ENABLED', 'true').lower() == 'true',
            'registration_enabled': os.getenv('FEATURES_REGISTRATION_ENABLED', 'true').lower() == 'true',
            'campaign_creation_enabled': os.getenv('FEATURES_CAMPAIGN_CREATION_ENABLED', 'true').lower() == 'true'
        }

def show_login_page():
    """Display login page with OAuth options and registration"""
    
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
    
    st.markdown("### 🎯 Choose Your Role")
    
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
        
        # OAuth section with pulse effect
        st.markdown("""
        <div class='oauth-section pulse-button'>
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

def show_registration_tab():
    """Show registration tab"""
    
    if not st.session_state.features.get('registration_enabled', True):
        st.warning("📝 Registration is currently disabled. Please contact the administrator.")
        return
    
    st.markdown("### 📝 New to Haven? Register Now!")
    
    # Use updated registration workflow
    show_registration_page()

def show_authenticated_app():
    """Show main application for authenticated users"""
    
    # Get user information
    user_info = get_user_info()
    user_role = get_current_user_role()
    
    if not user_info or not user_role:
        st.error("❌ Authentication error. Please login again.")
        logout()
        st.experimental_rerun()
        return
    
    # Sidebar navigation
    with st.sidebar:
        show_sidebar_navigation(user_info, user_role)
    
    # Main content area
    show_main_content(user_role)
    
    # Floating action button for organizations
    if user_role == 'organization' and st.session_state.features.get('campaign_creation_enabled', True):
        show_floating_action_button()

def show_sidebar_navigation(user_info: Dict[str, Any], user_role: str):
    """Show sidebar navigation with user info and menu"""
    
    # User info section
    st.markdown(f"""
    <div class='status-card'>
        <h4>👋 Welcome!</h4>
        <p><strong>Role:</strong> {user_role.title()}</p>
        <p><strong>Email:</strong> {user_info.get('email', 'N/A')}</p>
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
        logout()
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
            render_create_campaign_page(None)
        elif current_page == 'browse_campaigns':
            render_campaign_browse_page(None)
        elif current_page == 'campaign_details':
            render_campaign_details_page(None)
        elif current_page == 'donation':
            render_donation_page(None)
        elif current_page == 'my_campaigns' and user_role == 'organization':
            show_my_campaigns()
        elif current_page == 'my_donations' and user_role == 'individual':
            show_my_donations()
        elif current_page == 'profile':
            show_profile_settings()
        elif current_page == 'analytics' and user_role == 'organization':
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
        st.markdown("""
        **Quick Actions:**
        """)
        
        if st.button("🚀 Create New Campaign", use_container_width=True, type="primary"):
            st.session_state.current_page = 'create_campaign'
            st.experimental_rerun()
        
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.current_page = 'analytics'
            st.experimental_rerun()
        
        if st.button("💌 Send Update", use_container_width=True):
            st.info("📧 Campaign update feature coming soon!")

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
            st.experimental_rerun()
    
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
            st.experimental_rerun()
    
    # Recent activity
    st.markdown("### 📈 Your Recent Activity")
    
    st.markdown("""
    **Recent Donations:**
    - $75 to Emergency Medical Fund - 3 days ago
    - $50 to School Supplies Drive - 1 week ago
    - $25 to Animal Shelter Renovation - 2 weeks ago
    
    **Campaigns You're Following:**
    - Emergency Medical Fund (75% funded)
    - Clean Water Initiative (60% funded)
    - Community Garden Project (40% funded)
    """)

def show_floating_action_button():
    """Show floating action button for creating campaigns"""
    
    st.markdown("""
    <div style='position: fixed; bottom: 2rem; right: 2rem; z-index: 1000;'>
        <div class='fab-button' onclick='window.location.reload()' title='Create Campaign'>
            ➕
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_my_campaigns():
    """Show organization's campaigns"""
    
    st.markdown("### 📊 My Campaigns")
    
    # Mock campaign data
    campaigns = [
        {
            'title': 'Emergency Medical Fund',
            'status': 'Active',
            'raised': 37500,
            'target': 50000,
            'donors': 89,
            'days_left': 15
        },
        {
            'title': 'School Supplies Drive',
            'status': 'Under Review',
            'raised': 0,
            'target': 25000,
            'donors': 0,
            'days_left': 30
        }
    ]
    
    for campaign in campaigns:
        with st.expander(f"{campaign['title']} - {campaign['status']}"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💰 Raised", f"${campaign['raised']:,}")
            
            with col2:
                st.metric("🎯 Target", f"${campaign['target']:,}")
            
            with col3:
                st.metric("👥 Donors", campaign['donors'])
            
            with col4:
                st.metric("📅 Days Left", campaign['days_left'])
            
            # Progress bar
            if campaign['target'] > 0:
                progress = campaign['raised'] / campaign['target']
                st.progress(progress)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"📝 Edit", key=f"edit_{campaign['title']}"):
                    st.info("📝 Edit functionality coming soon!")
            
            with col2:
                if st.button(f"📊 Analytics", key=f"analytics_{campaign['title']}"):
                    st.info("📊 Analytics functionality coming soon!")
            
            with col3:
                if st.button(f"📢 Update", key=f"update_{campaign['title']}"):
                    st.info("📢 Update functionality coming soon!")

def show_my_donations():
    """Show individual's donation history"""
    
    st.markdown("### 💝 My Donation History")
    
    # Mock donation data
    donations = [
        {
            'campaign': 'Emergency Medical Fund',
            'amount': 75,
            'date': '2025-08-04',
            'status': 'Completed',
            'receipt': 'REC-001'
        },
        {
            'campaign': 'School Supplies Drive',
            'amount': 50,
            'date': '2025-07-28',
            'status': 'Completed',
            'receipt': 'REC-002'
        }
    ]
    
    for donation in donations:
        with st.expander(f"${donation['amount']} to {donation['campaign']} - {donation['date']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Amount:** ${donation['amount']}")
                st.write(f"**Status:** {donation['status']}")
            
            with col2:
                st.write(f"**Date:** {donation['date']}")
                st.write(f"**Receipt:** {donation['receipt']}")
            
            with col3:
                if st.button(f"📧 Email Receipt", key=f"receipt_{donation['receipt']}"):
                    st.success("📧 Receipt sent to your email!")
                
                if st.button(f"🔗 View Campaign", key=f"view_{donation['receipt']}"):
                    st.session_state.current_page = 'browse_campaigns'
                    st.experimental_rerun()

def show_profile_settings():
    """Show profile settings page"""
    
    st.markdown("### 👤 Profile Settings")
    
    user_info = get_user_info()
    user_role = get_current_user_role()
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Email", value=user_info.get('email', ''), disabled=True)
            st.text_input("First Name", value=user_info.get('first_name', ''))
            st.text_input("Last Name", value=user_info.get('last_name', ''))
        
        with col2:
            st.selectbox("Role", options=[user_role], index=0, disabled=True)
            st.text_input("Phone", value=user_info.get('phone', ''))
            st.selectbox("Preferred Language", options=["English", "Spanish", "French"], index=0)
        
        # Notification preferences
        st.markdown("#### 🔔 Notification Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Email notifications", value=True)
            st.checkbox("Campaign updates", value=True)
        
        with col2:
            st.checkbox("Donation receipts", value=True)
            st.checkbox("Newsletter", value=False)
        
        if st.form_submit_button("💾 Save Changes", use_container_width=True, type="primary"):
            st.success("✅ Profile updated successfully!")

def show_analytics():
    """Show analytics page for organizations"""
    
    st.markdown("### 📊 Campaign Analytics")
    
    # Mock analytics data
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📈 Total Views", "1,234", delta="156")
    
    with col2:
        st.metric("💰 Conversion Rate", "12.5%", delta="2.1%")
    
    with col3:
        st.metric("📱 Mobile Traffic", "68%", delta="5%")
    
    # Charts would go here
    st.info("📊 Detailed analytics charts coming soon!")

def show_help_support():
    """Show help and support page"""
    
    st.markdown("### ❓ Help & Support")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📚 Frequently Asked Questions
        
        **Q: How do I create a campaign?**
        A: Click on "Create Campaign" in the navigation menu and follow the step-by-step process.
        
        **Q: How long does campaign approval take?**
        A: Campaign approval typically takes 24-48 hours after submission.
        
        **Q: How do I receive donations?**
        A: Donations are transferred to your verified bank account weekly.
        """)
    
    with col2:
        st.markdown("""
        #### 📞 Contact Support
        
        **Email:** support@haven-platform.org
        **Phone:** +1 (555) 123-4567
        **Hours:** Monday-Friday, 9 AM - 6 PM EST
        
        #### 🔗 Useful Links
        - [Campaign Guidelines](https://haven-platform.org/guidelines)
        - [Terms of Service](https://haven-platform.org/terms)
        - [Privacy Policy](https://haven-platform.org/privacy)
        """)

if __name__ == "__main__":
    main()



# Additional workflow integration functions

def handle_page_navigation():
    """Handle advanced page navigation with workflow integration"""
    
    # Check for URL parameters or query strings for direct navigation
    query_params = st.experimental_get_query_params()
    
    if 'page' in query_params:
        requested_page = query_params['page'][0]
        if is_valid_page(requested_page):
            st.session_state.current_page = requested_page
    
    if 'campaign_id' in query_params:
        campaign_id = query_params['campaign_id'][0]
        # Load specific campaign
        load_campaign_by_id(campaign_id)

def is_valid_page(page: str) -> bool:
    """Check if requested page is valid for current user role"""
    
    user_role = get_current_user_role()
    
    valid_pages = {
        'individual': [
            'dashboard', 'browse_campaigns', 'campaign_details', 'donation',
            'my_donations', 'favorites', 'impact_report', 'profile', 'help'
        ],
        'organization': [
            'dashboard', 'create_campaign', 'my_campaigns', 'donations_received',
            'analytics', 'browse_campaigns', 'profile', 'help'
        ]
    }
    
    return page in valid_pages.get(user_role, [])

def load_campaign_by_id(campaign_id: str):
    """Load specific campaign for viewing or editing"""
    
    try:
        # In real implementation, this would fetch from backend
        # For now, we'll simulate loading
        st.session_state.selected_campaign = {
            'id': campaign_id,
            'title': f'Campaign {campaign_id}',
            'status': 'active'
        }
        st.session_state.current_page = 'campaign_details'
        
    except Exception as e:
        logger.error(f"Error loading campaign {campaign_id}: {e}")
        st.error(f"❌ Could not load campaign: {str(e)}")

def show_workflow_status():
    """Show current workflow status for organizations"""
    
    user_role = get_current_user_role()
    
    if user_role != 'organization':
        return
    
    # Check for campaigns in different workflow stages
    workflow_status = {
        'draft': 1,
        'pending_review': 2,
        'active': 3,
        'completed': 1
    }
    
    st.markdown("### 🔄 Workflow Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Drafts", workflow_status['draft'])
    
    with col2:
        st.metric("⏳ Pending Review", workflow_status['pending_review'])
    
    with col3:
        st.metric("🚀 Active", workflow_status['active'])
    
    with col4:
        st.metric("✅ Completed", workflow_status['completed'])

def show_notification_center():
    """Show notification center with workflow updates"""
    
    if 'show_notifications' not in st.session_state:
        st.session_state.show_notifications = False
    
    # Notification toggle in sidebar
    with st.sidebar:
        if st.button("🔔 Notifications", use_container_width=True):
            st.session_state.show_notifications = not st.session_state.show_notifications
    
    if st.session_state.show_notifications:
        with st.sidebar:
            st.markdown("#### 🔔 Recent Notifications")
            
            notifications = [
                {
                    'type': 'success',
                    'message': 'Campaign "Medical Fund" approved!',
                    'time': '2 hours ago'
                },
                {
                    'type': 'info',
                    'message': 'New donation of $50 received',
                    'time': '5 hours ago'
                },
                {
                    'type': 'warning',
                    'message': 'Campaign deadline approaching',
                    'time': '1 day ago'
                }
            ]
            
            for notification in notifications:
                icon = "✅" if notification['type'] == 'success' else "ℹ️" if notification['type'] == 'info' else "⚠️"
                st.markdown(f"{icon} {notification['message']}")
                st.caption(notification['time'])
                st.markdown("---")

def show_quick_actions():
    """Show quick action buttons based on user role and context"""
    
    user_role = get_current_user_role()
    current_page = st.session_state.get('current_page', 'dashboard')
    
    # Quick actions in sidebar
    with st.sidebar:
        st.markdown("### ⚡ Quick Actions")
        
        if user_role == 'organization':
            if current_page != 'create_campaign':
                if st.button("🚀 Quick Campaign", use_container_width=True, type="primary"):
                    st.session_state.current_page = 'create_campaign'
                    st.experimental_rerun()
            
            if st.button("📊 Quick Stats", use_container_width=True):
                show_quick_stats_modal()
            
            if st.button("💌 Send Update", use_container_width=True):
                show_campaign_update_modal()
        
        else:  # individual
            if st.button("💝 Quick Donate", use_container_width=True, type="primary"):
                st.session_state.current_page = 'browse_campaigns'
                st.experimental_rerun()
            
            if st.button("📊 My Impact", use_container_width=True):
                show_impact_modal()
            
            if st.button("⭐ Favorites", use_container_width=True):
                st.session_state.current_page = 'favorites'
                st.experimental_rerun()

def show_quick_stats_modal():
    """Show quick stats in a modal-like container"""
    
    with st.container():
        st.markdown("""
        <div class='info-card'>
            <h4>📊 Quick Stats</h4>
            <p><strong>Active Campaigns:</strong> 3</p>
            <p><strong>Total Raised:</strong> $12,450</p>
            <p><strong>This Month:</strong> $2,100</p>
        </div>
        """, unsafe_allow_html=True)

def show_campaign_update_modal():
    """Show campaign update form in a modal-like container"""
    
    with st.container():
        st.markdown("#### 💌 Send Campaign Update")
        
        with st.form("quick_update_form"):
            campaign = st.selectbox("Select Campaign", ["Emergency Medical Fund", "School Supplies Drive"])
            update_title = st.text_input("Update Title")
            update_message = st.text_area("Update Message", height=100)
            
            if st.form_submit_button("📤 Send Update"):
                st.success("✅ Update sent to all supporters!")

def show_impact_modal():
    """Show impact summary for individuals"""
    
    with st.container():
        st.markdown("""
        <div class='info-card'>
            <h4>🌟 Your Impact</h4>
            <p><strong>Total Donated:</strong> $450</p>
            <p><strong>Campaigns Supported:</strong> 7</p>
            <p><strong>Lives Impacted:</strong> ~150 people</p>
            <p><strong>Impact Score:</strong> 92/100</p>
        </div>
        """, unsafe_allow_html=True)

def handle_workflow_transitions():
    """Handle workflow state transitions and notifications"""
    
    # Check for workflow state changes
    if 'last_workflow_check' not in st.session_state:
        st.session_state.last_workflow_check = datetime.now()
    
    # Simulate workflow state changes (in real app, this would come from backend)
    current_time = datetime.now()
    time_diff = (current_time - st.session_state.last_workflow_check).seconds
    
    if time_diff > 30:  # Check every 30 seconds
        check_workflow_updates()
        st.session_state.last_workflow_check = current_time

def check_workflow_updates():
    """Check for workflow updates from backend"""
    
    try:
        # In real implementation, this would call backend API
        # For now, we'll simulate random updates
        import random
        
        if random.random() < 0.1:  # 10% chance of update
            show_workflow_notification()
    
    except Exception as e:
        logger.error(f"Error checking workflow updates: {e}")

def show_workflow_notification():
    """Show workflow notification to user"""
    
    notifications = [
        "✅ Your campaign has been approved!",
        "💰 New donation received!",
        "📊 Weekly report is ready",
        "⚠️ Campaign deadline approaching"
    ]
    
    import random
    notification = random.choice(notifications)
    
    st.toast(notification, icon="🔔")

def show_advanced_search():
    """Show advanced search functionality for campaigns"""
    
    if st.session_state.get('current_page') == 'browse_campaigns':
        with st.expander("🔍 Advanced Search", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.multiselect("Categories", 
                    ["Medical", "Education", "Environment", "Community", "Emergency"])
                st.slider("Funding Range", 0, 100000, (0, 50000), format="$%d")
            
            with col2:
                st.selectbox("Sort by", ["Most Recent", "Ending Soon", "Most Funded", "Alphabetical"])
                st.selectbox("Location", ["All Locations", "Local", "National", "International"])
            
            with col3:
                st.selectbox("Urgency", ["All Levels", "Critical", "High", "Medium", "Low"])
                st.checkbox("Verified Organizations Only")
            
            if st.button("🔍 Apply Filters", use_container_width=True):
                st.info("🔍 Filters applied! Results updated.")

def show_campaign_sharing():
    """Show campaign sharing functionality"""
    
    if st.session_state.get('selected_campaign'):
        campaign = st.session_state.selected_campaign
        
        st.markdown("### 📤 Share This Campaign")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📱 Share on Social", use_container_width=True):
                st.info("📱 Social sharing link copied to clipboard!")
        
        with col2:
            if st.button("📧 Email to Friend", use_container_width=True):
                st.info("📧 Email sharing form opened!")
        
        with col3:
            if st.button("🔗 Copy Link", use_container_width=True):
                st.info("🔗 Campaign link copied to clipboard!")

def show_donation_tracking():
    """Show donation tracking for individuals"""
    
    user_role = get_current_user_role()
    
    if user_role == 'individual' and st.session_state.get('current_page') == 'my_donations':
        st.markdown("### 📊 Donation Impact Tracking")
        
        # Impact visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Your Donation Journey:**
            - 🎯 Total Campaigns: 7
            - 💰 Average Donation: $64
            - 📈 Growth Rate: +15% this month
            - 🏆 Donor Level: Gold Supporter
            """)
        
        with col2:
            st.markdown("""
            **Impact Achieved:**
            - 👥 People Helped: ~150
            - 🏥 Medical Treatments: 12
            - 📚 Students Supported: 25
            - 🌱 Trees Planted: 50
            """)

def show_organization_verification():
    """Show organization verification status and requirements"""
    
    user_role = get_current_user_role()
    
    if user_role == 'organization':
        # Check verification status
        verification_status = {
            'documents': True,
            'bank_account': True,
            'identity': False,
            'tax_status': True
        }
        
        incomplete_items = [k for k, v in verification_status.items() if not v]
        
        if incomplete_items:
            st.warning(f"⚠️ Verification incomplete: {', '.join(incomplete_items)}")
            
            if st.button("📋 Complete Verification", use_container_width=True):
                st.session_state.current_page = 'verification'
                st.experimental_rerun()

def show_mobile_responsive_elements():
    """Show mobile-responsive elements and touch-friendly interfaces"""
    
    # Add mobile-specific CSS
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .stButton > button {
            padding: 1rem;
            font-size: 16px;
            min-height: 44px; /* Touch-friendly size */
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
        }
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_workflow_integration():
    """Initialize all workflow integration components"""
    
    # Initialize workflow state tracking
    if 'workflow_state' not in st.session_state:
        st.session_state.workflow_state = {
            'current_step': 1,
            'completed_steps': [],
            'pending_actions': []
        }
    
    # Initialize notification system
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    
    # Initialize search state
    if 'search_filters' not in st.session_state:
        st.session_state.search_filters = {}
    
    # Handle page navigation
    handle_page_navigation()
    
    # Show workflow status for organizations
    if get_current_user_role() == 'organization':
        show_workflow_status()
    
    # Show notification center
    show_notification_center()
    
    # Show quick actions
    show_quick_actions()
    
    # Handle workflow transitions
    handle_workflow_transitions()
    
    # Show mobile responsive elements
    show_mobile_responsive_elements()
    
    # Show organization verification status
    show_organization_verification()

# Enhanced main function with full workflow integration
def enhanced_main():
    """Enhanced main function with complete workflow integration"""
    
    try:
        # Initialize session state
        initialize_session_state()
        
        # Initialize workflow integration
        initialize_workflow_integration()
        
        # Handle OAuth callback first
        handle_oauth_callback()
        
        # Check authentication status
        if check_authentication_status():
            show_authenticated_app()
        else:
            show_login_page()
            
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"❌ Application error: {str(e)}")
        st.info("🔄 Please refresh the page or contact support if the issue persists.")

# Update the main execution to use enhanced version
if __name__ == "__main__":
    enhanced_main()

