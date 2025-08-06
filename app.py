"""
Enhanced HAVEN Crowdfunding Platform Frontend
Streamlit application with role-based access control and separate registration flows
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime

# Import enhanced authentication and registration modules
from workflow_auth_utils import (
    initialize_auth, is_authenticated, login_user, logout_user,
    is_individual, is_organization, can_donate, can_create_campaigns,
    needs_registration, get_user_role_display, get_allowed_features
)
from workflow_registration_pages import show_registration_workflow

# Import Tabler Icons
try:
    from pytablericons import TablerIcon
    TABLER_AVAILABLE = True
except ImportError:
    TABLER_AVAILABLE = False
    st.warning("⚠️ pytablericons not installed. Install with: pip install pytablericons")

# ===== CONFIGURATION =====
st.set_page_config(
    page_title="HAVEN - Enhanced Crowdfunding Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== DYNAMIC THEMING SYSTEM =====
class ThemeManager:
    """Manage dynamic theming for icons based on background"""
    
    @staticmethod
    def get_icon_color(context="light"):
        """Get appropriate icon color based on background context"""
        if context == "dark":
            return "#FFFFFF"  # White icons on dark background
        else:
            return "#000000"  # Black icons on light background
    
    @staticmethod
    def get_primary_color():
        """Get primary theme color"""
        return "#4CAF50"
    
    @staticmethod
    def get_secondary_color():
        """Get secondary theme color"""
        return "#2196F3"

# ===== ICON CONSTANTS =====
class HavenIcons:
    """Tabler icon constants for HAVEN platform"""
    HOME = "home"
    TRENDING = "trending-up"
    EXPLORE = "compass"
    SEARCH = "search"
    CAMPAIGN = "circle-plus"
    DONATE = "heart"
    PROFILE = "user"
    LOGOUT = "logout"
    RUPEE = "currency-rupee"
    GOOGLE = "brand-google"
    FACEBOOK = "brand-facebook"
    INDIVIDUAL = "user"
    ORGANIZATION = "building"
    ADMIN = "shield-check"

# ===== TABLER ICONS MANAGER =====
class TablerIconManager:
    """Manage Tabler Icons with dynamic theming and caching"""
    
    def __init__(self):
        self.icon_cache = {}
    
    def get_icon(self, icon_name, size=24, color=None, context="light", stroke_width=2):
        """Get Tabler icon with dynamic theming"""
        if not TABLER_AVAILABLE:
            return self._get_fallback_icon(icon_name)
        
        if color is None:
            color = ThemeManager.get_icon_color(context)
        
        # Create cache key
        cache_key = f"{icon_name}_{size}_{color}_{stroke_width}"
        
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]
        
        try:
            # Get Tabler icon
            icon = TablerIcon(
                name=icon_name,
                size=size,
                color=color,
                stroke_width=stroke_width
            )
            
            # Cache the result
            self.icon_cache[cache_key] = icon.svg
            return icon.svg
            
        except Exception as e:
            st.error(f"Error loading icon {icon_name}: {e}")
            return self._get_fallback_icon(icon_name)
    
    def _get_fallback_icon(self, icon_name):
        """Fallback emoji icons if Tabler Icons not available"""
        fallbacks = {
            "home": "🏠",
            "trending-up": "📈",
            "compass": "🧭",
            "search": "🔍",
            "circle-plus": "➕",
            "heart": "❤️",
            "user": "👤",
            "logout": "🚪",
            "currency-rupee": "₹",
            "brand-google": "🇬",
            "brand-facebook": "🇫",
            "building": "🏢",
            "shield-check": "🛡️"
        }
        return fallbacks.get(icon_name, "❓")
    
    def render_icon(self, icon_name, size=24, color=None, context="light", stroke_width=2):
        """Render Tabler icon in Streamlit"""
        if TABLER_AVAILABLE:
            svg_code = self.get_icon(icon_name, size, color, context, stroke_width)
            st.markdown(svg_code, unsafe_allow_html=True)
        else:
            fallback = self._get_fallback_icon(icon_name)
            st.markdown(f'<span style="font-size: {size}px;">{fallback}</span>', unsafe_allow_html=True)

# ===== CUSTOM CSS =====
def load_custom_css():
    """Load custom CSS for enhanced UI"""
    st.markdown("""
    <style>
    /* Main app styling */
    .main-header {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .role-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        margin-left: 1rem;
    }
    
    .individual-badge {
        background: #2196F3;
        color: white;
    }
    
    .organization-badge {
        background: #4CAF50;
        color: white;
    }
    
    .admin-badge {
        background: #FF9800;
        color: white;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .feature-card.enabled {
        border-color: #4CAF50;
    }
    
    .feature-card.disabled {
        border-color: #f44336;
        opacity: 0.6;
    }
    
    .login-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
    }
    
    .social-login-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .social-icon {
        padding: 0.75rem;
        border: 2px solid #e0e0e0;
        border-radius: 50%;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .social-icon:hover {
        border-color: #4CAF50;
        transform: scale(1.1);
    }
    
    .registration-prompt {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .access-denied {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        color: #721c24;
    }
    </style>
    """, unsafe_allow_html=True)

# ===== AUTHENTICATION FUNCTIONS =====
def render_login_page(icon_manager):
    """Render login page with role-based messaging"""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Welcome to HAVEN Enhanced</h1>
        <p>Empowering Communities Through Role-Based Crowdfunding</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Role-based information
        st.markdown("""
        ### 🎭 Choose Your Role
        
        **👤 Individual**: Register to donate to campaigns and support causes you care about.
        
        **🏢 Organization**: Register to create and manage fundraising campaigns.
        """)
        
        st.markdown("---")
        
        # Login form
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password", placeholder="Your password")
            
            col1, col2 = st.columns(2)
            with col1:
                login_submitted = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            with col2:
                register_clicked = st.form_submit_button("📝 Register", use_container_width=True)
            
            if login_submitted:
                if email and password:
                    with st.spinner("Logging in..."):
                        success, message = login_user("email", {"email": email, "password": password})
                    
                    if success:
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please enter both email and password")
            
            if register_clicked:
                st.session_state.show_registration = True
                st.rerun()
        
        # Social login buttons
        st.markdown("---")
        st.markdown("### Or sign in with")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🇬 Google", use_container_width=True):
                st.info("Google OAuth integration coming soon!")
        with col2:
            if st.button("🇫 Facebook", use_container_width=True):
                st.info("Facebook OAuth integration coming soon!")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_registration_prompt():
    """Render registration completion prompt"""
    st.markdown("""
    <div class="registration-prompt">
        <h3>📋 Complete Your Registration</h3>
        <p>You're logged in but need to complete your registration to access all features.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Complete Registration", use_container_width=True, type="primary"):
        st.session_state.show_registration = True
        st.rerun()

# ===== NAVIGATION FUNCTIONS =====
def render_navigation(icon_manager):
    """Render role-based navigation sidebar"""
    if not is_authenticated():
        return
    
    # User info in sidebar
    st.sidebar.markdown("### 👤 User Info")
    role_display = get_user_role_display()
    
    if is_individual():
        badge_class = "individual-badge"
    elif is_organization():
        badge_class = "organization-badge"
    else:
        badge_class = "admin-badge"
    
    st.sidebar.markdown(f"""
    <div style="text-align: center;">
        <span class="role-badge {badge_class}">{role_display}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Get allowed features
    features = get_allowed_features()
    
    # Navigation items based on role
    st.sidebar.markdown("### 🧭 Navigation")
    
    # Home (always available)
    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()
    
    # View campaigns (always available)
    if st.sidebar.button("👀 View Campaigns", use_container_width=True):
        st.session_state.current_page = "campaigns"
        st.rerun()
    
    # Role-specific features
    if features.get('donate', False):
        if st.sidebar.button("❤️ My Donations", use_container_width=True):
            st.session_state.current_page = "donations"
            st.rerun()
    
    if features.get('create_campaigns', False):
        if st.sidebar.button("➕ Create Campaign", use_container_width=True):
            st.session_state.current_page = "create_campaign"
            st.rerun()
    
    if features.get('manage_campaigns', False):
        if st.sidebar.button("📊 My Campaigns", use_container_width=True):
            st.session_state.current_page = "my_campaigns"
            st.rerun()
    
    if features.get('admin_panel', False):
        if st.sidebar.button("🛡️ Admin Panel", use_container_width=True):
            st.session_state.current_page = "admin"
            st.rerun()
    
    # Profile and logout
    st.sidebar.markdown("---")
    if st.sidebar.button("👤 Profile", use_container_width=True):
        st.session_state.current_page = "profile"
        st.rerun()
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout_user()
        st.rerun()

# ===== PAGE FUNCTIONS =====
def render_home_page(icon_manager):
    """Render role-based home page"""
    st.markdown("""
    <div class="main-header">
        <h1>🏠 HAVEN Dashboard</h1>
        <p>Welcome to your personalized crowdfunding experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Role-specific welcome message
    if is_individual():
        st.markdown("""
        ### 👤 Individual Dashboard
        
        As an individual donor, you can:
        - 💝 Donate to campaigns that matter to you
        - 📊 Track your donation history
        - 🧾 Download tax receipts
        - 🔍 Discover new causes to support
        """)
        
        # Quick donate section
        st.markdown("### 🚀 Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❤️ Browse Campaigns to Donate", use_container_width=True, type="primary"):
                st.session_state.current_page = "campaigns"
                st.rerun()
        with col2:
            if st.button("📊 View My Donations", use_container_width=True):
                st.session_state.current_page = "donations"
                st.rerun()
    
    elif is_organization():
        st.markdown("""
        ### 🏢 Organization Dashboard
        
        As an organization, you can:
        - 🎯 Create fundraising campaigns
        - 📈 Manage your active campaigns
        - 💰 Track donations received
        - 📝 Post campaign updates
        """)
        
        # Quick campaign actions
        st.markdown("### 🚀 Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Create New Campaign", use_container_width=True, type="primary"):
                st.session_state.current_page = "create_campaign"
                st.rerun()
        with col2:
            if st.button("📊 Manage My Campaigns", use_container_width=True):
                st.session_state.current_page = "my_campaigns"
                st.rerun()
    
    else:
        st.markdown("""
        ### 🛡️ Admin Dashboard
        
        As an administrator, you have full access to:
        - 👥 User management
        - 🎯 Campaign moderation
        - 📊 Platform analytics
        - ⚙️ System configuration
        """)

def render_campaigns_page():
    """Render campaigns listing page"""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Browse Campaigns</h1>
        <p>Discover amazing causes and make a difference</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Role-specific messaging
    if is_individual():
        st.info("💡 As an individual, you can donate to any active campaign!")
    elif is_organization():
        st.info("💡 As an organization, you can view campaigns but cannot donate. You can create your own campaigns!")
    
    # Placeholder for campaigns list
    st.markdown("### 📋 Active Campaigns")
    st.info("Campaign listing functionality will be implemented here.")

def render_access_denied(feature_name):
    """Render access denied message"""
    st.markdown(f"""
    <div class="access-denied">
        <h3>🚫 Access Denied</h3>
        <p>You don't have permission to access <strong>{feature_name}</strong>.</p>
        <p>Your current role: <strong>{get_user_role_display()}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Role-specific guidance
    if is_individual():
        st.info("💡 As an individual, you can donate to campaigns but cannot create them.")
    elif is_organization():
        st.info("💡 As an organization, you can create campaigns but cannot donate to them.")

# ===== MAIN APPLICATION =====
def main():
    """Main application function"""
    # Load custom CSS
    load_custom_css()
    
    # Initialize authentication
    initialize_auth()
    
    # Create icon manager
    icon_manager = TablerIconManager()
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    
    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False
    
    # Check if user wants to register
    if st.session_state.show_registration:
        show_registration_workflow()
        
        # Back to login button
        if st.button("← Back to Login"):
            st.session_state.show_registration = False
            st.rerun()
        return
    
    # Check authentication
    if not is_authenticated():
        render_login_page(icon_manager)
        return
    
    # Check if user needs to complete registration
    if needs_registration():
        render_registration_prompt()
        return
    
    # Render navigation
    render_navigation(icon_manager)
    
    # Render current page
    current_page = st.session_state.current_page
    
    if current_page == "home":
        render_home_page(icon_manager)
    elif current_page == "campaigns":
        render_campaigns_page()
    elif current_page == "donations":
        if can_donate():
            st.markdown("### 📊 My Donations")
            st.info("Donation history will be implemented here.")
        else:
            render_access_denied("Donation History")
    elif current_page == "create_campaign":
        if can_create_campaigns():
            st.markdown("### ➕ Create New Campaign")
            st.info("Campaign creation form will be implemented here.")
        else:
            render_access_denied("Campaign Creation")
    elif current_page == "my_campaigns":
        if can_create_campaigns():
            st.markdown("### 📊 My Campaigns")
            st.info("Campaign management will be implemented here.")
        else:
            render_access_denied("Campaign Management")
    elif current_page == "admin":
        if st.session_state.user_role == "admin":
            st.markdown("### 🛡️ Admin Panel")
            st.info("Admin panel will be implemented here.")
        else:
            render_access_denied("Admin Panel")
    elif current_page == "profile":
        st.markdown("### 👤 Profile")
        st.info("Profile management will be implemented here.")
    else:
        render_home_page(icon_manager)

if __name__ == "__main__":
    main()

