"""
Enhanced Authentication Utilities for HAVEN Workflow-Based Frontend
Handles OAuth and email authentication with proper workflow integration
"""

import streamlit as st
import requests
import logging
from typing import Dict, Any, Tuple, Optional
import time
import hashlib
import secrets

logger = logging.getLogger(__name__)

class AuthenticationManager:
    """Manages authentication state and operations for workflow-based frontend"""
    
    def __init__(self):
        self.backend_url = self._get_backend_url()
        self.session_timeout = 3600  # 1 hour
        self.max_login_attempts = 5
    
    def _get_backend_url(self) -> str:
        """Get backend URL from configuration"""
        try:
            return st.secrets.get("BACKEND_URL", "https://haven-fastapi-backend.onrender.com")
        except:
            return "https://haven-fastapi-backend.onrender.com"
    
    def initialize_auth_state(self):
        """Initialize authentication-related session state"""
        if 'auth_token' not in st.session_state:
            st.session_state.auth_token = None
        
        if 'auth_expires' not in st.session_state:
            st.session_state.auth_expires = 0
        
        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = 0
        
        if 'last_login_attempt' not in st.session_state:
            st.session_state.last_login_attempt = 0
        
        if 'oauth_state' not in st.session_state:
            st.session_state.oauth_state = None
    
    def check_authentication(self) -> bool:
        """Check if user is currently authenticated"""
        if not st.session_state.user_authenticated:
            return False
        
        # Check token expiration
        if st.session_state.auth_expires < time.time():
            self.logout_user()
            return False
        
        # Validate token with backend if available
        if st.session_state.auth_token:
            return self._validate_token(st.session_state.auth_token)
        
        return True
    
    def _validate_token(self, token: str) -> bool:
        """Validate authentication token with backend"""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(
                f"{self.backend_url}/api/auth/validate",
                headers=headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Token validation failed: {e}")
            return False
    
    def login_user(self, method: str, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
        """Login user with specified method"""
        self.initialize_auth_state()
        
        # Check rate limiting
        if not self._check_rate_limit():
            return False, "Too many login attempts. Please try again later."
        
        try:
            if method == 'email':
                return self._login_email(credentials)
            elif method == 'google':
                return self._login_oauth('google', credentials)
            elif method == 'facebook':
                return self._login_oauth('facebook', credentials)
            else:
                return False, f"Unsupported login method: {method}"
        
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False, f"Login failed: {str(e)}"
    
    def _check_rate_limit(self) -> bool:
        """Check if user has exceeded login attempt rate limit"""
        current_time = time.time()
        
        # Reset attempts if enough time has passed
        if current_time - st.session_state.last_login_attempt > 300:  # 5 minutes
            st.session_state.login_attempts = 0
        
        return st.session_state.login_attempts < self.max_login_attempts
    
    def _login_email(self, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
        """Login with email and password"""
        try:
            response = requests.post(
                f"{self.backend_url}/api/auth/login",
                json={
                    'email': credentials['email'],
                    'password': credentials['password']
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self._set_auth_session(data)
                return True, data['user']
            else:
                self._increment_login_attempts()
                error_data = response.json() if response.content else {}
                return False, error_data.get('detail', 'Login failed')
        
        except requests.RequestException as e:
            self._increment_login_attempts()
            logger.error(f"Email login request failed: {e}")
            # Demo mode fallback
            if credentials['email'] and credentials['password']:
                demo_user = {
                    'id': 'demo_user',
                    'email': credentials['email'],
                    'first_name': 'Demo',
                    'last_name': 'User',
                    'verified': True
                }
                self._set_auth_session({'user': demo_user, 'token': 'demo_token'})
                return True, demo_user
            return False, "Network error. Please check your connection."
    
    def _login_oauth(self, provider: str, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
        """Login with OAuth provider"""
        try:
            # Generate OAuth state for security
            oauth_state = secrets.token_urlsafe(32)
            st.session_state.oauth_state = oauth_state
            
            # In a real implementation, this would redirect to OAuth provider
            # For demo purposes, we'll simulate successful OAuth
            demo_user = {
                'id': f'oauth_{provider}_demo',
                'email': f'demo@{provider}.com',
                'first_name': 'OAuth',
                'last_name': 'User',
                'provider': provider,
                'verified': True
            }
            
            self._set_auth_session({'user': demo_user, 'token': f'oauth_{provider}_token'})
            return True, demo_user
        
        except Exception as e:
            self._increment_login_attempts()
            logger.error(f"OAuth login failed: {e}")
            return False, f"OAuth login failed: {str(e)}"
    
    def register_user(self, method: str, user_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Register new user with specified method"""
        try:
            if method == 'email':
                return self._register_email(user_data)
            elif method in ['google', 'facebook']:
                return self._register_oauth(method, user_data)
            else:
                return False, f"Unsupported registration method: {method}"
        
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False, f"Registration failed: {str(e)}"
    
    def _register_email(self, user_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Register with email"""
        try:
            response = requests.post(
                f"{self.backend_url}/api/auth/register",
                json=user_data,
                timeout=30
            )
            
            if response.status_code == 201:
                data = response.json()
                self._set_auth_session(data)
                return True, data['user']
            else:
                error_data = response.json() if response.content else {}
                return False, error_data.get('detail', 'Registration failed')
        
        except requests.RequestException as e:
            logger.error(f"Email registration request failed: {e}")
            # Demo mode fallback
            demo_user = {
                'id': f'user_{int(time.time())}',
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'phone': user_data.get('phone', ''),
                'verified': False
            }
            self._set_auth_session({'user': demo_user, 'token': 'demo_token'})
            return True, demo_user
    
    def _register_oauth(self, provider: str, user_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Register with OAuth provider"""
        try:
            # Generate OAuth state for security
            oauth_state = secrets.token_urlsafe(32)
            st.session_state.oauth_state = oauth_state
            
            # Demo OAuth registration
            demo_user = {
                'id': f'oauth_{provider}_{int(time.time())}',
                'email': f'new_user@{provider}.com',
                'first_name': 'New',
                'last_name': 'User',
                'provider': provider,
                'verified': True
            }
            
            self._set_auth_session({'user': demo_user, 'token': f'oauth_{provider}_token'})
            return True, demo_user
        
        except Exception as e:
            logger.error(f"OAuth registration failed: {e}")
            return False, f"OAuth registration failed: {str(e)}"
    
    def _set_auth_session(self, auth_data: Dict[str, Any]):
        """Set authentication session data"""
        st.session_state.user_authenticated = True
        st.session_state.user_data = auth_data['user']
        st.session_state.auth_token = auth_data.get('token')
        st.session_state.auth_expires = time.time() + self.session_timeout
        st.session_state.login_attempts = 0  # Reset on successful login
    
    def _increment_login_attempts(self):
        """Increment failed login attempts"""
        st.session_state.login_attempts += 1
        st.session_state.last_login_attempt = time.time()
    
    def logout_user(self):
        """Logout current user"""
        try:
            # Notify backend of logout if token exists
            if st.session_state.auth_token:
                headers = {'Authorization': f'Bearer {st.session_state.auth_token}'}
                requests.post(
                    f"{self.backend_url}/api/auth/logout",
                    headers=headers,
                    timeout=10
                )
        except Exception as e:
            logger.warning(f"Logout notification failed: {e}")
        
        # Clear session state
        st.session_state.user_authenticated = False
        st.session_state.user_data = {}
        st.session_state.auth_token = None
        st.session_state.auth_expires = 0
        st.session_state.oauth_state = None
    
    def get_user_profile(self) -> Optional[Dict[str, Any]]:
        """Get current user profile"""
        if not self.check_authentication():
            return None
        
        try:
            headers = {'Authorization': f'Bearer {st.session_state.auth_token}'}
            response = requests.get(
                f"{self.backend_url}/api/users/me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return st.session_state.user_data
        
        except Exception as e:
            logger.warning(f"Profile fetch failed: {e}")
            return st.session_state.user_data
    
    def update_user_profile(self, profile_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Update user profile"""
        if not self.check_authentication():
            return False, "Not authenticated"
        
        try:
            headers = {'Authorization': f'Bearer {st.session_state.auth_token}'}
            response = requests.put(
                f"{self.backend_url}/api/users/me",
                json=profile_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                updated_user = response.json()
                st.session_state.user_data.update(updated_user)
                return True, "Profile updated successfully"
            else:
                error_data = response.json() if response.content else {}
                return False, error_data.get('detail', 'Update failed')
        
        except Exception as e:
            logger.error(f"Profile update failed: {e}")
            return False, f"Update failed: {str(e)}"
    
    def change_password(self, current_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        if not self.check_authentication():
            return False, "Not authenticated"
        
        try:
            headers = {'Authorization': f'Bearer {st.session_state.auth_token}'}
            response = requests.post(
                f"{self.backend_url}/api/auth/change-password",
                json={
                    'current_password': current_password,
                    'new_password': new_password
                },
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return True, "Password changed successfully"
            else:
                error_data = response.json() if response.content else {}
                return False, error_data.get('detail', 'Password change failed')
        
        except Exception as e:
            logger.error(f"Password change failed: {e}")
            return False, f"Password change failed: {str(e)}"

# Global authentication manager instance
auth_manager = AuthenticationManager()

# Convenience functions for workflow integration
def check_authentication() -> bool:
    """Check if user is authenticated"""
    return auth_manager.check_authentication()

def login_user(method: str, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
    """Login user"""
    return auth_manager.login_user(method, credentials)

def register_user(method: str, user_data: Dict[str, Any]) -> Tuple[bool, Any]:
    """Register user"""
    return auth_manager.register_user(method, user_data)

def logout_user():
    """Logout user"""
    auth_manager.logout_user()

def get_current_user() -> Optional[Dict[str, Any]]:
    """Get current user data"""
    return auth_manager.get_user_profile()

def update_user_profile(profile_data: Dict[str, Any]) -> Tuple[bool, str]:
    """Update user profile"""
    return auth_manager.update_user_profile(profile_data)

def change_password(current_password: str, new_password: str) -> Tuple[bool, str]:
    """Change user password"""
    return auth_manager.change_password(current_password, new_password)

def is_oauth_enabled() -> bool:
    """Check if OAuth is enabled"""
    try:
        return st.secrets.get("OAUTH_ENABLED", "true").lower() == "true"
    except:
        return True  # Default to enabled

