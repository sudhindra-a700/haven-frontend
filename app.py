# Modified app.py - Main Haven Frontend Application with Bootstrap Icons
# This file replaces your existing app.py

import streamlit as st
from utils.icon_utils import display_icon, get_icon_html, icon_button, verify_icon_exists
from config.icon_mapping import get_icon, ICON_COLORS, ICON_SIZES

# Import your workflow modules (with icons now integrated)
from workflow_auth_utils import run_authentication_workflow, render_user_profile_settings
from workflow_campaign_pages import run_campaign_workflow
from workflow_verification_funding import run_verification_funding_workflow

class HavenMainApp:
    """Main Haven application with Bootstrap Icons integration."""
    
    def __init__(self):
        self.setup_page_config()
        self.inject_custom_css()
        self.verify_icons_setup()
        self.initialize_session_state()
    
    def setup_page_config(self):
        """Configure the Streamlit page."""
        st.set_page_config(
            page_title="Haven - Crowdfunding Platform",
            page_icon="🏠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def verify_icons_setup(self):
        """Verify that Bootstrap icons are properly set up."""
        if not verify_icon_exists("house-fill"):
            st.error("""
            ⚠️ **Bootstrap Icons Not Found!**
            
            Please ensure you have:
            1. Downloaded the bootstrap-icons repository
            2. Copied the `bootstrap-icons/icons/` directory to your project root
            3. Placed the icon utility files in the correct locations
            
            See the setup guide for detailed instructions.
            """)
            st.stop()
    
    def inject_custom_css(self):
        """Inject custom CSS for the application."""
        css = """
        <style>
        /* Main application styles */
        .main-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 30px;
            padding: 20px 0;
            border-bottom: 2px solid #4CAF50;
        }
        
        .nav-container {
            background: linear-gradient(135deg, #4CAF50, #66BB6A);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        
        .nav-button {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            margin: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .nav-button:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .nav-button.active {
            background: white;
            color: #4CAF50;
        }
        
        .sidebar-nav {
            padding: 10px 0;
        }
        
        .sidebar-nav .nav-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 15px;
            margin: 5px 0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .sidebar-nav .nav-item:hover {
            background: #f0f0f0;
        }
        
        .sidebar-nav .nav-item.active {
            background: #4CAF50;
            color: white;
        }
        
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }
        
        .feature-card {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 25px;
            margin: 15px 0;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            border-color: #4CAF50;
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.15);
        }
        
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .status-online { background: #d4edda; color: #155724; }
        .status-verified { background: #cce6ff; color: #004085; }
        .status-pending { background: #fff3cd; color: #856404; }
        
        .quick-action-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .footer {
            margin-top: 50px;
            padding: 30px 0;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            color: #666;
        }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    
    def initialize_session_state(self):
        """Initialize session state variables."""
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'
        
        if 'user_authenticated' not in st.session_state:
            st.session_state.user_authenticated = False
        
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {
                'name': 'John Doe',
                'email': 'john@example.com',
                'verified': True,
                'campaigns_created': 3,
                'campaigns_backed': 12,
                'total_contributed': 2450
            }
    
    def render_header(self):
        """Render the main application header."""
        st.markdown(f"""
        <div class="main-header">
            {get_icon_html("house-heart-fill", 40, "#4CAF50")}
            <h1 style="margin: 0; color: #2E7D32;">Haven Crowdfunding Platform</h1>
            <div style="margin-left: auto; display: flex; align-items: center; gap: 15px;">
                <span class="status-indicator status-online">
                    {get_icon_html('wifi', 14)} Online
                </span>
                <span class="status-indicator status-verified">
                    {get_icon_html('patch-check-fill', 14)} Verified
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar_navigation(self):
        """Render sidebar navigation with icons."""
        st.sidebar.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px;">
            {get_icon_html("person-circle", 48, "#4CAF50")}
            <h3 style="margin: 10px 0; color: #4CAF50;">Welcome, {st.session_state.user_data['name']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        nav_items = [
            ("home", "house-fill", "Home"),
            ("campaigns", "search", "Browse Campaigns"),
            ("create", "plus-circle-fill", "Create Campaign"),
            ("dashboard", "speedometer2", "My Dashboard"),
            ("verification", "shield-check", "Verification"),
            ("profile", "person-gear", "Profile Settings"),
            ("help", "question-circle", "Help & Support")
        ]
        
        st.sidebar.markdown("### Navigation")
        
        for page_key, icon, label in nav_items:
            if st.sidebar.button(f"{get_icon_html(icon, ICON_SIZES['sm'])} {label}", key=f"nav_{page_key}"):
                st.session_state.current_page = page_key
        
        # User stats in sidebar
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Quick Stats")
        
        stats = [
            ("campaigns_created", "rocket-takeoff", "Campaigns Created", st.session_state.user_data['campaigns_created']),
            ("campaigns_backed", "bookmark-star", "Campaigns Backed", st.session_state.user_data['campaigns_backed']),
            ("total_contributed", "currency-dollar", "Total Contributed", f"${st.session_state.user_data['total_contributed']}")
        ]
        
        for stat_key, icon, label, value in stats:
            st.sidebar.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; padding: 8px; margin: 5px 0; 
                        background: #f8f9fa; border-radius: 6px;">
                {get_icon_html(icon, 16, '#4CAF50')}
                <div>
                    <div style="font-weight: 500; font-size: 14px;">{value}</div>
                    <div style="font-size: 12px; color: #666;">{label}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_home_page(self):
        """Render the home page with platform overview."""
        st.markdown(f"""
        <h2>{get_icon_html('star-fill', 28, '#FFD700')} Welcome to Haven</h2>
        <p style="font-size: 18px; color: #666;">Your gateway to innovative crowdfunding projects</p>
        """, unsafe_allow_html=True)
        
        # Platform statistics
        col1, col2, col3, col4 = st.columns(4)
        
        stats = [
            ("currency-dollar", "Total Raised", "$2.5M", ICON_COLORS['success']),
            ("people-fill", "Active Users", "15,432", ICON_COLORS['info']),
            ("trophy-fill", "Successful Projects", "1,247", ICON_COLORS['warning']),
            ("lightning-charge-fill", "Active Campaigns", "89", ICON_COLORS['primary'])
        ]
        
        for i, (icon, label, value, color) in enumerate(stats):
            with [col1, col2, col3, col4][i]:
                st.markdown(f"""
                <div class="metric-card">
                    {get_icon_html(icon, 32, color)}
                    <h2 style="margin: 10px 0; color: {color};">{value}</h2>
                    <p style="margin: 0; color: {ICON_COLORS['muted']};">{label}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Featured sections
        st.markdown(f"""
        <h3>{get_icon_html('fire', ICON_SIZES['lg'])} What You Can Do</h3>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        features = [
            ("search", "Discover Projects", "Browse thousands of innovative campaigns", "Explore creative projects from around the world"),
            ("plus-circle-fill", "Start a Campaign", "Bring your ideas to life", "Launch your own crowdfunding campaign"),
            ("people", "Join Community", "Connect with creators", "Support projects you believe in")
        ]
        
        for i, (icon, title, subtitle, description) in enumerate(features):
            with [col1, col2, col3][i]:
                st.markdown(f"""
                <div class="feature-card">
                    {get_icon_html(icon, 48, '#4CAF50')}
                    <h3 style="margin: 15px 0 10px 0; color: #2E7D32;">{title}</h3>
                    <p style="margin: 0 0 10px 0; color: #4CAF50; font-weight: 500;">{subtitle}</p>
                    <p style="margin: 0; color: #666; font-size: 14px;">{description}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown(f"""
        <h3>{get_icon_html('lightning-fill', ICON_SIZES['lg'])} Quick Actions</h3>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        actions = [
            ("plus-circle-fill", "Create Campaign", "create"),
            ("search", "Browse Projects", "campaigns"),
            ("person-gear", "Update Profile", "profile"),
            ("shield-check", "Verify Account", "verification")
        ]
        
        for i, (icon, label, page) in enumerate(actions):
            with [col1, col2, col3, col4][i]:
                if st.button(f"{get_icon_html(icon, ICON_SIZES['sm'])} {label}", key=f"quick_{page}"):
                    st.session_state.current_page = page
    
    def render_help_page(self):
        """Render help and support page."""
        st.markdown(f"""
        <h1>{get_icon_html('question-circle-fill', 32, ICON_COLORS['primary'])} Help & Support</h1>
        """, unsafe_allow_html=True)
        
        # Help categories
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <h3>{get_icon_html('book', ICON_SIZES['lg'])} Getting Started</h3>
            """, unsafe_allow_html=True)
            
            help_topics = [
                ("person-plus", "Creating an Account"),
                ("shield-check", "Account Verification"),
                ("plus-circle", "Starting a Campaign"),
                ("cash-coin", "Making Contributions")
            ]
            
            for icon, topic in help_topics:
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 10px; padding: 10px; 
                            margin: 5px 0; background: #f8f9fa; border-radius: 6px; cursor: pointer;">
                    {get_icon_html(icon, 20, '#4CAF50')}
                    <span>{topic}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <h3>{get_icon_html('headset', ICON_SIZES['lg'])} Contact Support</h3>
            """, unsafe_allow_html=True)
            
            contact_options = [
                ("chat-dots", "Live Chat", "Available 24/7"),
                ("envelope", "Email Support", "support@haven.com"),
                ("telephone", "Phone Support", "+1 (555) 123-4567"),
                ("question-circle", "FAQ", "Common questions")
            ]
            
            for icon, method, detail in contact_options:
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 10px; padding: 15px; 
                            margin: 10px 0; background: white; border: 1px solid #e0e0e0; 
                            border-radius: 8px; cursor: pointer;">
                    {get_icon_html(icon, 24, '#4CAF50')}
                    <div>
                        <div style="font-weight: 500;">{method}</div>
                        <div style="color: #666; font-size: 14px;">{detail}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    def render_footer(self):
        """Render application footer."""
        st.markdown(f"""
        <div class="footer">
            <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 20px;">
                <a href="#" style="color: #666; text-decoration: none;">
                    {get_icon_html('info-circle', 16)} About
                </a>
                <a href="#" style="color: #666; text-decoration: none;">
                    {get_icon_html('shield-check', 16)} Privacy
                </a>
                <a href="#" style="color: #666; text-decoration: none;">
                    {get_icon_html('file-text', 16)} Terms
                </a>
                <a href="#" style="color: #666; text-decoration: none;">
                    {get_icon_html('envelope', 16)} Contact
                </a>
            </div>
            <p style="margin: 0;">
                {get_icon_html('heart-fill', 16, '#FF6B6B')} Made with love by the Haven team
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Main application runner."""
        # Render header
        self.render_header()
        
        # Render sidebar navigation
        self.render_sidebar_navigation()
        
        # Main content area
        if not st.session_state.user_authenticated and st.session_state.current_page not in ['home', 'help']:
            # Show authentication for protected pages
            if run_authentication_workflow():
                st.session_state.user_authenticated = True
                st.rerun()
        else:
            # Render appropriate page based on current_page
            if st.session_state.current_page == 'home':
                self.render_home_page()
            
            elif st.session_state.current_page == 'campaigns':
                run_campaign_workflow()
            
            elif st.session_state.current_page == 'create':
                run_campaign_workflow()
            
            elif st.session_state.current_page == 'dashboard':
                run_campaign_workflow()
            
            elif st.session_state.current_page == 'verification':
                run_verification_funding_workflow()
            
            elif st.session_state.current_page == 'profile':
                render_user_profile_settings()
            
            elif st.session_state.current_page == 'help':
                self.render_help_page()
            
            else:
                # Default to home page
                self.render_home_page()
        
        # Render footer
        self.render_footer()

# Main application entry point
def main():
    """Main function to run the Haven application."""
    app = HavenMainApp()
    app.run()

if __name__ == "__main__":
    main()

