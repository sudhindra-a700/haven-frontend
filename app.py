"""
Fixed HAVEN Crowdfunding Platform - Main Application
Implements proper authentication flow with conditional navigation and language dropdown
"""

import streamlit as st
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import page modules with error handling
try:
    from pages import home, login, register, explore, search, campaign, profile
    PAGES_AVAILABLE = True
except ImportError:
    try:
        # Fallback to individual imports
        import home
        import login  
        import register
        import explore
        import search
        import campaign
        import profile
        PAGES_AVAILABLE = True
    except ImportError as e:
        logger.error(f"Failed to import page modules: {e}")
        PAGES_AVAILABLE = False

def main():
    """Main application function"""
    try:
        # Page configuration
        st.set_page_config(
            page_title="HAVEN - Crowdfunding Platform",
            page_icon="🏠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Initialize session state
        initialize_session_state()
        
        # Load custom CSS
        load_custom_css()
        
        # Check authentication status
        is_authenticated = st.session_state.get('authenticated', False)
        
        if not is_authenticated:
            # Show login/registration interface
            show_auth_interface()
        else:
            # Show main application interface
            show_main_interface()
            
    except Exception as e:
        logger.error(f"Main application error: {e}")
        st.error("Sorry, there was an error loading the application. Please refresh the page.")
        st.exception(e)

def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user' not in st.session_state:
        st.session_state.user = {}
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'
    
    if 'language' not in st.session_state:
        st.session_state.language = 'English'

def load_custom_css():
    """Load custom CSS styling with light green theme"""
    st.markdown("""
    <style>
    /* Main theme colors - Light Green */
    :root {
        --primary-color: #4caf50;
        --secondary-color: #81c784;
        --accent-color: #2e7d32;
        --background-color: #e8f5e8;
        --text-color: #1b5e20;
    }
    
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--background-color);
    }
    
    /* Button styling */
    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: var(--accent-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    /* Navigation styling */
    .nav-button {
        width: 100%;
        margin: 0.25rem 0;
        padding: 0.75rem;
        background: white;
        border: 2px solid var(--primary-color);
        border-radius: 10px;
        color: var(--accent-color);
        font-weight: bold;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-button:hover {
        background: var(--primary-color);
        color: white;
        transform: translateX(5px);
    }
    
    .nav-button.active {
        background: var(--accent-color);
        color: white;
    }
    
    /* Language dropdown styling */
    .language-dropdown {
        background: white;
        border: 2px solid var(--primary-color);
        border-radius: 10px;
        padding: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Auth interface styling */
    .auth-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    /* Pulse animation for OAuth buttons */
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* MaterializeCSS inspired elements */
    .floating-action-btn {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 56px;
        height: 56px;
        background: var(--primary-color);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .floating-action-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.6);
    }
    
    /* Card panel styling */
    .card-panel {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid var(--primary-color);
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background-color: #c8e6c9;
        border-left: 4px solid #4caf50;
    }
    
    .stError {
        background-color: #ffcdd2;
        border-left: 4px solid #f44336;
    }
    
    .stWarning {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    
    .stInfo {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    </style>
    """, unsafe_allow_html=True)

def show_auth_interface():
    """Show authentication interface (login/registration only)"""
    try:
        # Language dropdown at the top
        show_language_dropdown()
        
        # Main header
        st.markdown("""
        <div class="main-header">
            <h1 style="color: #2e7d32; font-size: 3rem; margin-bottom: 1rem;">
                🏠 HAVEN
            </h1>
            <h2 style="color: #388e3c; margin-bottom: 1rem;">
                Crowdfunding Platform
            </h2>
            <p style="color: #4caf50; font-size: 1.2rem;">
                Empowering Communities Through Crowdfunding
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Authentication tabs
        tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Register"])
        
        with tab1:
            if PAGES_AVAILABLE:
                try:
                    login.show()
                except Exception as e:
                    logger.error(f"Error loading login page: {e}")
                    show_fallback_login()
            else:
                show_fallback_login()
        
        with tab2:
            if PAGES_AVAILABLE:
                try:
                    register.show()
                except Exception as e:
                    logger.error(f"Error loading register page: {e}")
                    show_fallback_register()
            else:
                show_fallback_register()
        
        # Platform information
        show_platform_info()
        
    except Exception as e:
        logger.error(f"Auth interface error: {e}")
        st.error("Error loading authentication interface.")

def show_main_interface():
    """Show main application interface for authenticated users"""
    try:
        # Sidebar navigation
        with st.sidebar:
            show_user_info()
            show_language_dropdown()
            show_navigation_menu()
            show_logout_button()
        
        # Main content area
        current_page = st.session_state.get('current_page', 'home')
        
        if PAGES_AVAILABLE:
            try:
                if current_page == 'home':
                    home.show()
                elif current_page == 'explore':
                    explore.show()
                elif current_page == 'search':
                    search.show()
                elif current_page == 'campaign':
                    campaign.show()
                elif current_page == 'profile':
                    profile.show()
                else:
                    # Default to home
                    home.show()
            except Exception as e:
                logger.error(f"Error loading page {current_page}: {e}")
                show_fallback_page(current_page)
        else:
            show_fallback_page(current_page)
        
        # Floating action button for quick campaign creation
        show_floating_action_button()
        
    except Exception as e:
        logger.error(f"Main interface error: {e}")
        st.error("Error loading main interface.")

def show_language_dropdown():
    """Show language selection dropdown"""
    try:
        st.markdown("### 🌍 Language / भाषा")
        
        languages = {
            "English": "🇺🇸 English",
            "Hindi": "🇮🇳 हिंदी", 
            "Tamil": "🇮🇳 தமிழ்",
            "Telugu": "🇮🇳 తెలుగు"
        }
        
        selected_language = st.selectbox(
            "Choose your language",
            options=list(languages.keys()),
            format_func=lambda x: languages[x],
            index=list(languages.keys()).index(st.session_state.get('language', 'English')),
            key="language_selector"
        )
        
        if selected_language != st.session_state.get('language'):
            st.session_state.language = selected_language
            st.success(f"Language changed to {languages[selected_language]}")
            st.rerun()
            
    except Exception as e:
        logger.error(f"Language dropdown error: {e}")
        st.error("Error loading language options.")

def show_user_info():
    """Show user information in sidebar"""
    try:
        user = st.session_state.get('user', {})
        user_name = user.get('name', 'User')
        user_email = user.get('email', 'user@example.com')
        user_avatar = user.get('avatar', '👤')
        
        st.markdown(f"""
        <div class="card-panel" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{user_avatar}</div>
            <h3 style="color: #2e7d32; margin-bottom: 0.5rem;">{user_name}</h3>
            <p style="color: #666; font-size: 0.9rem;">{user_email}</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"User info error: {e}")

def show_navigation_menu():
    """Show navigation menu for authenticated users"""
    try:
        st.markdown("### 🧭 Navigation")
        
        # Navigation options
        nav_options = {
            'home': {'icon': '🏠', 'label': 'Home', 'description': 'Dashboard and overview'},
            'explore': {'icon': '🔍', 'label': 'Explore', 'description': 'Browse campaigns'},
            'search': {'icon': '🔎', 'label': 'Search', 'description': 'Find specific campaigns'},
            'campaign': {'icon': '🎯', 'label': 'Campaigns', 'description': 'Manage your campaigns'},
            'profile': {'icon': '👤', 'label': 'Profile', 'description': 'Account settings'}
        }
        
        current_page = st.session_state.get('current_page', 'home')
        
        for page_key, page_info in nav_options.items():
            # Create button with active state styling
            button_class = "nav-button active" if page_key == current_page else "nav-button"
            
            if st.button(
                f"{page_info['icon']} {page_info['label']}",
                key=f"nav_{page_key}",
                help=page_info['description'],
                use_container_width=True
            ):
                st.session_state.current_page = page_key
                st.rerun()
        
        # Quick stats
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 Raised", "₹2.5L", "+₹15K")
        with col2:
            st.metric("🎯 Campaigns", "3", "+1")
        
    except Exception as e:
        logger.error(f"Navigation menu error: {e}")

def show_logout_button():
    """Show logout button"""
    try:
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            # Clear session state
            st.session_state.authenticated = False
            st.session_state.user = {}
            st.session_state.current_page = 'login'
            
            st.success("👋 Logged out successfully!")
            st.rerun()
            
    except Exception as e:
        logger.error(f"Logout error: {e}")

def show_floating_action_button():
    """Show floating action button for quick campaign creation"""
    try:
        st.markdown("""
        <div class="floating-action-btn" onclick="createCampaign()" title="Create New Campaign">
            ➕
        </div>
        
        <script>
        function createCampaign() {
            // This would trigger campaign creation
            alert('Quick campaign creation coming soon!');
        }
        </script>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Floating action button error: {e}")

def show_platform_info():
    """Show platform information for unauthenticated users"""
    try:
        st.markdown("---")
        st.markdown("### ℹ️ About HAVEN Platform")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 🎯 Create Campaigns
            Launch your fundraising campaigns with ease. Our platform provides all the tools you need to tell your story and reach your goals.
            """)
        
        with col2:
            st.markdown("""
            #### 🔍 Discover Causes
            Find and support causes that matter to you. Browse through verified campaigns across multiple categories.
            """)
        
        with col3:
            st.markdown("""
            #### 🔒 Secure & Trusted
            Advanced fraud detection and secure payment processing ensure your donations reach the right hands.
            """)
        
        # Platform statistics
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Total Raised", "₹12.5 Cr")
        
        with col2:
            st.metric("🎯 Active Campaigns", "1,247")
        
        with col3:
            st.metric("👥 Community Members", "45,678")
        
        with col4:
            st.metric("🏆 Success Rate", "78%")
        
    except Exception as e:
        logger.error(f"Platform info error: {e}")

def show_fallback_login():
    """Fallback login interface when modules fail to load"""
    st.markdown("### 🔐 Sign In to HAVEN")
    
    with st.form("fallback_login"):
        email = st.text_input("📧 Email", placeholder="your.email@example.com")
        password = st.text_input("🔒 Password", type="password", placeholder="Your password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("🚀 Sign In", use_container_width=True)
        with col2:
            demo_btn = st.form_submit_button("🎭 Demo Login", use_container_width=True)
    
    if login_btn and email and password:
        # Simple validation for demo
        if "@" in email:
            st.session_state.authenticated = True
            st.session_state.user = {
                'name': email.split('@')[0].title(),
                'email': email,
                'avatar': '👤'
            }
            st.session_state.current_page = 'home'
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Please enter a valid email address")
    
    if demo_btn:
        # Demo login
        st.session_state.authenticated = True
        st.session_state.user = {
            'name': 'Demo User',
            'email': 'demo@haven.com',
            'avatar': '🎭'
        }
        st.session_state.current_page = 'home'
        st.success("✅ Demo login successful!")
        st.rerun()

def show_fallback_register():
    """Fallback registration interface when modules fail to load"""
    st.markdown("### 📝 Create HAVEN Account")
    
    with st.form("fallback_register"):
        name = st.text_input("👤 Full Name", placeholder="Your full name")
        email = st.text_input("📧 Email", placeholder="your.email@example.com")
        password = st.text_input("🔒 Password", type="password", placeholder="Create password")
        terms = st.checkbox("I agree to Terms of Service")
        
        register_btn = st.form_submit_button("🎉 Create Account", use_container_width=True)
    
    if register_btn:
        if name and email and password and terms:
            st.session_state.authenticated = True
            st.session_state.user = {
                'name': name,
                'email': email,
                'avatar': '👤'
            }
            st.session_state.current_page = 'home'
            st.success("🎉 Account created successfully!")
            st.balloons()
            st.rerun()
        else:
            st.error("❌ Please fill all fields and accept terms")

def show_fallback_page(page_name: str):
    """Show fallback page when modules fail to load"""
    st.markdown(f"""
    <div class="main-header">
        <h1 style="color: #2e7d32;">🚧 {page_name.title()} Page</h1>
        <p style="color: #666;">This page is currently under development.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"The {page_name} page functionality will be available soon. Please check back later!")

if __name__ == "__main__":
    main()

