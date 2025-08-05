import streamlit as st
import os
import sys
from pathlib import Path

# Set page config FIRST - before any other Streamlit commands
st.set_page_config(
    page_title="HAVEN - Crowdfunding Platform",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import custom modules (after path setup)
try:
    from pages import home, login
    from utils import config, auth_utils
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure all required files are present in the deployment.")
    st.stop()

def get_config_value(key, default=None):
    """Get configuration value from environment variables or Streamlit secrets"""
    # Try environment variables first (for Render deployment)
    env_value = os.getenv(key)
    if env_value:
        return env_value
    
    # Try Streamlit secrets (for local development)
    try:
        return st.secrets.get(key, default)
    except:
        return default

def main():
    """Main application function"""
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    # Get configuration values
    backend_url = get_config_value('BACKEND_URL', 'http://localhost:8000')
    translation_enabled = get_config_value('TRANSLATION_ENABLED', 'true').lower() == 'true'
    oauth_enabled = get_config_value('OAUTH_ENABLED', 'true').lower() == 'true'
    
    # Store in session state for use across the app
    st.session_state.backend_url = backend_url
    st.session_state.translation_enabled = translation_enabled
    st.session_state.oauth_enabled = oauth_enabled
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🏠 HAVEN")
        st.markdown("---")
        
        # Navigation menu
        pages = {
            "🏠 Home": "home",
            "🔐 Login": "login",
            "📊 Dashboard": "dashboard",
            "💰 Campaigns": "campaigns",
            "👤 Profile": "profile"
        }
        
        selected_page = st.selectbox(
            "Navigate to:",
            options=list(pages.keys()),
            index=0 if st.session_state.current_page == 'home' else 
                  1 if st.session_state.current_page == 'login' else 0
        )
        
        st.session_state.current_page = pages[selected_page]
        
        # Configuration info
        st.markdown("---")
        st.markdown("### Configuration")
        st.markdown(f"**Backend**: {backend_url}")
        st.markdown(f"**Translation**: {'✅' if translation_enabled else '❌'}")
        st.markdown(f"**OAuth**: {'✅' if oauth_enabled else '❌'}")
    
    # Main content area
    try:
        if st.session_state.current_page == 'home':
            home.show()
        elif st.session_state.current_page == 'login':
            login.show()
        elif st.session_state.current_page == 'dashboard':
            st.title("📊 Dashboard")
            st.info("Dashboard functionality coming soon!")
        elif st.session_state.current_page == 'campaigns':
            st.title("💰 Campaigns")
            st.info("Campaign management coming soon!")
        elif st.session_state.current_page == 'profile':
            st.title("👤 Profile")
            st.info("User profile coming soon!")
        else:
            home.show()
    except Exception as e:
        st.error(f"Error loading page: {e}")
        st.error("Falling back to basic interface...")
        
        # Fallback basic interface
        st.title("🏠 HAVEN - Crowdfunding Platform")
        st.markdown("Welcome to HAVEN, your trusted crowdfunding platform.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🎯 Create Campaign")
            st.markdown("Launch your crowdfunding campaign")
            if st.button("Start Campaign"):
                st.info("Campaign creation coming soon!")
        
        with col2:
            st.markdown("### 🔍 Browse Projects")
            st.markdown("Discover amazing projects")
            if st.button("Browse"):
                st.info("Project browsing coming soon!")
        
        with col3:
            st.markdown("### 💝 Support Causes")
            st.markdown("Make a difference today")
            if st.button("Donate"):
                st.info("Donation system coming soon!")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>© 2025 HAVEN - Crowdfunding Platform | Built with ❤️ using Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

