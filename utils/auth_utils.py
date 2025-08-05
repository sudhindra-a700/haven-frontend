"""
Authentication Utilities for HAVEN Crowdfunding Platform Frontend
Handles OAuth, session management, and authentication flows
"""

import streamlit as st
import jwt
import time
import webbrowser
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AuthUtils:
    """
    Authentication utilities for frontend
    """
    
    def __init__(self, api_client):
        self.api_client = api_client
    
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate access token and return user info"""
        try:
            # Try to get user info with the token
            user_info = self.api_client.get_current_user(token)
            return user_info
        except Exception as e:
            logger.error(f"Token validation failed: {e}")
            return None
    
    def is_token_expired(self, token: str) -> bool:
        """Check if JWT token is expired"""
        try:
            # Decode without verification to check expiration
            decoded = jwt.decode(token, options={"verify_signature": False})
            exp = decoded.get('exp')
            
            if exp:
                return datetime.utcnow().timestamp() > exp
            
            return True  # If no expiration, consider expired
            
        except Exception:
            return True
    
    def refresh_access_token(self) -> bool:
        """Refresh access token using refresh token"""
        try:
            refresh_token = st.session_state.get('refresh_token')
            if not refresh_token:
                return False
            
            response = self.api_client.refresh_token(refresh_token)
            
            if response and 'access_token' in response:
                st.session_state.access_token = response['access_token']
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            return False
    
    def handle_oauth_login(self, provider: str) -> str:
        """Handle OAuth login flow"""
        try:
            # Get current URL for redirect
            current_url = st.experimental_get_query_params().get('redirect_url', [''])[0]
            if not current_url:
                current_url = "http://localhost:8501"  # Default Streamlit URL
            
            # Get OAuth URL from backend
            if provider == 'google':
                auth_url = self.api_client.get_google_auth_url(current_url)
            elif provider == 'facebook':
                auth_url = self.api_client.get_facebook_auth_url(current_url)
            else:
                raise ValueError(f"Unsupported OAuth provider: {provider}")
            
            return auth_url
            
        except Exception as e:
            logger.error(f"OAuth URL generation failed: {e}")
            raise
    
    def login_with_credentials(self, email: str, password: str) -> bool:
        """Login with email and password"""
        try:
            response = self.api_client.login(email, password)
            
            if response and 'access_token' in response:
                # Store authentication data
                st.session_state.authenticated = True
                st.session_state.access_token = response['access_token']
                st.session_state.refresh_token = response.get('refresh_token')
                st.session_state.user = response.get('user')
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise
    
    def register_user(self, email: str, password: str, full_name: str, phone_number: str = None) -> bool:
        """Register new user"""
        try:
            response = self.api_client.register(email, password, full_name, phone_number)
            
            if response and 'access_token' in response:
                # Store authentication data
                st.session_state.authenticated = True
                st.session_state.access_token = response['access_token']
                st.session_state.refresh_token = response.get('refresh_token')
                st.session_state.user = response.get('user')
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            raise
    
    def logout_user(self) -> bool:
        """Logout current user"""
        try:
            # Call logout API
            if st.session_state.get('access_token'):
                self.api_client.logout(st.session_state.access_token)
            
            # Clear session state
            self.clear_auth_session()
            
            return True
            
        except Exception as e:
            logger.error(f"Logout failed: {e}")
            # Clear session anyway
            self.clear_auth_session()
            return False
    
    def clear_auth_session(self):
        """Clear authentication session data"""
        keys_to_clear = [
            'authenticated',
            'access_token',
            'refresh_token',
            'user'
        ]
        
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    def check_authentication(self) -> bool:
        """Check if user is authenticated and token is valid"""
        if not st.session_state.get('authenticated'):
            return False
        
        token = st.session_state.get('access_token')
        if not token:
            return False
        
        # Check if token is expired
        if self.is_token_expired(token):
            # Try to refresh token
            if self.refresh_access_token():
                return True
            else:
                # Refresh failed, clear session
                self.clear_auth_session()
                return False
        
        return True
    
    def require_authentication(self, redirect_to_login: bool = True) -> bool:
        """Require authentication for protected pages"""
        if self.check_authentication():
            return True
        
        if redirect_to_login:
            st.warning("Please login to access this page")
            st.session_state.current_page = 'login'
            st.experimental_rerun()
        
        return False
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current authenticated user"""
        if not self.check_authentication():
            return None
        
        return st.session_state.get('user')
    
    def update_user_session(self, user_data: Dict[str, Any]):
        """Update user data in session"""
        if st.session_state.get('authenticated'):
            st.session_state.user = user_data
    
    def has_permission(self, required_role: str) -> bool:
        """Check if current user has required role"""
        user = self.get_current_user()
        if not user:
            return False
        
        user_role = user.get('role', 'user')
        
        # Role hierarchy: admin > moderator > user
        role_hierarchy = {
            'user': 1,
            'moderator': 2,
            'admin': 3
        }
        
        user_level = role_hierarchy.get(user_role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return user_level >= required_level
    
    def is_admin(self) -> bool:
        """Check if current user is admin"""
        return self.has_permission('admin')
    
    def is_moderator(self) -> bool:
        """Check if current user is moderator"""
        return self.has_permission('moderator')
    
    def get_auth_header(self) -> Dict[str, str]:
        """Get authorization header for API requests"""
        token = st.session_state.get('access_token')
        if token:
            return {'Authorization': f'Bearer {token}'}
        return {}
    
    def handle_auth_error(self, error: Exception):
        """Handle authentication errors"""
        error_message = str(error)
        
        if 'token' in error_message.lower() or 'unauthorized' in error_message.lower():
            # Token-related error, clear session and redirect to login
            self.clear_auth_session()
            st.error("Your session has expired. Please login again.")
            st.session_state.current_page = 'login'
            st.experimental_rerun()
        else:
            # Other authentication error
            st.error(f"Authentication error: {error_message}")
    
    def create_oauth_popup_script(self, auth_url: str, provider: str) -> str:
        """Create JavaScript for OAuth popup window"""
        return f"""
        <script>
        function openOAuthWindow() {{
            const popup = window.open(
                '{auth_url}',
                '{provider}_oauth',
                'width=500,height=600,scrollbars=yes,resizable=yes'
            );
            
            // Check for popup completion
            const checkClosed = setInterval(function() {{
                if (popup.closed) {{
                    clearInterval(checkClosed);
                    // Reload the page to check for auth tokens
                    window.location.reload();
                }}
            }}, 1000);
        }}
        
        // Auto-open popup
        openOAuthWindow();
        </script>
        """
    
    def render_oauth_buttons(self):
        """Render OAuth login buttons"""
        st.markdown("### Social Login")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Login with Google", key="google_oauth", use_container_width=True):
                try:
                    auth_url = self.handle_oauth_login('google')
                    
                    # Create popup script
                    popup_script = self.create_oauth_popup_script(auth_url, 'google')
                    st.components.v1.html(popup_script, height=0)
                    
                    st.info("Opening Google login window...")
                    
                except Exception as e:
                    st.error(f"Google login failed: {e}")
        
        with col2:
            if st.button("📘 Login with Facebook", key="facebook_oauth", use_container_width=True):
                try:
                    auth_url = self.handle_oauth_login('facebook')
                    
                    # Create popup script
                    popup_script = self.create_oauth_popup_script(auth_url, 'facebook')
                    st.components.v1.html(popup_script, height=0)
                    
                    st.info("Opening Facebook login window...")
                    
                except Exception as e:
                    st.error(f"Facebook login failed: {e}")
    
    def validate_password_strength(self, password: str) -> tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        if not has_upper:
            return False, "Password must contain at least one uppercase letter"
        
        if not has_lower:
            return False, "Password must contain at least one lowercase letter"
        
        if not has_digit:
            return False, "Password must contain at least one digit"
        
        if not has_special:
            return False, "Password must contain at least one special character"
        
        return True, "Password is strong"
    
    def validate_email(self, email: str) -> tuple[bool, str]:
        """Validate email format"""
        import re
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            return True, "Email is valid"
        else:
            return False, "Invalid email format"
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get current session information"""
        return {
            'authenticated': st.session_state.get('authenticated', False),
            'user': st.session_state.get('user'),
            'token_present': bool(st.session_state.get('access_token')),
            'session_keys': list(st.session_state.keys())
        }

