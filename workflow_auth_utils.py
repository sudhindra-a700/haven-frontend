"""
COMPATIBILITY UPDATED Workflow Authentication Utilities for HAVEN Platform
Ensures compatibility with the fully integrated Streamlit app

This module provides authentication utilities that work seamlessly with:
1. fully_integrated_app.py
2. corrected_authentication_flow.py
3. Streamlit compatibility fixes
4. Term simplification features
"""

import streamlit as st
import logging
import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

# Backend configuration
BACKEND_URL = st.secrets.get('BACKEND_URL', 'https://haven-backend-9lw3.onrender.com')

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

def get_auth_manager():
    """Get authentication manager instance"""
    try:
        from corrected_authentication_flow import auth_manager
        return auth_manager
    except ImportError:
        logger.warning("Authentication flow module not available")
        return None

def check_user_authentication() -> bool:
    """Check if user is authenticated with database verification"""
    
    # Check session state first
    if not st.session_state.get('authenticated', False):
        return False
    
    # Verify user data exists
    user_data = st.session_state.get('user_data')
    user_type = st.session_state.get('user_type')
    
    if not user_data or not user_type:
        logger.warning("User data missing, clearing authentication")
        clear_authentication()
        return False
    
    # Verify user still exists in database
    try:
        exists, _ = check_user_in_database(user_data.get('email'), user_type)
        if not exists:
            logger.warning("User no longer exists in database")
            clear_authentication()
            return False
    except Exception as e:
        logger.error(f"Error verifying user in database: {e}")
        return False
    
    return True

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

def handle_user_login(provider: str, user_type: str) -> bool:
    """Handle user login process"""
    try:
        # Generate OAuth URL
        oauth_url = generate_oauth_url(provider, user_type)
        if not oauth_url:
            return False
        
        # Store login attempt in session
        st.session_state.login_attempt = {
            'provider': provider,
            'user_type': user_type,
            'timestamp': datetime.now().isoformat()
        }
        
        # Open OAuth popup
        st.markdown(f"""
        <script>
        window.open('{oauth_url}', 'oauth_popup', 'width=500,height=600,scrollbars=yes,resizable=yes');
        </script>
        """, unsafe_allow_html=True)
        
        st.success(f"🔄 {provider.title()} login window opened. Please complete authentication.")
        return True
        
    except Exception as e:
        logger.error(f"Error in handle_user_login: {e}")
        st.error(f"❌ Login error: {str(e)}")
        return False

def generate_oauth_url(provider: str, user_type: str) -> Optional[str]:
    """Generate OAuth URL for the specified provider"""
    try:
        # Create state parameter with provider and user_type
        state = json.dumps({
            'provider': provider,
            'user_type': user_type,
            'timestamp': datetime.now().isoformat()
        })
        
        frontend_url = st.secrets.get('FRONTEND_URL', 'https://haven-frontend-65jr.onrender.com')
        oauth_url = f"{BACKEND_URL}/api/v1/auth/{provider}/login"
        oauth_url += f"?user_type={user_type}&state={state}&redirect_uri={frontend_url}"
        
        return oauth_url
        
    except Exception as e:
        logger.error(f"Error generating OAuth URL: {e}")
        return None

def handle_user_logout():
    """Handle user logout process"""
    try:
        # Clear authentication state
        clear_authentication()
        
        # Clear any cached data
        if 'login_attempt' in st.session_state:
            del st.session_state.login_attempt
        
        # Reset to login page
        st.session_state.current_page = 'login'
        
        logger.info("User logged out successfully")
        st.success("✅ Logged out successfully!")
        
        # Rerun to refresh the app
        safe_rerun()
        
    except Exception as e:
        logger.error(f"Error in handle_user_logout: {e}")
        st.error(f"❌ Logout error: {str(e)}")

def clear_authentication():
    """Clear all authentication-related session state"""
    keys_to_clear = [
        'authenticated', 'user_data', 'user_type', 
        'selected_role', 'oauth_callback_handled'
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def get_user_role() -> Optional[str]:
    """Get current user role"""
    return st.session_state.get('user_type')

def get_current_user_data() -> Optional[Dict[str, Any]]:
    """Get current user data"""
    return st.session_state.get('user_data')

def require_authentication(redirect_to_login: bool = True) -> bool:
    """Require user to be authenticated"""
    if not check_user_authentication():
        if redirect_to_login:
            st.error("❌ Authentication required. Please log in.")
            st.session_state.current_page = 'login'
            safe_rerun()
        return False
    return True

def require_role(required_role: str) -> bool:
    """Require user to have specific role"""
    if not require_authentication():
        return False
    
    user_role = get_user_role()
    if user_role != required_role:
        st.error(f"❌ Access denied. {required_role.title()} role required.")
        return False
    
    return True

def show_login_form():
    """Show login form with role selection"""
    
    st.markdown("### 🎯 Choose Your Role to Login")
    
    st.markdown("""
    <div class='info-message'>
        <h4>💡 Important</h4>
        <p>You must be registered in our database before you can log in.</p>
        <p><strong>Process:</strong> Registration → Database Storage → Login → Access</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Role selection
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
        
        if st.button("Login as Individual", key="auth_login_individual", use_container_width=True, type="primary"):
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
        
        if st.button("Login as Organization", key="auth_login_organization", use_container_width=True, type="primary"):
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
        
        show_oauth_buttons(st.session_state.selected_role)
        
        # Back button
        if st.button("⬅️ Back to Role Selection", key="auth_back_to_role"):
            if "selected_role" in st.session_state:
                del st.session_state.selected_role
            safe_rerun()

def show_oauth_buttons(user_type: str):
    """Show OAuth authentication buttons"""
    
    # OAuth section with pulse effect
    st.markdown("""
    <div class='oauth-section'>
        <h4 style='text-align: center; color: #4CAF50;'>🔐 Secure Login Options</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Continue with Google", key=f"auth_google_{user_type}", use_container_width=True, type="primary"):
            if handle_user_login("google", user_type):
                st.markdown("""
                <div class='info-message'>
                    <p>🔄 Google authentication window opened. Please complete authentication and return to this page.</p>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        if st.button("📘 Continue with Facebook", key=f"auth_facebook_{user_type}", use_container_width=True, type="primary"):
            if handle_user_login("facebook", user_type):
                st.markdown("""
                <div class='info-message'>
                    <p>🔄 Facebook authentication window opened. Please complete authentication and return to this page.</p>
                </div>
                """, unsafe_allow_html=True)

def show_role_selection() -> Optional[str]:
    """Show role selection and return selected role"""
    
    st.markdown("### 🎯 Choose Your Role")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='role-card'>
            <h4>👤 Individual</h4>
            <p>Donate to campaigns and support causes</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Select Individual", key="role_select_individual", use_container_width=True):
            return "individual"
    
    with col2:
        st.markdown("""
        <div class='role-card'>
            <h4>🏢 Organization</h4>
            <p>Create and manage fundraising campaigns</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Select Organization", key="role_select_organization", use_container_width=True):
            return "organization"
    
    return None

def show_authentication_status():
    """Show current authentication status (for debugging)"""
    
    if st.checkbox("Show Authentication Status", key="auth_debug"):
        st.markdown("### 🔍 Authentication Status")
        
        status_data = {
            "Authenticated": st.session_state.get('authenticated', False),
            "User Type": st.session_state.get('user_type', 'None'),
            "User Email": st.session_state.get('user_data', {}).get('email', 'None'),
            "Selected Role": st.session_state.get('selected_role', 'None'),
            "Current Page": st.session_state.get('current_page', 'None'),
            "Backend URL": BACKEND_URL
        }
        
        for key, value in status_data.items():
            st.write(f"**{key}:** {value}")

def validate_user_session() -> bool:
    """Validate current user session"""
    try:
        if not check_user_authentication():
            return False
        
        user_data = get_current_user_data()
        if not user_data:
            return False
        
        # Additional validation can be added here
        # e.g., token expiry, session timeout, etc.
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating user session: {e}")
        return False

def refresh_user_data():
    """Refresh user data from backend"""
    try:
        user_data = get_current_user_data()
        user_type = get_user_role()
        
        if not user_data or not user_type:
            return False
        
        # Fetch fresh user data from backend
        exists, fresh_data = check_user_in_database(user_data.get('email'), user_type)
        
        if exists and fresh_data:
            st.session_state.user_data = fresh_data
            logger.info("User data refreshed successfully")
            return True
        else:
            logger.warning("Failed to refresh user data")
            return False
            
    except Exception as e:
        logger.error(f"Error refreshing user data: {e}")
        return False

# Compatibility functions for integration with main app
def get_auth_status() -> Dict[str, Any]:
    """Get comprehensive authentication status"""
    return {
        'authenticated': check_user_authentication(),
        'user_data': get_current_user_data(),
        'user_type': get_user_role(),
        'session_valid': validate_user_session()
    }

def initialize_auth_state():
    """Initialize authentication state"""
    if 'auth_initialized' not in st.session_state:
        st.session_state.auth_initialized = True
        logger.info("Authentication state initialized")

# Export functions for main app integration
__all__ = [
    'get_auth_manager',
    'check_user_authentication', 
    'handle_user_login',
    'handle_user_logout',
    'get_user_role',
    'require_authentication',
    'require_role',
    'show_login_form',
    'show_oauth_buttons',
    'show_role_selection',
    'get_current_user_data',
    'validate_user_session',
    'refresh_user_data',
    'get_auth_status',
    'initialize_auth_state'
]

